from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


@app.route("/")
def index():
    return "nothing here..."


@app.route("/update", methods=["POST"])
def result():
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
    print(request.headers.get('X-Goog-Resource-State'), flush=True)
    return 'xd'

def test_job():
    print('testjobdone', flush=True)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(test_job, 'interval', seconds=2)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
