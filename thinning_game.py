import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Water Game", layout="centered")
st.title("💧 Water Consumption Simulation")

# Sidebar inputs
num_people = st.slider("Number of People", 1, 20, 12)
max_drink_per_person = st.slider("Max Drinks per Person", 1, 10, 5)
num_days = st.slider("Number of Days", 30, 365, 120)

# Daily supply range
st.subheader("🔧 Daily Supply Range")
min_supply = st.slider("Minimum Daily Supply (bottles)", 5, 90, 5)
max_supply = st.slider("Maximum Daily Supply (bottles)", min_supply + 1, 105, 90)

# Generate water supply
np.random.seed(42)
daily_supply = (np.random.gamma(shape=2.0, scale=15.0, size=num_days)).astype(int) + 5
daily_supply = np.clip(daily_supply, min_supply, max_supply)

# Calculate daily consumption
max_possible_drink = num_people * max_drink_per_person
actual_consumption = np.minimum(daily_supply, max_possible_drink)

# Calculate totals
total_supplied = np.sum(daily_supply)
total_consumed = np.sum(actual_consumption)
total_leftover = total_supplied - total_consumed

# Calculate instances where supply > consumption
excess_days = np.where(daily_supply > actual_consumption)[0]
num_excess_days = len(excess_days)

# Show metrics
st.metric("Total Supplied", total_supplied)
st.metric("Total Consumed", total_consumed)
st.metric("Total Leftover", total_leftover)
st.markdown(f"🟢 **Days when supply > consumption**: {num_excess_days} out of {num_days}")

# Plotting
st.subheader("📊 Daily Supply vs Consumption")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(daily_supply, label="Daily Supply", alpha=0.7)
ax.plot(actual_consumption, label="Daily Consumption", alpha=0.7)

# Highlight excess supply days
ax.scatter(excess_days, daily_supply[excess_days], color='green', label="Supply > Consumption", s=50, zorder=5)

ax.set_xlabel("Day")
ax.set_ylabel("Water Bottles")
ax.legend()
st.pyplot(fig)

