import streamlit as st

# ------- Helper: Yen → 万円 --------
def to_man(value):
    """Convert yen to 万単位 (10,000 yen)."""
    return value / 10000 if value is not None else 0

# ------- Page config --------
st.set_page_config(
    page_title="Sales Prediction - Uniqlo Case Study",
    layout="centered",
)

st.title("Sales Forecasting Prototype (Uniqlo Case Study)")
st.write(
    "This web app predicts end-of-day store sales using simple baseline logic.\n"
    "All numbers are simulated for **academic purposes only** — no real Uniqlo data is used."
)

# ------- Sidebar Inputs --------
st.sidebar.header("Store Settings")

open_time = st.sidebar.number_input(
    "Store opening time (hour, 24h)", min_value=0, max_value=23, value=10
)
close_time = st.sidebar.number_input(
    "Store closing time (hour, 24h)", min_value=1, max_value=23, value=21
)

if close_time <= open_time:
    st.sidebar.error("Closing time must be later than opening time.")

st.sidebar.header("Current Status (Now)")

current_time = st.sidebar.number_input(
    "Current time (hour, 24h)", min_value=0, max_value=23, value=15
)
customers_so_far = st.sidebar.number_input(
    "Customers so far", min_value=0, value=850, step=10
)
avg_ticket = st.sidebar.number_input(
    "Average spend per customer (¥)", min_value=0, value=2400, step=100
)
daily_target = st.sidebar.number_input(
    "Daily sales target (¥)", min_value=0, value=5_000_000, step=100_000
)

# ------- Input Summary --------
st.markdown("### Input Summary")

col1, col2 = st.columns(2)
with col1:
    st.write(f"**Store Hours:** {open_time}:00 ～ {close_time}:00")
    st.write(f"**Current Time:** {current_time}:00")
with col2:
    st.write(f"**Customers so far:** {customers_so_far}")
    st.write(f"**Average spend per customer:** ¥{avg_ticket:,}")
    st.write(f"**Target for the day:** {to_man(daily_target):.1f} 万円")

st.markdown("---")

# ------- Validation & Calculations --------
if current_time <= open_time:
    st.error("Current time must be after store opening time.")
else:
    hours_elapsed = current_time - open_time
    total_hours = close_time - open_time

    # Sales so far
    sales_so_far = customers_so_far * avg_ticket if customers_so_far and avg_ticket else 0

    if hours_elapsed > 0:
        hourly_rate = sales_so_far / hours_elapsed
        predicted_sales = hourly_rate * total_hours
    else:
        hourly_rate = 0
        predicted_sales = 0

    achievement = (predicted_sales / daily_target * 100) if daily_target > 0 else 0
    shortfall = daily_target - predicted_sales

    # ------- Results (in 万円) --------
    st.markdown("### Prediction Results（Baseline Linear Model）")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Sales so far", f"{to_man(sales_so_far):.1f} 万円")
        st.metric("Estimated hourly rate", f"{to_man(hourly_rate):.1f} 万円 / 時間")
    with c2:
        st.metric("Predicted end-of-day sales", f"{to_man(predicted_sales):.1f} 万円")
        st.metric("Target achievement (projected)", f"{achievement:.1f}%")

    st.markdown("---")

    # ------- Shortfall / Surplus Message --------
    if daily_target > 0:
        if shortfall > 0:
            st.error(
                f"⚠ 予測不足: **{to_man(shortfall):.1f} 万円** の不足が見込まれます "
                f"({100 - achievement:.1f}% below target)."
            )
            st.write(
                "Suggested actions (concept level):\n"
                "- Move more staff from back office to sales floor\n"
                "- Focus on promoting higher-priced / seasonal items\n"
                "- Speed up fitting room and checkout to increase conversion"
            )
        else:
            st.success(
                f"✅ 目標超過: **{to_man(-shortfall):.1f} 万円** 上回る予測です "
                f"({achievement - 100:.1f}% above target)."
            )
            st.write(
                "Suggested actions (concept level):\n"
                "- Maintain current staffing strategy\n"
                "- Observe which factors led to strong performance\n"
                "- Consider testing layout or promotion experiments"
            )

    # ------- Notes --------
    st.markdown("### Model Notes")
    st.write(
        "- This prototype uses a **simple linear baseline**: current average hourly sales "
        "are projected over the full business day.\n"
        "- In the full project report, this is extended to **ARIMA, XGBoost, and LSTM** "
        "and an ensemble model with lower MAPE.\n"
        "- All data here is **dummy/simulated**, not real company data."
    )
