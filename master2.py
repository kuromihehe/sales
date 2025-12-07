import streamlit as st

# ------- Helper: convert yen <-> 万円 --------
def man_to_yen(man_value):
    """Convert 万 input into yen."""
    return man_value * 10000

def yen_to_man(yen_value):
    """Convert yen into 万 for display."""
    return yen_value / 10000 if yen_value is not None else 0

# ------- Page config --------
st.set_page_config(
    page_title="Sales Forecasting Prototype",
    layout="centered",
)

st.title("Sales Forecasting Prototype (Uniqlo Case Study)")
st.write(
    "This prototype predicts end-of-day sales using simple baseline calculations. "
    "All data shown is simulated for academic purposes only."
)

# ------- Sidebar Inputs --------
st.sidebar.header("Store Settings")

open_time = st.sidebar.number_input(
    "Store opening time (hour, 24h)", min_value=0, max_value=23, value=10
)
close_time = st.sidebar.number_input(
    "Store closing time (hour, 24h)", min_value=1, max_value=23, value=21
)

st.sidebar.header("Current Status (Now)")

current_time = st.sidebar.number_input(
    "Current time (hour, 24h)", min_value=0, max_value=23, value=15
)
customers_so_far = st.sidebar.number_input(
    "Customers so far", min_value=0, value=850, step=10
)
avg_ticket = st.sidebar.number_input(
    "Average spend per customer (yen)", min_value=0, value=2400, step=100
)

# DAILY TARGET NOW ENTERED IN 万円 (example: 500 = 500万)
daily_target_man = st.sidebar.number_input(
    "Daily sales target (in 万 yen)", min_value=0, value=500, step=10
)
daily_target = man_to_yen(daily_target_man)

st.markdown("### Input Summary")

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Store Hours:** {open_time}:00 to {close_time}:00")
    st.write(f"**Current Time:** {current_time}:00")
with col2:
    st.write(f"**Customers so far:** {customers_so_far}")
    st.write(f"**Avg spend per customer:** ¥{avg_ticket:,}")
    st.write(f"**Daily target:** {daily_target_man} 万円")

st.markdown("---")

# ------- Validation --------
if current_time <= open_time:
    st.error("Current time must be after store opening time.")
else:
    # ------- Calculations --------
    hours_elapsed = current_time - open_time
    total_hours = close_time - open_time

    sales_so_far = customers_so_far * avg_ticket
    hourly_rate = sales_so_far / hours_elapsed if hours_elapsed > 0 else 0
    predicted_sales = hourly_rate * total_hours

    achievement = (predicted_sales / daily_target * 100) if daily_target > 0 else 0
    shortfall = daily_target - predicted_sales

    # ------- Display Results (All in 万円) --------
    st.markdown("### Prediction Results (Baseline Linear Model)")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Sales so far", f"{yen_to_man(sales_so_far):.1f} 万円")
        st.metric("Estimated hourly rate", f"{yen_to_man(hourly_rate):.1f} 万円/hr")
    with c2:
        st.metric("Predicted end-of-day sales", f"{yen_to_man(predicted_sales):.1f} 万円")
        st.metric("Target achievement", f"{achievement:.1f}%")

    st.markdown("---")

    # ------- Shortfall or Surplus (English only) --------
    if shortfall > 0:
        st.error(
            f"Projected shortfall: {yen_to_man(shortfall):.1f} 万円 "
            f"({100 - achievement:.1f}% below target)"
        )
    else:
        st.success(
            f"Projected surplus: {yen_to_man(-shortfall):.1f} 万円 "
            f"({achievement - 100:.1f}% above target)"
        )

    # ------- Notes --------
    st.markdown("### Model Notes")
    st.write(
        "- This app uses a simple linear extrapolation baseline for prediction.\n"
        "- In the main project, this logic is replaced by ARIMA / XGBoost / LSTM ensemble models.\n"
        "- All data used here is simulated and for demonstration only."
    )
    # ------- Shortfall or Surplus (English + Suggested Actions) --------
if shortfall > 0:
    st.error(
        f"Projected shortfall: {yen_to_man(shortfall):.1f} 万円 "
        f"({100 - achievement:.1f}% below target)"
    )
    st.markdown("#### Suggested Actions")
    st.write(
        "- Increase floor staff focus on high-value items\n"
        "- Promote seasonal or bundled products\n"
        "- Reduce backroom tasks during peak hours\n"
        "- Speed up fitting room and checkout operations"
    )

else:
    st.success(
        f"Projected surplus: {yen_to_man(-shortfall):.1f} 万円 "
        f"({achievement - 100:.1f}% above target)"
    )
    st.markdown("#### Suggested Actions")
    st.write(
        "- Maintain current staffing strategy\n"
        "- Observe factors contributing to strong performance\n"
        "- Use surplus margin to test layout or promotional ideas"
    )
    # ------- Uniqlo-style Red Theme CSS -------
uniqlo_css = """
<style>
/* Main background */
body {
    background-color: #ffffff;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 2px solid #e60012; /* Uniqlo red */
}

/* Title styling */
h1 {
    color: #e60012 !important;
    font-weight: 700 !important;
}

/* Section headers */
h2, h3, h4 {
    color: #e60012 !important;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    color: #e60012 !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton>button {
    background-color: #e60012;
    color: white;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
}

/* Error box */
.stAlert {
    border-left: 6px solid #e60012 !important;
}

/* Success box */
.stSuccess {
    border-left: 6px solid #008000 !important;
}
</style>
"""
st.markdown(uniqlo_css, unsafe_allow_html=True)


