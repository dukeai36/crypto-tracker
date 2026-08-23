"""
Crypto Price Tracker - Member 3: Input Module

This module is responsible for the Streamlit frontend user interface,
handling user inputs (coin selection, currency, and historical timeframe),
and passing these parameters to the backend API and Member 4's visualization module.
"""

import streamlit as st
import pandas as pd
from api import get_coin_price, get_price_history, check_alert, APIError

# Page Configuration & Header
st.set_page_config(
    page_title="Crypto Price Tracker",
    page_icon="📈",
    layout="centered"
)

st.title("Crypto Price Tracker")
st.write("Track real-time cryptocurrency prices and historical trends effortlessly.")

# Sidebar Configuration (Input Controls)
st.sidebar.header("Configuration Panel")
st.sidebar.markdown("Customize your market view parameters below.")

# Global Advanced Mode Toggle for a sleek, pro-level experience
advanced_mode = st.sidebar.toggle(
    label="Enable Advanced Input Mode",
    value=False,
    help="Switch on to manually input custom asset IDs, fiat currencies, and precise historical day ranges."
)

# 1. Coin Type Input (Dynamic based on toggle)
coin_options = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Tether (USDT)": "tether",
    "BNB (BNB)": "binancecoin",
    "Solana (SOL)": "solana",
    "USDC (USDC)": "usd-coin",
    "XRP (XRP)": "ripple",
    "Dogecoin (DOGE)": "dogecoin",
    "Cardano (ADA)": "cardano",
    "TRON (TRX)": "tron",
    "Avalanche (AVAX)": "avalanche-2",
    "Chainlink (LINK)": "chainlink",
    "Polkadot (DOT)": "polkadot",
    "Polygon (POL)": "polygon",
    "Litecoin (LTC)": "litecoin",
    "Bitcoin Cash (BCH)": "bitcoin-cash",
    "Stellar (XLM)": "stellar",
    "Uniswap (UNI)": "uniswap",
    "Cosmos (ATOM)": "cosmos",
    "Shiba Inu (SHIB)": "shiba-inu"
}

if not advanced_mode:
    selected_coin = st.sidebar.selectbox(
        label="Choose coin type",
        options=list(coin_options.keys()),
        help="Select the cryptocurrency for tracking."
    )

    coin = coin_options[selected_coin]

else:
    coin_input = st.sidebar.text_input(
        label="Enter custom CoinGecko ID",
        value="bitcoin",
        placeholder="e.g., avalanche-2, chainlink",
        help="Input any valid CoinGecko API cryptocurrency identifier."
    ).strip().lower()
    
    # Defensive programming: Prevent empty string submission
    if not coin_input:
        st.sidebar.error("⚠️ Please enter a valid CoinGecko ID to proceed.")
        st.stop()
    coin = coin_input


# 2. Currency Input (Dynamic based on toggle)
currency_options = {
    "USD (US Dollar)": "usd",
    "EUR (Euro)": "eur",
    "GBP (British Pound)": "gbp",
    "JPY (Japanese Yen)": "jpy",
    "CAD (Canadian Dollar)": "cad",
    "AUD (Australian Dollar)": "aud",
    "CHF (Swiss Franc)": "chf",
    "CNY (Chinese Yuan)": "cny",
    "INR (Indian Rupee)": "inr",
    "AED (UAE Dirham)": "aed"
}

if not advanced_mode:

    selected_currency = st.sidebar.selectbox(
        label="Select currency",
        options=list(currency_options.keys()),
        index=0,
        help="Select the fiat currency for price conversion."
    )

    currency = currency_options[selected_currency]
else:
    currency_input = st.sidebar.text_input(
        label="Enter custom currency code",
        value="usd",
        placeholder="e.g., jpy, aud, cad",
        help="Input a standard ISO fiat currency code."
    ).strip().lower()
    
    # Defensive programming: Prevent empty string submission
    if not currency_input:
        st.sidebar.error("⚠️ Please enter a valid currency code.")
        st.stop()
    currency = currency_input


# 3. Historical Days Input (Dynamic based on toggle)
if not advanced_mode:
    days = st.sidebar.slider(
        label="Select historical days", 
        min_value=1, 
        max_value=30, 
        value=7,
        help="Select the timeframe length for historical trend analysis."
    )
else:
    days = int(st.sidebar.number_input(
        label="Enter custom historical days",
        min_value=1,
        max_value=365,
        value=7,
        step=1,
        help="Input a precise number of days for extended historical data tracking."
    ))
    
    if days is None or days <= 0:
        st.sidebar.error("⚠️ Please input at least 1 valid day for tracking.")
        st.stop()

# Add a submit buttom on the bottom of the sidebar
submit_btn = st.sidebar.button("Fetch Data", type="primary")

if not submit_btn:
    st.info("👈 Adjust your parameters and click 'Fetch Data' to update the dashboard.")
    st.stop()  # Halt execution until the user clicks the button; never call the API prematurely.

# Visual separator for the main dashboard body
st.markdown("---")

# Fetch crypto data
try:
    price_data = get_coin_price(coin, currency)
    history = get_price_history(coin, days, currency)

except (ValueError, APIError) as exc:
    st.error(f"Unable to fetch data: {exc}")
    st.stop()

# Market overview
st.subheader(f"{coin.title()} Market Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Price",
        f"{price_data['price']:,.2f} {currency.upper()}"
    )

with col2:
    change = price_data["change_24h"]
    if change is None:
        st.metric("24h Change", "N/A")
    else:
        st.metric(
            "24h Change",
            f"{change:+.2f}%"
        )

with col3:
    market_cap = price_data["market_cap"]

    if market_cap is None:
        market_cap_display = "N/A"

    elif market_cap >= 1_000_000_000_000:
        market_cap_display = f"{market_cap / 1_000_000_000_000:.2f}T"

    elif market_cap >= 1_000_000_000:
        market_cap_display = f"{market_cap / 1_000_000_000:.2f}B"

    else:
        market_cap_display = f"{market_cap / 1_000_000:.2f}M"

    st.metric(
        "Market Cap",
        f"{market_cap_display} {currency.upper()}"
    )
    
# Historical price chart
st.subheader(f"Price History - Last {days} Days")

history_df = pd.DataFrame(
    history["prices"],
    columns=["timestamp", "price"]
)

history_df["date"] = pd.to_datetime(
    history_df["timestamp"],
    unit="ms"
)

history_df = history_df.set_index("date")
st.line_chart(history_df["price"])

# Statistics table
st.subheader("Price Statistics")

stats_df = pd.DataFrame({
    "Metric": [
        "Current Price",
        "24h Change",
        "Market Cap"
    ],
    "Value": [
        f"{price_data['price']:,.2f} {currency.upper()}",
        (
            "N/A"
            if price_data["change_24h"] is None
            else f"{price_data['change_24h']:+.2f}%"
        ),
        (
            "N/A"
            if price_data["market_cap"] is None
            else f"{price_data['market_cap']:,.0f} {currency.upper()}"
        )
    ]
})

st.dataframe(
    stats_df,
    hide_index=True,
    use_container_width=True
)

# Price alert
if check_alert(price_data, threshold=5.0):
    st.warning(
        f"⚠️ {coin.title()} moved more than 5% "
        "in the last 24 hours!"
    )