import streamlit as st
import pandas as pd
from api import get_coin_price, get_price_history

# Set the page title and basic configuration
st.title("Crypto Price Tracker")

# User inputs: Select coin type and historical time range (in days)
coin = st.selectbox("Choose coin type", ["bitcoin", "ethereum", "solana", "cardano", "ripple"]) #TODO: maybe not these types, it's just a format, all based on api.
days = st.slider("Select historical days", 1, 30, 7)

# Define the currency (default to 'usd' for now, can be changed later)# TODO: currency to be decided
currency = "usd"

# Fetch current price and historical data from backend api.py
price_data = get_coin_price(coin, vs_currency=currency) # TODO: currency to be decided
history = get_price_history(coin, days=days, vs_currency=currency) # TODO: currency to be decided