
import pandas as pd
import numpy as np

def load_sales_data():
    """Load sales data with proper encoding handling"""
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv('attached_assets/Ace Superstore Retail Dataset(in)_1751579681236.csv', 
                               encoding=encoding)
                print(f"Successfully loaded sales data with {encoding} encoding")
                return df
            except UnicodeDecodeError:
                continue
        
        print("Could not load data with any encoding")
        return None
        
    except FileNotFoundError:
        print("Sales data file not found")
        return None

def summarize_by_order_mode(df):
    """Create comprehensive summary by Order Mode"""
    
    if df is None:
        print("No data to analyze")
        return None
    
    # Group by Order Mode
    order_mode_summary = df.groupby('Order Mode').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'Cost Price': 'sum',
        'Discount': 'mean'
    }).round(2)
    
    # Flatten column names
    order_mode_summary.columns = ['Total_Sales', 'Avg_Sales', 'Order_Count', 
                                 'Total_Quantity', 'Total_Cost', 'Avg_Discount']
    
    # Calculate additional metrics
    order_mode_summary['Profit'] = order_mode_summary['Total_Sales'] - order_mode_summary['Total_Cost']
    order_mode_summary['Profit_Margin'] = (order_mode_summary['Profit'] / order_mode_summary['Total_Sales'] * 100).round(2)
    order_mode_summary['Sales_Percentage'] = (order_mode_summary['Total_Sales'] / order_mode_summary['Total_Sales'].sum() * 100).round(2)
    
    return order_mode_summary

def analyze_product_performance(df):
    """Analyze product performance by revenue"""
    
    if df is None:
        print("No data to analyze")
        return None, None
    
    # Group by Product Name and calculate metrics
    product_analysis = df.groupby('Product Name').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'Cost Price': 'sum',
        'Discount': 'mean'
    }).round(2)
    
    # Flatten column names
    product_analysis.columns = ['Total_Revenue', 'Avg_Revenue_Per_Sale', 'Total_Orders', 
                               'Total_Quantity_Sold', 'Total_Cost', 'Avg_Discount']
    
    # Calculate additional metrics
    product_analysis['Profit'] = product_analysis['Total_Revenue'] - product_analysis['Total_Cost']
    product_analysis['Profit_Margin'] = (product_analysis['Profit'] / product_analysis['Total_Revenue'] * 100).round(2)
    product_analysis['Revenue_Percentage'] = (product_analysis['Total_Revenue'] / product_analysis['Total_Revenue'].sum() * 100).round(2)
    
    # Sort by revenue
    product_analysis = product_analysis.sort_values('Total_Revenue', ascending=False)
    
    # Get top 5 and bottom 5
    top_5_products = product_analysis.head(5)
    bottom_5_products = product_analysis.tail(5)
    
    return top_5_products, bottom_5_products

def main():
    print("=== Sales Data Analysis ===\n")
    
    # Load sales data
    print("Loading sales data...")
    sales_df = load_sales_data()
    
    if sales_df is not None:
        print(f"Sales data loaded: {len(sales_df)} records")
        print(f"Columns available: {sales_df.columns.tolist()}\n")
        
        # Summarize by Order Mode
        print("=== Order Mode Analysis ===")
        order_mode_summary = summarize_by_order_mode(sales_df)
        
        if order_mode_summary is not None:
            print("\nDetailed Summary by Order Mode:")
            print(order_mode_summary)
            
            # Save to CSV
            order_mode_summary.to_csv('order_mode_detailed_summary.csv')
            print(f"\nDetailed summary saved to 'order_mode_detailed_summary.csv'")
            
            # Print key insights
            print("\n=== Order Mode Key Insights ===")
            total_sales = order_mode_summary['Total_Sales'].sum()
            print(f"Total Sales: ${total_sales:,.2f}")
            
            for mode in order_mode_summary.index:
                sales = order_mode_summary.loc[mode, 'Total_Sales']
                percentage = order_mode_summary.loc[mode, 'Sales_Percentage']
                orders = order_mode_summary.loc[mode, 'Order_Count']
                avg_order = order_mode_summary.loc[mode, 'Avg_Sales']
                profit_margin = order_mode_summary.loc[mode, 'Profit_Margin']
                
                print(f"\n{mode}:")
                print(f"  - Sales: ${sales:,.2f} ({percentage}%)")
                print(f"  - Orders: {orders:,}")
                print(f"  - Avg Order Value: ${avg_order:,.2f}")
                print(f"  - Profit Margin: {profit_margin}%")
        
        # Product Performance Analysis
        print("\n" + "="*60)
        print("=== PRODUCT PERFORMANCE ANALYSIS BY REVENUE ===")
        print("="*60)
        
        top_5, bottom_5 = analyze_product_performance(sales_df)
        
        if top_5 is not None and bottom_5 is not None:
            
            # Top 5 Best-Selling Products
            print("\n🏆 TOP 5 BEST-SELLING PRODUCTS BY REVENUE:")
            print("-" * 50)
            for i, (product, data) in enumerate(top_5.iterrows(), 1):
                print(f"{i}. {product}")
                print(f"   Revenue: ${data['Total_Revenue']:,.2f} ({data['Revenue_Percentage']:.2f}% of total)")
                print(f"   Orders: {data['Total_Orders']:,} | Quantity Sold: {data['Total_Quantity_Sold']:,}")
                print(f"   Avg Revenue/Sale: ${data['Avg_Revenue_Per_Sale']:,.2f}")
                print(f"   Profit Margin: {data['Profit_Margin']:.2f}%")
                print()
            
            # Bottom 5 Underperforming Products
            print("📉 TOP 5 UNDERPERFORMING PRODUCTS BY REVENUE:")
            print("-" * 50)
            for i, (product, data) in enumerate(bottom_5.iterrows(), 1):
                print(f"{i}. {product}")
                print(f"   Revenue: ${data['Total_Revenue']:,.2f} ({data['Revenue_Percentage']:.2f}% of total)")
                print(f"   Orders: {data['Total_Orders']:,} | Quantity Sold: {data['Total_Quantity_Sold']:,}")
                print(f"   Avg Revenue/Sale: ${data['Avg_Revenue_Per_Sale']:,.2f}")
                print(f"   Profit Margin: {data['Profit_Margin']:.2f}%")
                print()
            
            # Save detailed product analysis
            full_product_analysis = analyze_product_performance(sales_df)[0].reset_index()
            if len(analyze_product_performance(sales_df)[1]) > 0:
                full_analysis = pd.concat([
                    analyze_product_performance(sales_df)[0], 
                    analyze_product_performance(sales_df)[1]
                ]).sort_values('Total_Revenue', ascending=False)
                full_analysis.to_csv('product_performance_analysis.csv')
                print(f"📊 Complete product performance analysis saved to 'product_performance_analysis.csv'")
            
            # Summary Statistics
            print("\n=== PRODUCT PERFORMANCE SUMMARY ===")
            total_products = len(sales_df['Product Name'].unique())
            top_5_revenue = top_5['Total_Revenue'].sum()
            total_revenue = sales_df['Sales'].sum()
            top_5_percentage = (top_5_revenue / total_revenue) * 100
            
            print(f"Total Products Analyzed: {total_products}")
            print(f"Top 5 Products Revenue: ${top_5_revenue:,.2f} ({top_5_percentage:.1f}% of total sales)")
            print(f"Best Performing Product: {top_5.index[0]} (${top_5.iloc[0]['Total_Revenue']:,.2f})")
            print(f"Least Performing Product: {bottom_5.index[-1]} (${bottom_5.iloc[-1]['Total_Revenue']:,.2f})")
            
            revenue_gap = top_5.iloc[0]['Total_Revenue'] - bottom_5.iloc[-1]['Total_Revenue']
            print(f"Revenue Gap (Best vs Worst): ${revenue_gap:,.2f}")
    else:
        print("Failed to load sales data. Please check the file path and encoding.")

if __name__ == "__main__":
    main()
