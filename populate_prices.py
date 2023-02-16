import sqlite3, config
from alpaca_trade_api import REST, TimeFrame
from dotenv import load_dotenv
from os import environ as env

load_dotenv()

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT id,symbol FROM stock")

rows = cursor.fetchall()

symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = REST(env["ALPACA_API_KEY"], env["ALPACA_SECRET_KEY"],
           base_url=config.API_URL)

chunk_size = 1000
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
        
    barsets = api.get_bars(symbol_chunk, TimeFrame.Day, "2022-05-21", "2022-05-23")

    for bar in barsets:
        try:
            print(f"Processing symbol {bar.S}")
            cursor.execute("INSERT INTO stock_price (stock_id,date,open,high,low,close,volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (stock_dict[bar.S], bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
        except Exception as e:
            print(e)

connection.commit()