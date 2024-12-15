import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# File Paths
TRAFFIC_FILE = 'traffic.xlsx'
ITEM_CATALOG_FILE = 'items_catalog.xlsx'
CLEANED_PRODUCT_COUNTS = 'cleaned_product_counts.csv'

# Load Data
try:
    traffic_df = pd.read_excel(TRAFFIC_FILE)
    items_catalog_df = pd.read_excel(ITEM_CATALOG_FILE)
    product_counts_df = pd.read_csv(CLEANED_PRODUCT_COUNTS)
except Exception as e:
    print(f"Error loading files: {e}")
    exit()


traffic_df.columns = traffic_df.columns.str.strip().str.lower().str.replace(' ', '_')
items_catalog_df.columns = items_catalog_df.columns.str.strip().str.lower().str.replace(' ', '_')
product_counts_df.columns = product_counts_df.columns.str.strip().str.lower().str.replace(' ', '_')


def clean_product_names(products):
    return products.str.replace(r'[\(\),:]', '', regex=True).str.strip()

traffic_df['item_name'] = clean_product_names(traffic_df['item_name'])
items_catalog_df['item_number'] = clean_product_names(items_catalog_df['item_number'])
product_counts_df['product_id'] = clean_product_names(product_counts_df['product_id'])


def prepare_data():

    traffic_items = traffic_df.merge(items_catalog_df, how='inner', left_on='item_name', right_on='item_number')
    full_data = traffic_items.merge(product_counts_df, how='inner', left_on='item_name', right_on='product_id')

    return full_data


def filter_valid_products(full_data):
    valid_products = full_data[(full_data['total_purchasers'] > 0) |
                               (full_data['items_purchased'] > 0) |
                               (full_data['items_added_to_cart'] > 0) |
                               (full_data['items_viewed'] > 0)]
    return valid_products['item_name'].unique()


full_data = prepare_data()
product_list = filter_valid_products(full_data)

def create_dashboard():
    def update_dashboard():
     
        selected_product = product_dropdown.get()
        if not selected_product:
            messagebox.showerror("Error", "Please select a product")
            return

        filtered_data = full_data[full_data['item_name'] == selected_product]
        if filtered_data.empty:
            messagebox.showinfo("No Data", "No data available for the selected product")
            return

        total_purchasers = filtered_data['total_purchasers'].sum()
        items_purchased = filtered_data['items_purchased'].sum()
        items_added_cart = filtered_data['items_added_to_cart'].sum()
        items_viewed = filtered_data['items_viewed'].sum()
        item_revenue = filtered_data['item_revenue'].sum()
        total_purchasers_label.config(text=f"Total Purchasers: {total_purchasers}")
        items_purchased_label.config(text=f"Items Purchased: {items_purchased}")
        items_added_cart_label.config(text=f"Items Added to Cart: {items_added_cart}")
        items_viewed_label.config(text=f"Items Viewed: {items_viewed}")
        item_revenue_label.config(text=f"Item Revenue: {item_revenue:.2f}")


    root = tk.Tk()
    root.title("Traffic Analysis Dashboard")
    root.geometry("800x600")


    ttk.Label(root, text="Select Product Group:").grid(row=0, column=0, padx=10, pady=10)
    product_dropdown = ttk.Combobox(root, values=product_list, state='readonly', height=10)
    product_dropdown.grid(row=0, column=1, padx=10, pady=10)


    update_button = ttk.Button(root, text="Update Dashboard", command=update_dashboard)
    update_button.grid(row=0, column=2, padx=10, pady=10)
    total_purchasers_label = ttk.Label(root, text="Total Purchasers: -")
    total_purchasers_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    items_purchased_label = ttk.Label(root, text="Items Purchased: -")
    items_purchased_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    items_added_cart_label = ttk.Label(root, text="Items Added to Cart: -")
    items_added_cart_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    items_viewed_label = ttk.Label(root, text="Items Viewed: -")
    items_viewed_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    item_revenue_label = ttk.Label(root, text="Item Revenue: -")
    item_revenue_label.grid(row=5, column=0, padx=10, pady=10, sticky='w')

    root.mainloop()

if __name__ == "__main__":
    create_dashboard()
