from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from os import environ
from utils.exchange_rate import get_usd_rate
from utils.resubscribe import resubscribe
from utils import models
from utils.db import engine

app = Flask(__name__)
update_path = environ.get("channel_path")
update_headers = {"update", "sync", "change"}


@app.route("/")
def index():
    return 'nothing here yet...' # read table from db TODO


@app.route(update_path, methods=["POST"])
def update():
    if request.headers.get("X-Goog-Resource-State") in update_headers:
        pass # read sheet, save to db TODO
    return 'thanks'


if __name__ == "__main__":
    resubscribe()
    scheduler = BackgroundScheduler()
    scheduler.add_job(resubscribe, "interval", minutes=50)
    scheduler.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
