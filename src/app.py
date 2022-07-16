from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from os import environ
from utils.exchange_rate import get_usd_rate
from utils.resubscribe import resubscribe
from utils import models
from utils.db import engine
from utils.db import Base
from utils.wrappers import load_data, save_data

app = Flask(__name__)
update_path = environ.get("channel_path")
update_headers = {"update", "sync", "change"}


@app.route("/")
def index():
    return "\n".join([str(i)+'\t' for i in load_data()])


@app.route(update_path, methods=["POST"])
def update():
    if request.headers.get("X-Goog-Resource-State") in update_headers:
        save_data()
    return "thanks"


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    update_mode = environ.get("update_mode")
    update_mode = 'pull'
    if update_mode not in {'push', 'pull'}:
        raise ValueError
    if update_mode == 'push':
        resubscribe()
        scheduler.add_job(resubscribe, "interval", minutes=50)
    elif update_mode == 'pull':
        scheduler.add_job(save_data, "interval", seconds=2)
    scheduler.start()

    # create table
    Base.metadata.create_all(engine)
    save_data()
    print('print loaddata')
    print(load_data())

    app.run(host="0.0.0.0", port=5000, debug=True)
