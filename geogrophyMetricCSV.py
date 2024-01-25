import pandas as pd
from datetime import timedelta

# Assuming 'df' is your DataFrame
df = pd.read_csv('BAU_Load.csv')

# Convert date columns to datetime format
df['manifestation_date'] = pd.to_datetime(df['manifestation_date'])
df['pickup_date'] = pd.to_datetime(df['pickup_date'])
df['first_ofd_date'] = pd.to_datetime(df['first_ofd_date'])
df['first_rto_date'] = pd.to_datetime(df['first_rto_date'])
df['latest_status_date'] = pd.to_datetime(df['latest_status_date'])

# Function to calculate pickup performance, delivery TAT, and delivery percentage for each vendor
def calculate_metrics(group_df):
    # Pickup Performance
    pickup_performance = group_df[group_df['pickup_date'] <= group_df['manifestation_date'] + timedelta(days=2)]
    pickup_performance_percentage = len(pickup_performance) / len(group_df) * 100

    # Delivery TAT
    group_df['delivery_tat'] = group_df['latest_status_date'] - group_df['pickup_date']
    average_delivery_tat = group_df['delivery_tat'].mean()

    # Delivery Percentage (Successful Deliveries)
    unsuccessful_deliveries = group_df[group_df['shipment_status'] == 'RTO Delivered']
    return_percentage = len(unsuccessful_deliveries) / len(group_df) * 100

    return {
        'Number of Orders': len(group_df),
        'Pickup Performance Percentage': pickup_performance_percentage,
        'Average Delivery TAT': average_delivery_tat,
        'Return Percentage': return_percentage
    }

# Group by 'geography' and 'vendor' and calculate metrics for each group
metrics_by_geography_and_vendor = df.groupby(['pickup_state', 'vendor']).apply(calculate_metrics)

# Create a DataFrame from the calculated metrics
result_df = pd.DataFrame(metrics_by_geography_and_vendor.tolist(), index=metrics_by_geography_and_vendor.index)

# Save the DataFrame to a CSV file
result_df.to_csv('calculated_metrics.csv')
