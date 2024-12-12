import pandas as pd
import re
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

#https://docs.python.org/3/library/tk.html
def extract_product_id(row):
    # check "" marks
    if row.strip().startswith('"'):
        return None
    
    # Product: or Item Number:
    product_match = re.search(r'(?:Product:|Item Number:)\s*([\w-]+)', row, re.IGNORECASE)
    if product_match:
        return product_match.group(1)
    # take the first word
    first_word_match = re.match(r'[\w-]+', row.strip())
    if first_word_match:
        return first_word_match.group(0)
    return None

def process_files():
    item_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not item_file_path:
        return
    product_request_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not product_request_file_path:
        return

    try:
        product_data = pd.read_excel(product_request_file_path)
        items = pd.read_excel(item_file_path)


        product_data['Product ID'] = product_data['Products Requested'].apply(extract_product_id)
        cleaned_product_data = cleaned_product_data[~cleaned_product_data['Product ID'].isin(['-'])]
        #if none then remove the data
        #cleaned_product_data = product_data.dropna(subset=['Product ID'])

        #counting occurence of different product in product
        product_counts = cleaned_product_data['Product ID'].value_counts().reset_index()
        product_counts.columns = ['Product ID', 'Count']
        

        valid_ids = set(items['item_number'])
        cleaned_product_counts = product_counts[
            (product_counts['Product ID'].isin(valid_ids)) | (product_counts['Count'] > 7)
        ]

        #csv and database files
        #cleaned_csv_path = 'cleaned_product_counts.csv'
        #cleaned_product_counts.to_csv(cleaned_csv_path, index=False)
        #db_path = 'mydb.db'
        #conn = sqlite3.connect(db_path)
        #cleaned_product_counts.to_sql('cleaned_product_counts', conn, if_exists='replace', index=False)
        # conn.commit()
        # conn.close()

        #top 10 bar chart data
        top_10_products = cleaned_product_counts.nlargest(10, 'Count')
        plt.figure(figsize=(10, 6))
        plt.bar(top_10_products['Product ID'], top_10_products['Count'], color='skyblue', edgecolor='black')
        plt.title('Top 10 Products by Lead', fontsize=14)
        plt.xlabel('Product ID', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()
        plt.show()
        messagebox.showinfo("Success", "Done")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")