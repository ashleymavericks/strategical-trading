import sqlite3, config

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

cursor.execute("DROP TABLE stock")

cursor.execute("DROP TABLE stock_price")

connection.commit()
