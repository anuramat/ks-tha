from utils import models
from decimal import Decimal
from utils.db import engine
from utils.db import Base
from sqlalchemy import select
from utils.db import Session
from datetime import date
from utils.data import get_data
from utils.exchange_rate import get_usd_rate

def 
# read stuff
def load_data():
    """
    Reads rows from db
    """
    with Session() as session:
        statement = select(models.Order)
        result = session.execute(statement).all()
    # TODO

def save_data():
    """
    Polls spreadsheet from google sheets,
    saves spreadsheet to db
    """
    spreadsheet_rows = get_data()
    usd_rate = get_usd_rate()
    # ['№', 'заказ №', 'стоимость,$', 'срок поставки'], ['1', '1249708', '675', '24.05.2021']
    with Session() as session:
        for row in spreadsheet_rows[1:]:
            db_row = models.Order(
                pseudo_id=int(row[0]),
                order_id=int(row[1]),
                usd_price=float(row[2]),
                rur_price=float(int(usd_rate) * row[2]),
                deadline=date(*[int(i) for i in row[3].split(".")[::-1]]),
            )
            session.add(db_row)
        session.commit()

def delete_data():
    with Session() as session:
        session.query(models.Order).delete()
        session.commit()
