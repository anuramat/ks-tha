from sqlalchemy import Column, Integer, Date, Numeric, Float
from utils.db import Base
money_type = Float
class Order(Base):
    __tablename__ = "orders"
    real_id = Column(Integer, primary_key=True, nullable=False)
    pseudo_id = Column(Integer, nullable=True)
    order_id = Column(Integer, nullable=True)
    usd_price = Column(money_type, nullable=True)
    rur_price = Column(money_type, nullable=True)
    deadline = Column(Date, nullable=True)
