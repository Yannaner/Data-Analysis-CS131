import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not file_path:
        return None

    try:
        data = pd.read_excel(file_path)
        data.columns = ['Top queries', 'Clicks', 'Impressions', 'CTR', 'Position', 'Mon-Year']
        data['Mon-Year'] = pd.to_datetime(data['Mon-Year'], format='%b-%Y')
        messagebox.showinfo("File Upload", "File uploaded successfully!")
        run_all_analyses(data)
        return data
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to load file: {e}")
        return None

def run_all_analyses(data):
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("SEO Analysis Dashboard", fontsize=16, fontweight='bold')
    trend_analysis(data, axs[0, 0])
    top_performing_queries(data, axs[0, 1])
    ctr_vs_position(data, axs[1, 0])
    seasonal_trends(data, axs[1, 1])
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def trend_analysis(data, ax):
    monthly_data = data.groupby('Mon-Year')[['Clicks', 'Impressions']].sum().reset_index()
    ax.plot(monthly_data['Mon-Year'], monthly_data['Clicks'], label='Clicks', marker='o')
    ax.plot(monthly_data['Mon-Year'], monthly_data['Impressions'], label='Impressions', marker='s')
    ax.set_title("Monthly Trends for Clicks and Impressions")
    ax.set_xlabel("Month-Year")
    ax.set_ylabel("Count")
    ax.legend()
    ax.grid()

def top_performing_queries(data, ax):
    top_queries = data.groupby('Top queries')[['Clicks', 'Impressions']].sum().reset_index()
    top_queries = top_queries.sort_values(by='Clicks', ascending=False).head(10)
    sns.barplot(x='Clicks', y='Top queries', data=top_queries, palette='viridis', ax=ax)
    ax.set_title("Top 10 Performing Queries by Clicks")
    ax.set_xlabel("Clicks")
    ax.set_ylabel("Top Queries")
    ax.grid()

def ctr_vs_position(data, ax):
    sns.scatterplot(x='Position', y='CTR', data=data, alpha=0.6, ax=ax)
    ax.set_title("CTR vs Average Position")
    ax.set_xlabel("Position")
    ax.set_ylabel("CTR (%)")
    ax.grid()

def seasonal_trends(data, ax):
    monthly_clicks = data.groupby(data['Mon-Year'].dt.month)['Clicks'].sum()
    ax.bar(monthly_clicks.index, monthly_clicks.values, color='teal', edgecolor='black')
    ax.set_title("Seasonal Trends in Clicks")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Clicks")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    ax.grid()
