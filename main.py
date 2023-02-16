import arel
import sqlite3
import config
from datetime import date, timedelta
from numpy import row_stack
from alpaca_trade_api import REST, TimeFrame
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

if _debug := True:  # os.getenv("DEBUG")
    hot_reload = arel.HotReload(paths=[arel.Path(".")])
    app.add_websocket_route("/hot-reload", route=hot_reload, name="hot-reload")
    app.add_event_handler("startup", hot_reload.startup)
    app.add_event_handler("shutdown", hot_reload.shutdown)
    templates.env.globals["DEBUG"] = _debug
    templates.env.globals["hot_reload"] = hot_reload

# Temporary setup
today = date.today()
n_days_ago = today - timedelta(days=3)

@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)
    
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
      cursor.execute("""
      SELECT * FROM (SELECT symbol, name, stock_id, max(close), date FROM stock_price JOIN stock ON 
      stock_price.stock_id = stock.id
      GROUP BY stock_id
      ORDER BY symbol) WHERE date = ?
      """, (n_days_ago.isoformat(),))
    else:
      cursor.execute("""
        SELECT symbol, name FROM stock ORDER BY symbol
      """)

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def index(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
      SELECT * FROM stock WHERE symbol = ?
    """, (symbol,))

    row = cursor.fetchone()

    SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    cursor.execute("""
    """, (row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars":prices})