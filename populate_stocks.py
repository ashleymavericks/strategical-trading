import sqlite3
import re, config
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
from os import environ as env

load_dotenv()

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row  #to get rows as SQL objects in return while querying, not as a list of tuples
cursor = connection.cursor()

cursor.execute("SELECT symbol, name FROM stock")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]

api = tradeapi.REST(env["ALPACA_API_KEY"], env["ALPACA_SECRET_KEY"],
                    base_url=config.API_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols and not re.match(r'\w*USD\b', asset.symbol):
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name, exchange) VALUES (?, ?, ?)", (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()
