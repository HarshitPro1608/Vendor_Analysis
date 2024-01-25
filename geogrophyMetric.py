import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Assuming 'df' is your DataFrame
df = pd.read_csv('Festive_Load.csv')

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

    return {
        'Number of Orders': len(group_df),
        'Pickup Performance Percentage': pickup_performance_percentage,
    }

# Group by 'pickup_state' and 'vendor' and calculate metrics for each group
metrics_by_geography_and_vendor = df.groupby(['pickup_state', 'vendor']).apply(calculate_metrics)

# Create a DataFrame from the calculated metrics
result_df = pd.DataFrame(metrics_by_geography_and_vendor.tolist(), index=metrics_by_geography_and_vendor.index)

# Filter out vendors with 0 orders
result_df = result_df[result_df['Number of Orders'] > 0]

# Find the vendor with maximum pickup performance for each state
max_performance_vendors = result_df.groupby('pickup_state')['Pickup Performance Percentage'].idxmax()
result_df_max_performance = result_df.loc[max_performance_vendors]

# Pivot the DataFrame for plotting
result_pivot = result_df_max_performance.pivot_table(index='pickup_state', columns='vendor', values='Pickup Performance Percentage', aggfunc='first')

# Plotting
ax = result_pivot.plot(kind='bar', figsize=(12, 6), stacked=True, title='Max Pickup Performance Vendor by Pickup State')
plt.xlabel('Pickup State')
plt.ylabel('Pickup Performance Percentage')
plt.legend(title='Vendor', bbox_to_anchor=(1.05, 1), loc='upper left')

# Set numerical index for the x-axis and set the state labels manually
ax.set_xticks(range(len(result_pivot.index)))
ax.set_xticklabels(result_pivot.index, rotation=45, ha='right')

# Annotate each bar with its Pickup Performance Percentage value
for state in result_pivot.index:
    for vendor in result_pivot.columns:
        value = result_pivot.loc[state, vendor]
        if not pd.isna(value):  # Skip NaN values
            ax.annotate(f"{value:.2f}%", (result_pivot.index.get_loc(state), value),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points', color='black')

plt.show()
