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
    sql_rows = load_data()
    header_row = (
            'pseudo_id',
            'order_id',
            'usd_price',
            'rur_price',
            'deadline'
            )
    rows=[]
    for row in sql_rows:
        rows.append((
            row.pseudo_id,
            row.order_id,
            row.usd_price,
            f'{row.rur_price:.2f}',
            row.deadline
            ))
    head = ''
    head += f'<thead><tr>{"".join(["<th>"+i+"</th>" for i in header_row])}</tr></thead>'
    body = ''
    for row in rows:
        body += f'<tr>{"".join(["<th>"+str(i)+"</th>" for i in row])}</tr>'
    body = f'<tbody>{body}<tbody>'
    return f'<table>{head+body}</table>'

@app.route(update_path, methods=["POST"])
def update():
    if request.headers.get("X-Goog-Resource-State") in update_headers:
        save_data()
    return "thanks"


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    update_mode = environ.get("update_mode")
    update_mode = 'pull'
    if update_mode == 'push':
        resubscribe()
        scheduler.add_job(resubscribe, "interval", minutes=50)
    elif update_mode == 'pull':
        scheduler.add_job(save_data, "interval", seconds=2)
    else:
        raise ValueError
    scheduler.start()

    # create table
    Base.metadata.create_all(engine)
    save_data()
    print('print loaddata')
    print(load_data())

    app.run(host="0.0.0.0", port=5000, debug=True)
