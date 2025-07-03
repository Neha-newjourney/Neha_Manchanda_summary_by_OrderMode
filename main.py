
import pandas as pd
import os

def load_store_locations():
    """Load store locations data"""
    try:
        store_locations = pd.read_csv('attached_assets/Store Locations(Store Locations)_1751578741135.csv')
        return store_locations
    except Exception as e:
        print(f"Error loading store locations: {e}")
        return None

def load_sales_data():
    """Load sales data with proper encoding handling"""
    try:
        # Try different encodings for the sales data file
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                sales_data = pd.read_csv('attached_assets/Ace Superstore Retail Dataset(in)_1751578741136.csv', 
                                       encoding=encoding)
                print(f"Successfully loaded sales data with {encoding} encoding")
                return sales_data
            except UnicodeDecodeError:
                continue
                
        print("Could not load sales data with any encoding")
        return None
    except Exception as e:
        print(f"Error loading sales data: {e}")
        return None

def analyze_sales_by_region_segment(sales_data, store_locations):
    """Analyze sales data by region and segment"""
    
    # If sales data has city information, merge with store locations to get regions
    if 'City' in sales_data.columns:
        # Merge sales data with store locations to get region information
        merged_data = pd.merge(sales_data, store_locations, on='City', how='left')
    else:
        # If no city column, assume Region is already in sales data
        merged_data = sales_data.copy()
    
    # Check for required columns
    required_cols = ['Sales', 'Profit', 'Discount']
    segment_col = 'Segment' if 'Segment' in merged_data.columns else 'Customer Segment'
    region_col = 'Region'
    
    if not all(col in merged_data.columns for col in required_cols):
        print("Missing required columns for analysis")
        print("Available columns:", merged_data.columns.tolist())
        return None
    
    # Group by Region and Segment
    summary = merged_data.groupby([region_col, segment_col]).agg({
        'Sales': ['sum', 'mean', 'count'],
        'Profit': ['sum', 'mean'],
        'Discount': ['mean', 'sum']
    }).round(2)
    
    # Flatten column names
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    
    # Calculate additional metrics
    summary['Revenue'] = summary['Sales_sum']
    summary['Avg_Discount_Rate'] = summary['Discount_mean']
    summary['Total_Discount_Amount'] = summary['Discount_sum']
    
    return summary

def create_regional_summary(summary_data):
    """Create regional summary from detailed data"""
    if summary_data is None:
        return None
    
    # Reset index to work with region and segment as columns
    df = summary_data.reset_index()
    
    # Group by region only
    regional_summary = df.groupby('Region').agg({
        'Sales_sum': 'sum',
        'Profit_sum': 'sum',
        'Discount_mean': 'mean',
        'Sales_count': 'sum'
    }).round(2)
    
    regional_summary.columns = ['Total_Sales', 'Total_Profit', 'Avg_Discount_Rate', 'Total_Orders']
    
    return regional_summary

def summarize_sales_by_order_mode(sales_data):
    """Summarize total sales by Order Mode"""
    if sales_data is None:
        return None
    
    if 'Order Mode' not in sales_data.columns or 'Sales' not in sales_data.columns:
        print("Missing required columns: 'Order Mode' or 'Sales'")
        return None
    
    # Group by Order Mode and calculate summary statistics
    order_mode_summary = sales_data.groupby('Order Mode').agg({
        'Sales': ['sum', 'mean', 'count'],
        'Quantity': 'sum',
        'Discount': 'mean'
    }).round(2)
    
    # Flatten column names
    order_mode_summary.columns = ['_'.join(col).strip() for col in order_mode_summary.columns.values]
    
    # Rename columns for clarity
    order_mode_summary = order_mode_summary.rename(columns={
        'Sales_sum': 'Total_Sales',
        'Sales_mean': 'Average_Sales_Per_Order',
        'Sales_count': 'Number_of_Orders',
        'Quantity_sum': 'Total_Quantity',
        'Discount_mean': 'Average_Discount_Rate'
    })
    
    # Calculate percentage of total sales
    total_sales = order_mode_summary['Total_Sales'].sum()
    order_mode_summary['Sales_Percentage'] = (order_mode_summary['Total_Sales'] / total_sales * 100).round(2)
    
    return order_mode_summary

def main():
    print("=== Sales Data Analysis by Region and Segment ===\n")
    
    # Load data
    print("Loading store locations...")
    store_locations = load_store_locations()
    if store_locations is not None:
        print(f"Store locations loaded: {len(store_locations)} records")
        print("Regions available:", store_locations['Region'].unique())
    
    print("\nLoading sales data...")
    sales_data = load_sales_data()
    
    if sales_data is not None:
        print(f"Sales data loaded: {len(sales_data)} records")
        print("Columns available:", sales_data.columns.tolist())
        
        # Analyze data
        print("\n=== Analysis Results ===")
        
        # 1. Sales Summary by Order Mode
        print("\n1. Sales Summary by Order Mode:")
        order_mode_summary = summarize_sales_by_order_mode(sales_data)
        if order_mode_summary is not None:
            print(order_mode_summary)
            order_mode_summary.to_csv('sales_summary_by_order_mode.csv')
            print("Order Mode summary saved to 'sales_summary_by_order_mode.csv'")
        
        # 2. Regional analysis (if store locations available)
        if store_locations is not None:
            summary = analyze_sales_by_region_segment(sales_data, store_locations)
            
            if summary is not None:
                print("\n2. Sales Summary by Region and Segment:")
                print(summary)
                
                print("\n3. Regional Summary:")
                regional_summary = create_regional_summary(summary)
                if regional_summary is not None:
                    print(regional_summary)
                
                # Save results to CSV
                summary.to_csv('sales_summary_by_region_segment.csv')
                if regional_summary is not None:
                    regional_summary.to_csv('regional_summary.csv')
                print("\nRegional analysis results saved to CSV files")
            else:
                print("Could not perform regional analysis due to missing columns")
        else:
            print("Cannot perform regional analysis without store locations data")
    else:
        print("Cannot perform analysis without sales data")
        
        # Show sample analysis structure with store locations only
        if store_locations is not None:
            print("\nStore Locations Summary:")
            region_counts = store_locations['Region'].value_counts()
            print(region_counts)

if __name__ == "__main__":
    main()
