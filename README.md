# Crypto Price Tracker App

    Crypto Price Tracker allows the user to track cryptocurrency market data in their desired fiat currency and timeframe with the CoinGecko API.
     This project is deployed on Streamlit Community Cloud: **TODO: Add live Streamlit app URL here 


## Features

    Once the user inputs their preferences the app shows the current price of the selected cryptocurrency, it's 24-hour percentage change, and a historical price chart. (A warning appears when the coin moves more than 5% in either direction over 24 hours.)
    
    There's also an Advanced Input Mode for custom CoinGecko coin IDs, currency codes, and historical periods from 1 to 365 days.

    The project can be run three ways: through Streamlit, through the interactive CLI, or directly through `api.py`.

    Bad coin IDs and other invalid inputs show an error instead of crashing. The API also handles network errors, request timeouts, CoinGecko rate limits, and invalid API responses.

# Getting Set Up

## Prerequisites

    * Python 3.10.0
    * Git
    * streamlit
    * pandas
    * requests

    The CoinGecko endpoints used here work without an API key. The API layer also supports an optional CoinGecko demo key through the `COINGECKO_API_KEY` environment variable.

## Clone and Set Up
    Initialize the project by running code in your terminal to clone the project from git, navigate to the proper project folder, create the required virtual environment, and install the necessary packages

    # Clone the repo
        git clone git@github.com:dukeai36/crypto-tracker.git
        cd crypto-tracker

    #Create and activate a virtual environment
        python3 -m venv .venv
        source .venv/bin/activate # macOS/Linux
        .venv\Scripts\Activate.ps1 # Windows PowerShell

    #Install dependencies
        pip install -r requirements.txt
   

# Running Crypto Price Tracker on your Terminal

    # Running on Streamlit (app.py):    
        streamlit run app.py
            Then open your browser at http://localhost:8501
    
    
    # Running Interactive CLI (cli_demo.py)
        python cli_demo.py
             The CLI asks the user to manually input hte name of cryptocurrency, fiat currency, and  number of historical days of finacial data.

                    Example:

                    ```text
                    Input the Crypto Coin You want The Price for: bitcoin: *User input*
                    Enter the currency you'd like to see bitcoin in: (usd, eur, or gbp) usd: *user input*
                    How many past days do you want to check the price history for bitcoin? *user input*
                    ```

                    It then prints the coin ID, currency, current price, 24-hour price change, market capitalization, price alert status, historical starting and ending prices, and percentage change over the selected period.

                    Enter `exit` at the coin or currency prompt to close the CLI.

    ## Run the API Module Directly

        ```bash
        python api.py --coin bitcoin --currency usd --days 7
        ```

        Another example:

        ```bash
        python api.py --coin ethereum --currency eur --days 30
        ```

            Available arguments:

                ```text
                    --coin        CoinGecko cryptocurrency ID
                    --currency    Fiat currency code
                    --days        Number of historical days
                    --threshold   24-hour percentage-change alert threshold
                ```

### Input and Frontend engagmenet

    # Normally
        1. Drop down to select desired crypto and fiat currency
        2. Slider to seelct the amount of days of history requested
        3. Hit 'Fetch Data' to get output

    #Advanced Input Mode 
        Allows for manual input to choose desired CoinGecko ID, currency code, and timeframe.

        For example:

            ```text
                CoinGecko ID: dogecoin
                Currency: eur
                Historical days: 14
            ```
        


## Project Case Testing History

    Run the smoke tests with:

    ```bash
    python test_api.py
    ```

    The script checks five basic cases:

    1. Bitcoin price retrieval in USD
    2. Ethereum price retrieval in EUR
    3. Seven-day Bitcoin price history
    4. Price-alert logic when a 6% move exceeds a 5% threshold
    5. Error handling for an invalid cryptocurrency ID

    In final QA run, all five API test cases passed

## Core API Functions

    ### `get_coin_price(coin_id, vs_currency="usd")`

        Gets the current price, 24-hour percentage change, and market capitalization.

    ### `get_price_history(coin_id, days=7, vs_currency="usd")`

        Gets historical cryptocurrency price points for the selected timeframe.

    ### `check_alert(price_data, threshold=5.0)`

         Returns `True` when the absolute 24-hour percentage change is greater than the selected threshold.

## Project Structure

    ```text
    crypto-tracker/
        ├── api.py: CoinGecko API functions and the standalone command-line API interface
        ├── app.py: : Streamlit web app
        ├── cli_demo.py: : interactive terminal version
        ├── test_api.py
        ├── requirements.txt
        ├── README.md
        ├── .gitignore
        ├── LICENSE
        └── assets/
            └── crypto-tracker-demo.png
    ```

## Notes and Known Limitations

    CoinGecko's free tier can rate-limit repeated requests. If that happens, the API waits briefly and retries once before returning an error.

    The standard Streamlit interface is intentionally limited to 20 coins and 1 to 30 days of history. Advanced Input Mode supports custom CoinGecko IDs and up to 365 days.


## Demo

    Our final project demo shows the CLI, the Streamlit app running locally, and the live Streamlit Community Cloud deployment.

## Contributors

    This project was built by a six-person team using individual Git branches, commits, and pull requests:
        Praful Chunchu
        John Fillingim
        Cheney Li
        Lexie Lin
        Murwan Owais
        Samuel Teshome