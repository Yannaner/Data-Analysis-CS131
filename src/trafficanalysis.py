import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        data['Mon-Year'] = pd.to_datetime(data['Mon-Year'], format='%b-%Y')
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    

def perform_analysis(data):
    if data is None:
        print("No data, please upload data")
        return

    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Traffic Analysis Overview", fontsize=16, fontweight='bold')
    descriptive_stats = data[['Items viewed', 'Items added to cart', 'Items purchased']].describe()
    axs[0, 0].axis('off')
    axs[0, 0].table(cellText=descriptive_stats.values, colLabels=descriptive_stats.columns, loc='center', cellLoc='center', colColours=["#D3D3D3"]*descriptive_stats.shape[1])
    axs[0, 0].set_title('Descriptive Statistics', fontsize=18, fontweight='bold')

    product_performance_plot(data, axs[0, 1])
    trend_analysis(data, axs[1, 0])
    revenue_prediction(data, axs[1, 1])
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def product_performance_plot(data, ax):
    product_data = data.groupby('Item name')[['Items added to cart', 'Items purchased']].sum()
    top_products = product_data.sort_values(by='Items purchased', ascending=False).head(10)

    # top 10
    top_products[['Items added to cart', 'Items purchased']].plot(kind='bar', ax=ax, stacked=False)
    ax.set_title('Top 10 Products by Items Added and Purchased')
    ax.set_ylabel('Count')

    #make the tag into horizontal for a better visual
    ax.set_xticklabels(top_products.index, rotation=45, ha="right") 
    ax.legend(["Items Added to Cart", "Items Purchased"])

def trend_analysis(data, ax):
    monthly_data = data.groupby(data['Mon-Year'].dt.to_period('M'))[['Items added to cart', 'Items purchased']].sum()
    monthly_data.plot(ax=ax)
    ax.set_title('Monthly Trends in Adds to Cart and Purchases')
    ax.set_ylabel('Count')

def revenue_prediction(data, ax):
    features = ['Items viewed', 'Items added to cart', 'Items purchased']
    target = 'Item revenue'
    data['Month'] = data['Mon-Year'].dt.month  
    data = data.sort_values('Month') 
    #use the previous 10 month to predict the last two month
    #no 11 & 12 input so unable to predict these two months
    data_10_months = data[data['Month'] <= 10] 


    #code using sckit learn linearmodel
    #currently not working
    #====================================
    X = data_10_months[['Month'] + features]
    y = data_10_months[target]
    model = LinearRegression()
    model.fit(X, y)
    future_months = np.array([[11], [12]])
    future_features = np.tile(data_10_months[features].mean().values, (2, 1))
    X_future = np.hstack((future_months, future_features))
    predicted_revenue = model.predict(X_future)
    monthly_revenue_10_months = data_10_months.groupby('Month')[target].sum()
    ax.plot(monthly_revenue_10_months.index, monthly_revenue_10_months, label='Actual Revenue', color='blue')
    ax.plot([11, 12], predicted_revenue, label='Predicted Revenue', color='red', marker='o')
    ax.set_title('Revenue Prediction for Months 11 and 12')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    ax.legend()
    #====================================
