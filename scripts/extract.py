import requests


def extract_crypto():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    crypto_data = extract_crypto()
    for crypto in crypto_data:
        print(crypto['id'], crypto['name'], crypto['current_price'], crypto['market_cap'], crypto['market_cap_rank'], crypto['total_volume'], crypto['high_24h'], crypto['low_24h'], crypto['price_change_percentage_24h'], crypto['last_updated'])