import pandas as pd
from datetime import timedelta

# Assuming 'df' is your DataFrame
df = pd.read_csv('Festive_Load.csv')

# Convert date columns to datetime format
df['manifestation_date'] = pd.to_datetime(df['manifestation_date'])
df['pickup_date'] = pd.to_datetime(df['pickup_date'])
df['first_ofd_date'] = pd.to_datetime(df['first_ofd_date'])
df['first_rto_date'] = pd.to_datetime(df['first_rto_date'])
df['latest_status_date'] = pd.to_datetime(df['latest_status_date'])

# # Function to calculate pickup performance, delivery TAT, and delivery percentage for each vendor
# def calculate_metrics(group_df):
#     # Pickup Performance
#     pickup_performance = group_df[group_df['pickup_date'] <= group_df['manifestation_date'] + timedelta(days=2)]
#     pickup_performance_percentage = len(pickup_performance) / len(group_df) * 100

#     # Delivery TAT
#     group_df['delivery_tat'] = group_df['latest_status_date'] - group_df['pickup_date']
#     average_delivery_tat = group_df['delivery_tat'].mean()

#     # Delivery Percentage (Successful Deliveries)
#     successful_deliveries = group_df[group_df['shipment_status'] == 'Delivered']
#     delivery_percentage = len(successful_deliveries) / len(group_df) * 100

#     return {
#         'Number of Orders': len(group_df),
#         'Pickup Performance Percentage': pickup_performance_percentage,
#         'Average Delivery TAT': average_delivery_tat,
#         'Delivery Percentage': delivery_percentage
#     }

# # Group by 'vendor' and calculate metrics for each group
# metrics_by_vendor = df.groupby('vendor').apply(calculate_metrics)

# # Display the calculated metrics for each vendor
# for vendor, metrics in metrics_by_vendor.items():
#     print(f'\nMetrics for Vendor: {vendor}')
#     for metric, value in metrics.items():
#         print(f'{metric}: {value}')

pickup_performance = df[df['pickup_date'] <= df['manifestation_date'] + timedelta(days=2)]
pickup_performance_percentage = len(pickup_performance) / len(df) * 100

# Delivery TAT
df['delivery_tat'] = df['latest_status_date'] - df['pickup_date']
average_delivery_tat = df['delivery_tat'].mean()

# Delivery Percentage (Successful Deliveries)
successful_deliveries = df[df['shipment_status'] == 'Delivered']
delivery_percentage = len(successful_deliveries) / len(df) * 100

# Display the calculated metrics for the entire dataset
print(f'Number of Orders: {len(df)}')
print(f'Pickup Performance Percentage: {pickup_performance_percentage:.2f}%')
print(f'Average Delivery TAT: {average_delivery_tat}')
print(f'Delivery Percentage: {delivery_percentage:.2f}%')