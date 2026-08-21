import pandas as pd

df = pd.read_csv("APSRTC_Transport_Data.csv")

print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
# Check Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Check Duplicate Rows
print("\nDuplicate Rows:", df.duplicated().sum())

# Convert Date Column
df["date"] = pd.to_datetime(df["date"])

# Check Data Types
print("\nData Types:")
print(df.dtypes)
print("\n========== DASHBOARD SUMMARY ==========\n")

print(f"🚌 Total Routes           : {df['route'].nunique()}")
print(f"🚍 Total Bus Types        : {df['bus_type'].nunique()}")
print(f"🏢 Total Depots           : {df['depot'].nunique()}")
print(f"👥 Total Passengers       : {df['passengers'].sum()}")
print(f"💰 Total Revenue          : ₹{df['revenue'].sum():,.2f}")
print(f"📈 Average Occupancy      : {df['occupancy_rate'].mean():.2f}%")
print(f"🛣 Average Distance       : {df['distance_km'].mean():.2f} KM")
print(f"⛽ Average Fuel Consumed  : {df['fuel_consumed_liters'].mean():.2f} Liters")

route_revenue = (
    df.groupby("route")["revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== TOP ROUTES BY REVENUE =====\n")
print(route_revenue)

route_passenger = (
    df.groupby("route")["passengers"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== TOP ROUTES BY PASSENGERS =====\n")
print(route_passenger)

bus_performance = (
    df.groupby("bus_type")[["passengers", "revenue", "occupancy_rate"]]
      .mean()
      .round(2)
)

print("\n===== BUS TYPE PERFORMANCE =====\n")
print(bus_performance)

import matplotlib.pyplot as plt

route_revenue = (
    df.groupby("route")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

plt.bar(route_revenue.index, route_revenue.values)

plt.xticks(rotation=45)

plt.xlabel("Route")
plt.ylabel("Revenue")
plt.title("Revenue by Route")

plt.tight_layout()

plt.savefig("graphs/revenue_by_route.png")

plt.show()

route_passenger = (
    df.groupby("route")["passengers"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

plt.bar(route_passenger.index, route_passenger.values)

plt.xticks(rotation=45)

plt.xlabel("Route")
plt.ylabel("Passengers")
plt.title("Passengers by Route")

plt.tight_layout()

plt.savefig("graphs/passenger_by_route.png")

plt.show()

bus = (
    df.groupby("bus_type")["revenue"]
    .mean()
)

plt.figure(figsize=(8,5))

plt.bar(bus.index, bus.values)

plt.title("Average Revenue by Bus Type")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("graphs/revenue_by_bus_type.png")

plt.show()