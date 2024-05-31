from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CarInfo(Base):
    __tablename__ = 'car_info'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    title = Column(String(255), nullable=False)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String(255))
    phone_number = Column(String(20))
    image_url = Column(String(255))
    images_count = Column(Integer)
    car_number = Column(String(20))
    car_vin = Column(String(17))
    datetime_found = Column(DateTime, nullable=False, default=datetime.utcnow)
