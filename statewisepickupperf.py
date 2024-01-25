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

# Function to calculate pickup performance for each state
def calculate_metrics(group_df):
    # Pickup Performance
    pickup_performance = group_df[group_df['pickup_date'] <= group_df['manifestation_date'] + timedelta(days=2)]
    pickup_performance_percentage = len(pickup_performance) / len(group_df) * 100

    return {
        'State': group_df['pickup_state'].iloc[0],  # Get the state name from the first row
        'Number of Orders': len(group_df),
        'Pickup Performance Percentage': pickup_performance_percentage,
    }

# Group by 'pickup_state' and calculate metrics for each group
metrics_by_state = df.groupby('pickup_state').apply(calculate_metrics)

# Create a DataFrame from the calculated metrics
result_df = pd.DataFrame(metrics_by_state.tolist())

# Save the results to a CSV file
result_df.to_csv('statewise_pickup_performance.csv', index=False)
