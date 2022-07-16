from utils import models
from utils.db import engine
from utils.db import Base
from sqlalchemy import select
from utils.db import Session
from datetime import date
from utils.data import get_data
from exchange_rate import get_usd_rate

# read stuff
def load_data():
    """
    Reads rows from db
    """
    results = []
    with Session() as session:
        stmt = select(models.Order)
        for row in session.execute(stmt):
            results.append(row)


def save_data():
    """
    Polls spreadsheet from google sheets,
    saves spreadsheet to db
    """
    spreadsheet_rows = get_data()
    usd_rate = get_usd_rate()
    # ['№', 'заказ №', 'стоимость,$', 'срок поставки'], ['1', '1249708', '675', '24.05.2021']
    with Session() as session:
        db_new_rows = []
        for row in spreadsheet_row[1:]:
            db_row = models.Order(
                pseudo_id=row[0],
                order_id=row[1],
                usd_price=row[2],
                rur_price=usd_rate * row[2],
                deadline=date(*[int(i) for i in xd.split(".")[::-1]]),
            )
        session.add_all(db_new_rows)
        session.commit()
