# Data Analysis Project - README

This project contains several Python scripts designed for analyzing and visualizing data related to SEO queries, traffic metrics, and lead analysis.

## Project Structure:

- **main.py**: This is the entry point for the project. It creates the main UI window using Tkinter, where users can select different analysis tools, such as Lead Visualization, Traffic Visualization, and SEO Analysis.

- **data_correlation.py**: This script performs advanced data analysis by loading various data sources (SEO queries, traffic data, leads data) and computes correlations between them. It includes functions for:
  - Loading data sources.
  - Creating composite keys for data merging.
  - Performing Principal Component Analysis (PCA) and Linear Regression.
  - Visualizing correlations and generating a comprehensive report.

- **leadanalysis.py**: This script processes product and product request data to count the occurrences of products in requests. It filters valid product IDs and generates a bar chart of the top 10 products based on lead count.

- **seodashboard.py**: This script creates an interactive dashboard to analyze SEO data. It allows users to filter SEO queries and pages based on product group and date range, visualizing key metrics like clicks, impressions, CTR, and position.

- **seoqueriesanalysis.py**: This script processes SEO queries data from an uploaded Excel file. It performs trend analysis, displays top-performing queries, visualizes the relationship between CTR and position, and identifies seasonal trends.

- **trafficdashboard.py**: This script merges traffic data with item catalogs and cleaned product data. It provides a dashboard to select products and view metrics like total purchasers, items purchased, and item revenue. The data is dynamically updated when a product is selected.

- **trafficanalysis.py**: This script loads traffic data and performs various analyses, including:
  - Product performance visualization by items added to the cart and purchased.
  - Trend analysis of monthly adds to cart and purchases.
  - Revenue prediction using Linear Regression for future months.

- **requirements.txt**: Lists the necessary Python libraries for the project, including:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `sklearn`
  - `tkinter`

## How to Run:

1. Install the required libraries:
   - pip install -r requirements.txt

2. Run the `main.py` script to launch the main application:
   - python main.py

3. The application will display buttons to access various analysis tools. Select the analysis you want to run, such as Lead Visualization, SEO Analysis, or Traffic Visualization.

## Data Files:

The following data files are required for the scripts:
- **SEO Queries**: `seo_queries.xlsx`
- **SEO Pages**: `seo_pages.xlsx`
- **Items Catalog**: `items_catalog.xlsx`
- **Traffic Data**: `traffic.xlsx`
- **Product Counts**: `cleaned_product_counts.csv`

Make sure these files are available in the correct format for proper functionality.
