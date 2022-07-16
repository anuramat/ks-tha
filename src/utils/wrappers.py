from utils import models
from utils.db import engine
from utils.db import Base
from sqlalchemy import select
from utils.db import sessionmaker
from datetime import date


# read stuff
def load_data():
    with sessionmaker() as session:
        stmt = select(models.Order)
        for order in session.scalars(stmt):
            print(order)


def save_data():
    with sessionmaker() as session:
        # TODO
        firstrow = models.Order(
            pseudo_id=123,
            order_id=234,
            usd_price=100,
            rur_price=5000,
            deadline=date(2020, 1, 15),
        )
        session.add_all([firstrow])
        session.commit()
