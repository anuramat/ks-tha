from utils import models
from utils.db import engine
from utils.db import Base
# create table
Base.metadata.create_all(engine)
# create session
from sqlalchemy.orm import Session
# create stuff
from datetime import date
with Session(engine) as session:
    firstrow = models.Order(
            pseudo_id = 123,
            order_id = 234,
            usd_price = 100,
            rur_price = 5000,
            deadline = date(2020,1,15),
            )
    session.add_all([firstrow])
    session.commit()
# read stuff
from sqlalchemy import select
stmt = select(models.Order)
for order in session.scalars(stmt):
    print(order)

