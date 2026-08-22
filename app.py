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
coin_options = [
    "bitcoin", 
    "ethereum", 
    "solana", 
    "cardano", 
    "ripple", 
    "dogecoin", 
    "polkadot"
]

if not advanced_mode:
    coin = st.sidebar.selectbox(
        label="Choose coin type", 
        options=coin_options,
        help="Select the CoinGecko coin ID for tracking."
    )
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
currency_options = ["usd", "eur", "gbp"]

if not advanced_mode:
    currency = st.sidebar.selectbox(
        label="Select currency", 
        options=currency_options,
        index=0,
        help="Select the fiat currency for price conversion."
    )
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

# ==========================================    
# Handover Contract Variables for Member 4
# ==========================================
# All user inputs have been strictly sanitized, validated, and frozen upon the click of the "Fetch Data" button. You can safely consume the following variables:
# 
# - coin (str): Cleaned, lowercase CoinGecko identifier (e.g., "bitcoin", "ethereum"). Ready to be passed directly to api.py functions.
# - currency (str): Cleaned, lowercase ISO fiat currency code (e.g., "usd", "eur").
# - days (int): Validated historical timeframe integer (constrained by UI range: 1 to 365).
#
# Note: Empty inputs, invalid types, and premature API calls have already been intercepted here via st.stop() and guarded with defensive checks.