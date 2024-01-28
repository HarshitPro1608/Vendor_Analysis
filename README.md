# Vendor_Analysis
There are 2 datasets given having information of couriers delivered by various delivery partner/vendors and the task is to infer insights from the datasets to see the shift in performance from normal to festive season.

# How to measure Performance

1. Pickup Performance Percentage: Measure of the successful pickup by a vendor for a particular pickup_state of the total pickups being made for that state by that vendor.
How is Successful Pickup Defined?
If the difference between pickup date and manifestation date is less than or equal to 2 days/48 hours is defined as successful Pickup.
2. Average Delivery TAT: Assuming status updates on latest_status_date after delivery, the difference between latest_status_date and pickup_date is Average Delivery TAT for a particular vendor and particular state.
3. Return Percentage: Percentage of orders with shipment_status as RTO for an order/ Total Number of orders by a particular vendor for a particular state is defined as return percentage.
