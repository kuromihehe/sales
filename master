import streamlit as st

st.set_page_config(
    page_title="Sales Prediction - Uniqlo Case Study",
    layout="centered",
)

st.title("AI-Powered Sales Forecasting (Uniqlo Case Study Prototype)")
st.write(
    "This demo predicts end-of-day store sales using current customer and sales data. "
    "All numbers are simulated for academic purposes only."
)

st.sidebar.header("Store Settings")

# Sidebar inputs for store hours
open_time = st.sidebar.number_input("Store opening time (hour, 24h)", min_value=0, max_value=23, value=10)
close_time = st.sidebar.number_input("Store closing time (hour, 24h)", min_value=1, max_value=23, value=21)

if close_time <= open_time:
    st.sidebar.error("Closing time must be later than opening time.")

st.sidebar.header("Current Status (Now)")

current_time = st.sidebar.number_input("Current time (hour, 24h)", min_value=0, max_value=23, value=15)
customers_so_far = st.sidebar.number_input("Customers so far", min_value=0, value=850)
avg_ticket = st.sidebar.number_input("Average spend per customer (¥)", min_value=0, value=2400)
daily_target = st.sidebar.number_input("Daily sales target (¥)", min_value=0, value=5_000_000)

st.markdown("### Input Summary")

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Store Hours:** {open_time}:00 - {close_time}:00")
    st.write(f"**Current Time:** {current_time}:00")
with col2:
    st.write(f"**Customers so far:** {customers_so_far}")
    st.write(f"**Average spend per customer:** ¥{avg_ticket:,}")
    st.write(f"**Target for the day:** ¥{daily_target:,}")

st.markdown("---")

# Basic validation
if current_time <= open_time:
    st.error("Current time must be after store opening time.")
else:
    # Calculations
    hours_elapsed = current_time - open_time
    total_hours = close_time - open_time

    sales_so_far = customers_so_far * avg_ticket if customers_so_far and avg_ticket else 0

    if hours_elapsed > 0:
        hourly_rate = sales_so_far / hours_elapsed
        predicted_sales = hourly_rate * total_hours
    else:
        hourly_rate = 0
        predicted_sales = 0

    achievement = (predicted_sales / daily_target * 100) if daily_target > 0 else 0
    shortfall = daily_target - predicted_sales

    st.markdown("### Prediction Results (Baseline Linear Model)")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Sales so far", f"¥{int(sales_so_far):,}")
        st.metric("Estimated hourly rate", f"¥{int(hourly_rate):,} / hour")
    with c2:
        st.metric("Predicted end-of-day sales", f"¥{int(predicted_sales):,}")
        st.metric("Target achievement (projected)", f"{achievement:.1f}%")

    st.markdown("---")

    if daily_target > 0:
        if shortfall > 0:
            st.error(
                f"⚠ Projected shortfall: **¥{int(shortfall):,}** "
                f"(about {100 - achievement:.1f}% below target)."
            )
            st.write(
                "Suggested actions (conceptual):\n"
                "- Increase floor staff focus on high-value items\n"
                "- Promote seasonal or bundled products\n"
                "- Reduce backroom tasks during peak hours"
            )
        else:
            st.success(
                f"✅ You are projected to exceed the target by **¥{int(-shortfall):,}** "
                f"(about {achievement - 100:.1f}% above target)."
            )
            st.write(
                "Suggested actions (conceptual):\n"
                "- Maintain current staffing strategy\n"
                "- Monitor for unexpected drops in traffic\n"
                "- Use extra margin to test new layouts or promotions"
            )

    st.markdown("### Model Notes")
    st.write(
        "- Current implementation uses a **linear baseline model** based on average hourly sales.\n"
        "- In the full project, this can be replaced by an **ensemble of ARIMA, XGBoost, and LSTM** "
        "trained on historical data.\n"
        "- This prototype is for demonstration and does not use real Uniqlo data."
    )
