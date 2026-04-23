import pandas as pd
import datetime as dt
import extract as e


def transform_crypto(crypto_data):
    df = pd.DataFrame(crypto_data)
    df = df[['id', 'name', 'current_price', 'market_cap', 'market_cap_rank', 'total_volume', 'high_24h', 'low_24h', 'price_change_percentage_24h', 'last_updated']]
    df.columns = ['id', 'name', 'current_price_usd', 'market_cap_usd', 'market_cap_rank', 'total_volume_usd', 'high_24h_usd', 'low_24h_usd', 'price_change_percentage_24h', 'last_updated']
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['last_updated'] = df['last_updated'].dt.date
    df['price_change_percentage_24h'] = df['price_change_percentage_24h'].round(2)

    return df

if __name__ == "__main__":
    crypto_data = e.extract_crypto()
    crypto_df = transform_crypto(crypto_data)
    print(crypto_df)
