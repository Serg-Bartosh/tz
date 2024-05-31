import schedule
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.car_info import CarInfo
from normalize_data import normalize_data
from find_car_info import fetch_car_data_from_site
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

dotenv_path = '.env'
load_dotenv(dotenv_path)

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
CarInfo.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def load_data_to_db(data):
    session = Session()
    try:
        for item in data:
            logging.info(f"Loading data to database: {item}")
            car_info = CarInfo(
                url=item['url'],
                title='',
                price_usd=item['price_usd'],
                odometer=item['odometer'],
                username=item['username'],
                phone_number=item['phone_number'],
                image_url=item['image_url'],
                images_count=item['images_count'],
                car_number=item['car_number'],
                car_vin=item['car_vin']
            )
            session.add(car_info)
        session.commit()
        logging.info("Data loaded successfully!")
    except Exception as e:
        session.rollback()
        logging.error(f"Error loading data to database: {e}")
    finally:
        session.close()


def daily_task():
    current_date = datetime.now()
    dump_file_path = f"dump/dump_file{current_date.strftime('%d.%m.%Y')}.sql"
    dump_command = f'pg_dump -U {db_user} -h {db_host} -p {db_port} {db_name} > {dump_file_path}'
    logging.info("Fetching car data fromexists site...")
    data = fetch_car_data_from_site()
    normalized_data = normalize_data(data)
    logging.info("Loading data to database...")
    load_data_to_db(normalized_data)
    logging.info("Data loaded successfully!")
    subprocess.run(dump_command, shell=True)


schedule.every().day.at("15:30").do(daily_task)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(5)
