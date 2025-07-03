
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

def main():
    print("=== Sales Data Analysis by Order Mode ===\n")
    
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
            print("\n=== Key Insights ===")
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

if __name__ == "__main__":
    main()
