# File: seo_analysis_dashboard.py
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class SEOAnalysisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("SEO Analysis Dashboard")
        self.root.geometry("1400x500")

        self.initialize_data()
        self.create_layout()

    def initialize_data(self):
        try:
            self.items_catalog = pd.read_excel('items_catalog.xlsx', sheet_name='Items Catalog')
            self.seo_queries = pd.read_excel('seo_queries.xlsx', sheet_name='SEO Queries')
            self.seo_pages = pd.read_excel('seo_pages.xlsx', sheet_name='SEO Pages')

            self.seo_queries['Mon-Year'] = pd.to_datetime(self.seo_queries['Mon-Year'], format='%Y-%m-%d')
            self.seo_pages['Mon-Year'] = pd.to_datetime(self.seo_pages['Mon-Year'], format='%Y-%m-%d')

            self.item_product_group_mapping = self.items_catalog.groupby('item_product_group')['item_number'].apply(list).reset_index()
        except Exception as e:
            messagebox.showerror("Data Loading Error", f"Could not load data: {e}")
            raise

    def create_layout(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_controls(main_frame)
        self.create_dashboard(main_frame)

    def create_controls(self, parent):
        controls_frame = ttk.Frame(parent, padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.E))

        ttk.Label(controls_frame, text="Select Product Group:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_group_var = tk.StringVar(value="Select Product Group")
        self.product_group_dropdown = ttk.Combobox(
            controls_frame,
            textvariable=self.product_group_var,
            values=self.item_product_group_mapping['item_product_group'].tolist(),
            state="readonly",
            width=30
        )
        self.product_group_dropdown.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.product_group_dropdown.bind('<<ComboboxSelected>>', self.update_dashboard)

        ttk.Label(controls_frame, text="Start Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_date_entry = DateEntry(controls_frame, width=30)
        self.start_date_entry.grid(row=3, column=0, sticky=tk.W, pady=5)

        ttk.Label(controls_frame, text="End Date:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.end_date_entry = DateEntry(controls_frame, width=30)
        self.end_date_entry.grid(row=5, column=0, sticky=tk.W, pady=5)

        ttk.Button(controls_frame, text="Update Dashboard", command=self.update_dashboard).grid(row=6, column=0, sticky=tk.W, pady=10)

    def create_dashboard(self, parent):
        dashboard_frame = ttk.Frame(parent, padding="10")
        dashboard_frame.grid(row=0, column=1, sticky=(tk.W, tk.N, tk.E, tk.S), columnspan=2)

        self.metrics_frame = ttk.Frame(dashboard_frame)
        self.metrics_frame.pack(fill=tk.X, pady=10)
        self.clicks_label = ttk.Label(self.metrics_frame, text="Total Clicks: -", font=("Arial", 12))
        self.clicks_label.pack(side=tk.LEFT, padx=10)
        self.impressions_label = ttk.Label(self.metrics_frame, text="Total Impressions: -", font=("Arial", 12))
        self.impressions_label.pack(side=tk.LEFT, padx=10)
        self.ctr_label = ttk.Label(self.metrics_frame, text="Avg CTR: -", font=("Arial", 12))
        self.ctr_label.pack(side=tk.LEFT, padx=10)
        self.notebook = ttk.Notebook(dashboard_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        self.create_page_performance_tab()


    def create_page_performance_tab(self):
        page_performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(page_performance_frame, text="Page Performance")

        self.page_performance_tree = ttk.Treeview(
            page_performance_frame,
            columns=("First Level", "Clicks", "Impressions", "CTR", "Position"),
            show="headings"
        )
        self.page_performance_tree.heading("First Level", text="First Level")
        self.page_performance_tree.heading("Clicks", text="Clicks")
        self.page_performance_tree.heading("Impressions", text="Impressions")
        self.page_performance_tree.heading("CTR", text="CTR (%)")
        self.page_performance_tree.heading("Position", text="Position")

        page_scrollbar = ttk.Scrollbar(page_performance_frame, orient=tk.VERTICAL, command=self.page_performance_tree.yview)
        self.page_performance_tree.configure(yscroll=page_scrollbar.set)

        self.page_performance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        page_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_dashboard(self, event=None):
        try:
            selected_group = self.product_group_var.get()
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()

            item_numbers = self.items_catalog[self.items_catalog['item_product_group'] == selected_group]['item_number'].tolist()
            filtered_pages = self.seo_pages[
                (self.seo_pages['Mon-Year'] >= pd.to_datetime(start_date)) &
                (self.seo_pages['Mon-Year'] <= pd.to_datetime(end_date))
            ]
            #(r'([^/]+)$')[0]
            if item_numbers:
                #filtered_pages = filtered_pages[filtered_pages['Page'].str.contains('|'.join(item_numbers))]
                filtered_pages.loc[:, 'First Level'] = filtered_pages['Page'].str.split('/').str[1]
                filtered_pages.loc[:,'Item Number']= filtered_pages['Page'].str.extract(r'([^/]+)$')[0]

                # if the first level is " " then remove
                filtered_pages = filtered_pages[filtered_pages['First Level'] != " "]

            self.update_metrics(filtered_pages)
            self.populate_page_performance_tree(filtered_pages)

        except Exception as e:
            messagebox.showerror("Update Error", f"An error occurred: {e}")

    def update_metrics(self, filtered_pages):

        #metrics on mean or sum
        total_clicks = filtered_pages['Clicks'].sum()
        total_impressions = filtered_pages['Impressions'].sum()
        avg_ctr = filtered_pages['CTR'].mean() * 100 if not filtered_pages.empty else 0

        self.clicks_label.config(text=f"Total Clicks: {total_clicks}")
        self.impressions_label.config(text=f"Total Impressions: {total_impressions}")
        self.ctr_label.config(text=f"Avg CTR: {avg_ctr:.2f}%")

    def populate_page_performance_tree(self, filtered_pages):
        for i in self.page_performance_tree.get_children():
            self.page_performance_tree.delete(i)

        page_performance = filtered_pages.groupby('First Level').agg({
            'Clicks': 'sum',
            'Impressions': 'sum',
            'CTR': 'mean',
            'Position': 'mean'
        }).sort_values('Clicks', ascending=False)
        #first 7
        page_performance = page_performance.head(7)

        for first_level, row in page_performance.iterrows():
            self.page_performance_tree.insert("", tk.END, values=(
                first_level, row['Clicks'], row['Impressions'], f"{row['CTR']*100:.2f}%", f"{row['Position']:.2f}"
            ))



def start_app():
    root = tk.Tk()
    app = SEOAnalysisDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    start_app()
