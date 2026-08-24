# crypto-tracker
A Streamlit crypto price tracker using the CoinGecko API

# 📈 Crypto Price Tracker

An interactive cryptocurrency price tracker built with **Python, Streamlit, and the CoinGecko API**.

Users can select a cryptocurrency, choose a fiat currency, and explore current prices, 24-hour price changes, market capitalization, and historical price trends. The project also includes a standalone command-line interface and API test script.

## 🌐 Live App

**[Launch the Crypto Price Tracker](PASTE-LIVE-APP-URL-HERE)**

## Features

* Track popular cryptocurrencies including Bitcoin, Ethereum, Solana, Dogecoin, and more
* View prices in multiple fiat currencies
* Display current price, 24-hour percentage change, and market capitalization
* Explore historical price trends with an interactive chart
* Select custom historical timeframes
* Use Advanced Input Mode to enter custom CoinGecko IDs and currencies
* Display an alert when a cryptocurrency moves more than 5% in 24 hours
* Run the tracker through either Streamlit or the command line
* Handle invalid coins, API errors, timeouts, and CoinGecko rate limits

## Project Structure

```text
crypto-tracker/
├── api.py
├── app.py
├── cli_demo.py
├── test_api.py
├── requirements.txt
├── README.md
└── .gitignore
```

### File Overview

* `api.py` — CoinGecko API layer containing price, historical data, and alert functions. It can also run independently from the command line.
* `app.py` — Streamlit web application containing the user interface, chart, market statistics, and alert display.
* `cli_demo.py` — Interactive command-line version of the crypto tracker.
* `test_api.py` — End-to-end smoke tests for the core API functions.
* `requirements.txt` — Python package dependencies.

## Getting Started

### Prerequisites

* Python 3.10.0
* Git
* Internet connection

The CoinGecko endpoints used by this project **do not require an API key**.

### Clone the Repository

```bash
git clone git@github.com:dukeai36/crypto-tracker.git
cd crypto-tracker
```

### Create a Virtual Environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses:

```text
streamlit
pandas
requests
```

## Run the Streamlit App

Start the local web application with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open that address in your browser.

### Example Usage

1. Select **Bitcoin (BTC)**.
2. Select **USD (US Dollar)**.
3. Choose **7 days** of historical data.
4. Click **Fetch Data**.
5. Review the current price, 24-hour change, market capitalization, price-history chart, and statistics table.

Enable **Advanced Input Mode** to manually enter other valid CoinGecko coin IDs, currencies, and longer historical periods.

## Command-Line Interface

The project also includes an interactive CLI:

```bash
python cli_demo.py
```

The CLI will prompt you for:

```text
Input the Crypto Coin You want The Price for: bitcoin
Enter the currency you'd like to see bitcoin in: (usd, eur, or gbp) usd
How many past days do you want to check the price history for bitcoin? 7
```

It then displays the current price, 24-hour price movement, market capitalization, alert status, and historical price change.

Enter `exit` when prompted for the coin or currency to leave the program.

## Run the API Module Directly

`api.py` can also be executed independently:

```bash
python api.py --coin bitcoin --currency usd --days 7
```

Example with another asset:

```bash
python api.py --coin ethereum --currency eur --days 30
```

Optional arguments include:

```text
--coin        CoinGecko coin ID
--currency    Fiat currency such as usd, eur, or gbp
--days        Number of days of historical data
--threshold   24-hour percentage-change alert threshold
```

## Testing

Run the API smoke tests with:

```bash
python test_api.py
```

The test script checks:

* Bitcoin price retrieval
* Ethereum price retrieval in EUR
* Bitcoin historical price data
* Price-alert logic
* Error handling for an invalid coin

You can also verify that all project files compile correctly with:

```bash
python -m py_compile api.py app.py cli_demo.py test_api.py
```

## Core API Functions

### `get_coin_price(coin_id, vs_currency="usd")`

Retrieves the current price, 24-hour percentage change, and market capitalization for a cryptocurrency.

### `get_price_history(coin_id, days=7, vs_currency="usd")`

Retrieves historical price data for the requested cryptocurrency and timeframe.

### `check_alert(price_data, threshold=5.0)`

Returns `True` when the absolute 24-hour percentage change exceeds the selected threshold.

## Demo

A short demonstration of the project shows:

1. The standalone API/CLI
2. The local Streamlit application
3. The live deployed application

<!-- After adding your demo file, uncomment one of these:

![Crypto Price Tracker Demo](assets/demo.gif)

or add a link to your demo video here.

-->

## Technologies Used

* Python 3.10.0
* Streamlit
* CoinGecko API
* Requests
* Pandas
* Git
* GitHub

## Error Handling

The API layer includes handling for:

* Unknown cryptocurrency IDs
* Invalid currencies
* Invalid historical-day values
* Network failures
* Request timeouts
* CoinGecko rate limiting
* Invalid API responses

CoinGecko rate-limit responses are retried once before an error is returned to the user.

## Contributors

This project was developed collaboratively as a six-person team project. Development was divided across the API layer, CLI interface, Streamlit inputs, Streamlit outputs and visualization, deployment, and documentation/QA.

## License

This project was developed for an academic team assignment.