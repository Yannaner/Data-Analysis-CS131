import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog, messagebox
import tkinter as tk
import re
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import openai

class AdvancedDataAnalyzer:
    def __init__(self):
        self.data_sources = {}
        self.correlation_matrix = None
        self.openai_api_key = "sk-Tdacw0oH88psakmesW7gqy4koThjB7TAs-dfPbFyvWT3BlbkFJ43g2710o707BsEDSBtDQXqzfW48K246YgiTgn3DtUA"  

    #fuzzy matching by normalizing

    def fuzzy_column_match(self, df, target_column):
        def normalize_column_name(col):
            return re.sub(r'[^a-zA-Z]', '', col).lower()
        
        normalized_target = normalize_column_name(target_column)
        normalized_columns = {normalize_column_name(col): col for col in df.columns}
        if normalized_target in normalized_columns:
            return normalized_columns[normalized_target]
        matches = [col for col in normalized_columns.keys() if normalized_target in col]
        if matches:
            return normalized_columns[matches[0]]
        
        return None

    def load_data_sources(self):
        file_types = [
            ("SEO Queries", "seo_queries.xlsx"),
            ("Traffic Data", "traffic.xlsx"),
            ("Leads Data", "leads.xlsx"),
            ("SEO Pages", "seo_pages.xlsx"),
            ("Items Catalog", "items_catalog.xlsx")
        ]

        for file_type, default_name in file_types:
            file_path = filedialog.askopenfilename(
                title=f"Select {file_type} Excel File", 
                filetypes=[("Excel files", "*.xlsx;*.xls")]
            )
            if file_path:
                try:
                    df = pd.read_excel(file_path)
                    self.data_sources[file_type] = df
                except Exception as e:
                    messagebox.showerror("File Load Error", f"Error loading {file_type}: {str(e)}")

    def create_composite_key(self, data_type):
        #https://www.ibm.com/docs/en/zvm/7.4?topic=keys-match
        #https://www.youtube.com/watch?v=_2HODd8Gq3A
        df = self.data_sources[data_type].copy()
        
        key_strategies = {
            "SEO Queries": {
                "key_columns": ['Top queries', 'Position'],
                "description_column": ['Top queries', 'Queries']
            },
            "Traffic Data": {
                "key_columns": ['Item name', 'Items viewed', 'Item'],
                "description_column": ['Item name', 'Item']
            },
            "Leads Data": {
                "key_columns": ['Products Requested', 'Product ID', 'Product'],
                "description_column": ['Products Requested', 'Product']
            },
            "SEO Pages": {
                "key_columns": ['Page', 'Clicks', 'URL'],
                "description_column": ['Page', 'URL']
            },
            "Items Catalog": {
                "key_columns": ['item_number', 'item_product_group', 'Item Number'],
                "description_column": ['item_description', 'Description']
            }
        }

        strategy = key_strategies.get(data_type, {})

        matched_key_columns = []
        for potential_column in strategy.get('key_columns', []):
            matched_col = self.fuzzy_column_match(df, potential_column)
            if matched_col:
                matched_key_columns.append(matched_col)
        description_column = None
        for potential_column in strategy.get('description_column', []):
            matched_col = self.fuzzy_column_match(df, potential_column)
            if matched_col:
                description_column = matched_col
                break

        # create composite key if possible
        if matched_key_columns:
            try:
                df['composite_key'] = df[matched_key_columns].apply(lambda row: '_'.join(row.astype(str)), axis=1)
            except Exception as e:
                print(f"Warning: Could not create composite key for {data_type}. Error: {e}")
        
        #description for better matching
        if description_column:
            df['description_key'] = df[description_column].astype(str).str.lower()
        
        return df

    def find_cross_sheet_correlations(self):
        try:
            processed_sources = {
                name: self.create_composite_key(name) 
                for name in self.data_sources.keys()
            }
            correlation_data = {}
            for source_name, source_df in processed_sources.items():
                correlation_data[source_name] = {
                    'total_entries': len(source_df),
                    'unique_entries': len(source_df.get('description_key', source_df.index).unique()),
                    'sample_keys': source_df.get('description_key', source_df.index).head(5).tolist()
                }

            self.visualize_data_correlation(correlation_data)
            self.perform_openai_analysis(processed_sources)
            self.perform_pca_and_regression(processed_sources)
        except Exception as e:
            messagebox.showerror("Correlation Error", f"Error finding cross-sheet correlations: {str(e)}")

    def visualize_data_correlation(self, correlation_data):
        plt.figure(figsize=(12, 6))
        sources = list(correlation_data.keys())
        total_entries = [data['total_entries'] for data in correlation_data.values()]
        unique_entries = [data['unique_entries'] for data in correlation_data.values()]

        plt.subplot(1, 2, 1)
        plt.bar(sources, total_entries, color='skyblue', label='Total Entries')
        plt.title('Total Entries per Data Source')
        plt.xlabel('Data Source')
        plt.ylabel('Number of Entries')
        plt.xticks(rotation=45)

        plt.subplot(1, 2, 2)
        plt.bar(sources, unique_entries, color='lightgreen', label='Unique Entries')
        plt.title('Unique Entries per Data Source')
        plt.xlabel('Data Source')
        plt.ylabel('Number of Unique Entries')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def perform_openai_analysis(self, processed_sources):

        openai.api_key = self.openai_api_key

        for source_name, source_df in processed_sources.items():
            try:
                prompt = f"Provide a detailed analysis of the '{source_name}' data, including key insights, notable trends, and potential relationships with other data sources."
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                analysis = response.choices[0].text
                print(f"OpenAI Analysis for {source_name}:\n{analysis}\n")
            except Exception as e:
                print(f"Error running OpenAI analysis for {source_name}: {str(e)}")

    def perform_pca_and_regression(self, processed_sources):

        for source_name, source_df in processed_sources.items():
            try:
                # Prepare the data for PCA and regression
                numeric_cols = source_df.select_dtypes(include=['number']).columns
                X = source_df[numeric_cols].values
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                pca = PCA(n_components=2)
                X_pca = pca.fit_transform(X_scaled)
                source_df['PCA_1'] = X_pca[:, 0]
                source_df['PCA_2'] = X_pca[:, 1]

                # linear regression
                for target_col in numeric_cols:
                    model = LinearRegression()
                    model.fit(X_scaled, source_df[target_col])
                    r_squared = model.score(X_scaled, source_df[target_col])
                    print(f"Linear Regression for {source_name} '{target_col}': R-squared = {r_squared:.2f}")

                plt.figure(figsize=(8, 8))
                plt.scatter(source_df['PCA_1'], source_df['PCA_2'])
                plt.title(f"PCA for {source_name}")
                plt.xlabel('PCA 1')
                plt.ylabel('PCA 2')
                plt.show()
            except Exception as e:
                print(f"Error performing PCA and regression for {source_name}: {str(e)}")

    def generate_comprehensive_report(self):
        report_text = "Comprehensive Data Analysis Report\n\n"
        
        for source, data in self.data_sources.items():
            report_text += f"{source} Summary:\n"
            report_text += str(data.describe()) + "\n\n"
        with open('comprehensive_data_report.txt', 'w') as f:
            f.write(report_text)

        messagebox.showinfo("Report Generated", "Comprehensive report saved as comprehensive_data_report.txt")

def launch_advanced_data_analysis():
    root = tk.Tk()
    root.title("Advanced Data Analysis")
    
    analyzer = AdvancedDataAnalyzer()
    load_data_btn = tk.Button(root, text="Load Data Sources", command=analyzer.load_data_sources)
    correlate_btn = tk.Button(root, text="Find Cross-Sheet Correlations", command=analyzer.find_cross_sheet_correlations)
    generate_report_btn = tk.Button(root, text="Generate Comprehensive Report", command=analyzer.generate_comprehensive_report)
    
    load_data_btn.pack(pady=10)
    correlate_btn.pack(pady=10)
    generate_report_btn.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    launch_advanced_data_analysis()