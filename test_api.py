# Import the functions from api.py
from api import get_coin_price, get_price_history, check_alert


# Test 1: Bitcoin price
print("TEST 1: Bitcoin Price")

try:
    bitcoin = get_coin_price("bitcoin", "usd")

    print("Coin:", bitcoin["coin_id"])
    print("Currency:", bitcoin["vs_currency"])
    print("Price:", bitcoin["price"])
    print("PASS")

except Exception as error:
    print("FAIL:", error)


print()


# Test 2: Ethereum price
print("TEST 2: Ethereum Price")

try:
    ethereum = get_coin_price("ethereum", "eur")

    print("Coin:", ethereum["coin_id"])
    print("Currency:", ethereum["vs_currency"])
    print("Price:", ethereum["price"])
    print("PASS")

except Exception as error:
    print("FAIL:", error)


print()


# Test 3: Bitcoin price history
print("TEST 3: Bitcoin History")

try:
    history = get_price_history("bitcoin", 7, "usd")

    print("Days:", history["days"])
    print("Price points:", len(history["prices"]))
    print("PASS")

except Exception as error:
    print("FAIL:", error)


print()


# Test 4: Price alert
print("TEST 4: Price Alert")

price_data = {"change_24h": 6.0}

alert = check_alert(price_data, 5.0)

print("Price change: 6%")
print("Alert:", alert)

if alert:
    print("PASS")
else:
    print("FAIL")


print()


# Test 5: Invalid coin
print("TEST 5: Invalid Coin")

try:
    get_coin_price("not_a_valid_coin", "usd")
    print("FAIL")

except ValueError as error:
    print("Error caught:", error)
    print("PASS")

except Exception as error:
    print("API error:", error)