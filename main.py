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

