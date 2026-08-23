from api import get_coin_price, get_price_history, check_alert, APIError
import time

while True:
    try:

        user_coin = str(input("Input the Crypto Coin You want The Price for: "))
        if user_coin.lower() == "exit":
            print("You are now exiting the program, Thank you!")
            break
        coin_currency = str(input(f"Enter the currency you'd like to see {user_coin} in: (usd, eur, or gbp) "))
        if coin_currency.lower() == "exit":
            print("You are now exiting the program, Thank you!")
            break
        coin_details = get_coin_price(user_coin, coin_currency)

        print(f"Coin ID: {coin_details['coin_id']}")
        print(f"Currency: {coin_details['vs_currency']}")
        print(f"Current Price in {coin_details['vs_currency']}: {coin_details['price']}")
        print(f"Price this Coin has changed in the last 24 hours: {coin_details['change_24h']}")
        print(f"Total Market Cap: {coin_details['market_cap']} \n")

        print("Checking for Major price movements in the last 24 hours.... \n")
        if check_alert(coin_details):
            print(f"⚠️ ALERT: {coin_details['coin_id']} moved {coin_details['change_24h']:.2f}% in the last 24 hours!\n")
        else:
            print(f"No Major price movement {coin_details['coin_id']} in the last 24 hours.\n")

        print("Checking Price history for this Coin...")

        days = int(input(f"How many past days do you want to check the price history for {user_coin}? "))
        price_history = get_price_history(user_coin, days, coin_currency)

        first_price = price_history["prices"][0][1]
        last_price = price_history["prices"][-1][1]
        percent_change = ((last_price - first_price) / first_price) * 100

        print(f"\n{price_history['days']}-Day History:")
        print(f"  {price_history['days']} days ago: {first_price:,.2f} {coin_currency.upper()}")
        print(f"  Today:        {last_price:,.2f} {coin_currency.upper()}")
        print(f"  Change:       {percent_change:+.2f}%")
        print("\n")






    except ValueError as e:
        print(f"Error please check: {e}")
    except APIError as e:
        print(f"Network problem please review: {e}")
    
    


