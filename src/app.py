from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from os import environ
from utils.exchange_rate import get_usd_rate
from utils.resubscribe import resubscribe
from utils.sheets_wrapper import get_sheet

app = Flask(__name__)
update_path = environ.get("channel_path")
update_headers = {"update", "sync", "change"}


@app.route("/")
def index():
    return str(usdrate) + str(data)


@app.route(update_path, methods=["POST"])
def update():
    # X-Goog-Channel-Id: bc127763-1ed4-4796-b7ea-c5ce9574fa93
    # X-Goog-Channel-Expiration: Fri, 15 Jul 2022 18:06:18 GMT
    # X-Goog-Resource-State: update
    # X-Goog-Changed: content
    # X-Goog-Message-Number: 3236479
    # X-Goog-Resource-Id: jv2sI78Oz0nntsXBXfHxhJYS0Ig
    # X-Goog-Resource-Uri: https://www.googleapis.com/drive/v3/files/1oy13To3eyYlNDEs49TekBWFBKLycmoq0-wAjl2kEOdY?acknowledgeAbuse=false&alt=json&supportsAllDrives=false&supportsTeamDrives=false&alt=json
    # User-Agent: APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)
    # Accept-Encoding: gzip, deflate, br

    # print(request.headers, flush=True)
    global data
    if request.headers.get("X-Goog-Resource-State") in update_headers:
        data = get_sheet()
    return "xd"


data = None
usdrate = -1


def update_exchange_rate():
    global usdrate
    usdrate = get_usd_rate()


if __name__ == "__main__":
    update_exchange_rate()
    resubscribe()
    scheduler = BackgroundScheduler()
    scheduler.add_job(resubscribe, "interval", minutes=50)
    scheduler.add_job(
        update_exchange_rate, "interval", hours=24
    )  # TODO hide in a db, update at noon
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
