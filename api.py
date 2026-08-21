"""API layer for the Crypto Price Tracker.

Wraps the free CoinGecko v3 API (no API key required).

Importable:
    from api import get_coin_price, get_price_history, check_alert

Standalone:
    python api.py --coin bitcoin --currency usd --days 7
"""

import argparse
import os
import time

import requests

BASE_URL = "https://api.coingecko.com/api/v3"
TIMEOUT = 10

# Optional CoinGecko demo key. The endpoints used here work without one, so
# this is read from the environment and simply omitted when it is not set.
API_KEY_ENV = "COINGECKO_API_KEY"


class APIError(Exception):
    """Raised when CoinGecko cannot be reached or returns an error."""


def _headers():
    """Auth headers for CoinGecko, or an empty dict when no key is set."""
    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        return {}
    return {"x-cg-demo-api-key": key}


def _get(path, params):
    """GET a CoinGecko endpoint, retrying once if we get rate limited.

    Returns the decoded JSON body. Raises APIError on network/HTTP problems.
    """
    url = BASE_URL + path
    headers = _headers()
    for attempt in range(2):
        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=TIMEOUT
            )
        except requests.exceptions.Timeout:
            raise APIError("CoinGecko request timed out. Try again in a moment.")
        except requests.exceptions.RequestException as exc:
            raise APIError("Could not reach CoinGecko: %s" % exc)

        if response.status_code == 429:
            if attempt == 0:
                time.sleep(2)  # rate limited - back off once, then retry
                continue
            raise APIError("CoinGecko rate limit hit. Wait a minute and retry.")

        if response.status_code in (401, 403) and headers:
            raise APIError(
                "CoinGecko rejected the API key in %s. Check the key, or unset "
                "the variable to use the free endpoints." % API_KEY_ENV
            )

        if not response.ok:
            raise APIError(
                "CoinGecko returned HTTP %s for %s" % (response.status_code, path)
            )

        try:
            return response.json()
        except ValueError:
            raise APIError("CoinGecko returned a response that was not valid JSON.")


def get_coin_price(coin_id, vs_currency="usd"):
    """Return current price data for one coin.

    Returns a dict with these keys (this is the shared data shape the
    CLI and Streamlit layers build against):

        {
            "coin_id":     "bitcoin",
            "vs_currency": "usd",
            "price":       64231.55,
            "change_24h":  -2.31,      # percent, may be None
            "market_cap":  1268000000, # may be None
        }

    Raises ValueError for an unknown coin id, APIError for API problems.
    """
    coin_id = str(coin_id).strip().lower()
    vs_currency = str(vs_currency).strip().lower()

    data = _get(
        "/simple/price",
        {
            "ids": coin_id,
            "vs_currencies": vs_currency,
            "include_24hr_change": "true",
            "include_market_cap": "true",
        },
    )

    # CoinGecko answers an unknown id with 200 and an empty object.
    if coin_id not in data:
        raise ValueError(
            "Unknown coin id '%s'. Use a CoinGecko id such as 'bitcoin' or "
            "'ethereum'." % coin_id
        )

    entry = data[coin_id]
    if vs_currency not in entry:
        raise ValueError(
            "Unknown currency '%s'. Try 'usd', 'eur' or 'gbp'." % vs_currency
        )

    return {
        "coin_id": coin_id,
        "vs_currency": vs_currency,
        "price": entry[vs_currency],
        "change_24h": entry.get("%s_24h_change" % vs_currency),
        "market_cap": entry.get("%s_market_cap" % vs_currency),
    }


def get_price_history(coin_id, days=7, vs_currency="usd"):
    """Return historical prices for charting.

    Returns a dict:

        {
            "coin_id":     "bitcoin",
            "vs_currency": "usd",
            "days":        7,
            "prices":      [(datetime_ms, price), ...],  # oldest first
        }

    Each entry in "prices" is a (timestamp_ms, price) tuple, so a chart
    layer can convert the timestamp however it likes.

    Raises ValueError for a bad coin id or a bad days value, APIError for
    API problems.
    """
    coin_id = str(coin_id).strip().lower()
    vs_currency = str(vs_currency).strip().lower()

    try:
        days = int(days)
    except (TypeError, ValueError):
        raise ValueError("days must be a whole number, got %r" % (days,))
    if days < 1:
        raise ValueError("days must be at least 1, got %s" % days)

    try:
        data = _get(
            "/coins/%s/market_chart" % coin_id,
            {"vs_currency": vs_currency, "days": days},
        )
    except APIError as exc:
        # An unknown coin id gives a 404 on this endpoint.
        if "404" in str(exc):
            raise ValueError(
                "Unknown coin id '%s'. Use a CoinGecko id such as 'bitcoin'."
                % coin_id
            )
        raise

    points = data.get("prices") or []
    if not points:
        raise ValueError(
            "No price history returned for '%s' in '%s'." % (coin_id, vs_currency)
        )

    return {
        "coin_id": coin_id,
        "vs_currency": vs_currency,
        "days": days,
        "prices": [(int(point[0]), float(point[1])) for point in points],
    }


def check_alert(price_data, threshold=5.0):
    """True if the 24h percent change is bigger than threshold in either direction.

    Takes the dict returned by get_coin_price(). Returns False when the
    24h change is unavailable.
    """
    change = price_data.get("change_24h") if price_data else None
    if change is None:
        return False
    return abs(change) > abs(float(threshold))


def _format_money(value, vs_currency):
    if value is None:
        return "n/a"
    return "%s %s" % ("{:,.2f}".format(value), vs_currency.upper())


def main():
    parser = argparse.ArgumentParser(
        description="Fetch crypto prices from CoinGecko."
    )
    parser.add_argument("--coin", default="bitcoin", help="CoinGecko coin id")
    parser.add_argument("--currency", default="usd", help="fiat currency, e.g. usd")
    parser.add_argument("--days", type=int, default=7, help="days of price history")
    parser.add_argument(
        "--threshold", type=float, default=5.0, help="24h %% change alert threshold"
    )
    args = parser.parse_args()

    try:
        price = get_coin_price(args.coin, args.currency)
        history = get_price_history(args.coin, args.days, args.currency)
    except (ValueError, APIError) as exc:
        print("Error: %s" % exc)
        return 1

    change = price["change_24h"]
    print("%s (%s)" % (price["coin_id"].title(), price["vs_currency"].upper()))
    print("  Price:      %s" % _format_money(price["price"], args.currency))
    print("  24h change: %s" % ("n/a" if change is None else "%+.2f%%" % change))
    print("  Market cap: %s" % _format_money(price["market_cap"], args.currency))

    points = history["prices"]
    print("  History:    %d points over %d day(s)" % (len(points), history["days"]))
    print("    first: %s" % _format_money(points[0][1], args.currency))
    print("    last:  %s" % _format_money(points[-1][1], args.currency))

    if check_alert(price, args.threshold):
        print("  ALERT: moved more than %.2f%% in the last 24h." % args.threshold)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
