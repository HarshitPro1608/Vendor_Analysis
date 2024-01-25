import pandas as pd

# Sample metrics data for vendors
vendor_metrics = {
    'XPRESSBEES_INTERCITY': {'Number of Orders': 167, 'Pickup Performance Percentage': 82.04, 'Average Delivery TAT': '3 days 14:32:06.760563380', 'Delivery Percentage': 79.64},
    'XPRESSBEES_NDD': {'Number of Orders': 1397, 'Pickup Performance Percentage': 91.98, 'Average Delivery TAT': '2 days 19:33:53.383010432', 'Delivery Percentage': 82.75},
    'AMAZON': {'Number of Orders': 923, 'Pickup Performance Percentage': 91.87, 'Average Delivery TAT': '5 days 16:52:17.614678899', 'Delivery Percentage': 73.24},
    'BLUEDART': {'Number of Orders': 28746, 'Pickup Performance Percentage': 88.96, 'Average Delivery TAT': '4 days 14:18:40.852648100', 'Delivery Percentage': 83.65},
    'BLUEDART_B2B': {'Number of Orders': 222, 'Pickup Performance Percentage': 68.47, 'Average Delivery TAT': '2 days 01:05:52.941176470', 'Delivery Percentage': 67.12},
    'DELHIVERY': {'Number of Orders': 14573, 'Pickup Performance Percentage': 82.30, 'Average Delivery TAT': '5 days 14:13:15.533845080', 'Delivery Percentage': 75.78},
    'DELHIVERY_B2B': {'Number of Orders': 34, 'Pickup Performance Percentage': 73.53, 'Average Delivery TAT': '4 days 22:04:48', 'Delivery Percentage': 73.53},
    'DTDC': {'Number of Orders': 1657, 'Pickup Performance Percentage': 82.44, 'Average Delivery TAT': '5 days 16:30:07.531380753', 'Delivery Percentage': 78.09},
    'ECOM': {'Number of Orders': 6760, 'Pickup Performance Percentage': 92.46, 'Average Delivery TAT': '7 days 21:53:47.469426152', 'Delivery Percentage': 73.03},
    'EKART': {'Number of Orders': 4090, 'Pickup Performance Percentage': 92.79, 'Average Delivery TAT': '5 days 03:03:58.875878220', 'Delivery Percentage': 75.31},
    'SMARTR': {'Number of Orders': 23448, 'Pickup Performance Percentage': 80.68, 'Average Delivery TAT': '4 days 11:34:19.061738222', 'Delivery Percentage': 69.82},
    'SMARTR_B2B': {'Number of Orders': 78, 'Pickup Performance Percentage': 32.05, 'Average Delivery TAT': '5 days 06:43:12', 'Delivery Percentage': 32.05},
    'XPRESSBEES': {'Number of Orders': 17905, 'Pickup Performance Percentage': 86.52, 'Average Delivery TAT': '8 days 05:48:36.094986807', 'Delivery Percentage': 69.56}
}

# Convert average delivery TAT to timedelta
for vendor, metrics in vendor_metrics.items():
    metrics['Average Delivery TAT'] = pd.to_timedelta(metrics['Average Delivery TAT'])  

# Find the maximum 'Average Delivery TAT' across all vendors
max_delivery_tat_seconds = max(metrics['Average Delivery TAT'].total_seconds() for metrics in vendor_metrics.values())

# Define weights for optimization criteria
pickup_weight = 0
delivery_weight = 1
tat_weight = 0

# Calculate a score for each vendor based on the defined weights
for vendor, metrics in vendor_metrics.items():
    metrics['Score'] = (
        (metrics['Pickup Performance Percentage']/100) * pickup_weight +
        (metrics['Delivery Percentage']/100) * delivery_weight -
        (metrics['Average Delivery TAT'].total_seconds()/max_delivery_tat_seconds) * tat_weight
    )

# Calculate redistributed orders without explicit sorting
total_orders = 100000
redistributed_orders = {}
remaining_orders = total_orders

# Initialize a list of vendors and their scores
vendors_and_scores = list(vendor_metrics.items())

while remaining_orders > 0 and vendors_and_scores:
    # Select the vendor with the highest score
    current_vendor, metrics = max(vendors_and_scores, key=lambda x: x[1]['Score'])

    # Calculate orders to redistribute for the current vendor
    orders_to_redistribute = int(metrics['Number of Orders'] / total_orders * total_orders)

    # Distribute orders to the vendor
    redistributed_orders[current_vendor] = redistributed_orders.get(current_vendor, 0) + orders_to_redistribute
    vendors_and_scores.remove((current_vendor, metrics))

    # Update remaining orders
    remaining_orders -= orders_to_redistribute

# Display the optimized distribution of orders
for vendor, orders in redistributed_orders.items():
    print(f"{vendor}: {orders} orders")



# # Display the redistributed orders
# for vendor, orders in redistributed_orders.items():
#     print(f'{vendor}: {orders} orders')

# Calculate overall metrics after redistribution
total_orders_after_redistribution = sum(redistributed_orders.values())

# Calculate overall pickup performance percentage, average delivery TAT, and delivery percentage
overall_pickup_performance = sum(metrics['Pickup Performance Percentage'] * redistributed_orders[vendor] for vendor, metrics in vendor_metrics.items()) / total_orders_after_redistribution
overall_average_delivery_tat = sum(metrics['Average Delivery TAT'].total_seconds() * redistributed_orders[vendor] for vendor, metrics in vendor_metrics.items()) / total_orders_after_redistribution
overall_delivery_percentage = sum(metrics['Delivery Percentage'] * redistributed_orders[vendor] for vendor, metrics in vendor_metrics.items()) / total_orders_after_redistribution

overall_metrics = {
    'Number of Orders': total_orders_after_redistribution,
    'Pickup Performance Percentage': overall_pickup_performance,
    'Average Delivery TAT': pd.to_timedelta(overall_average_delivery_tat),
    'Delivery Percentage': overall_delivery_percentage
}

# Display the overall metrics after redistribution
print("\nOverall Metrics After Redistribution:")
print(f"Number of Orders: {overall_metrics['Number of Orders']}")
print(f"Pickup Performance Percentage: {overall_metrics['Pickup Performance Percentage']:.2f}%")
print(f"Average Delivery TAT: {overall_metrics['Average Delivery TAT']}")
print(f"Delivery Percentage: {overall_metrics['Delivery Percentage']:.2f}%")