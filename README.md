# Scraper Auto Ria

Opensource scraper

## Instructions for use

1) Download the project

2) Create a postgres database

3) Fill out the .env file

4) Paste ```pip install -r requirements.txt``` in ur terminal 

Project structure
===========
1) dumps folder, where dumps will be saved in dump-date- format
2) Models where the model of our table is described
3) ```find_car_info.py``` , where the functions ```fetch_car_data_from_page()```, ```valid_car_number()```, ```find_phone_number()```, ```fetch_car_data_from_site()``` are located
```fetch_car_data_from_site()``` - function that transfers links to pages that need to be parsed
```fetch_car_data_from_page()``` - page parsing
```valid_car_number()``` - in order to remove unnecessary information from the answer
```find_phone_number()``` - launches drivers to imitate a person to open a phone number
4) ```main.py``` - using ```load_data_to_db()``` we create migrations to the database, ```daily_task()``` parses the page and dumps the database, ```schedule.every().day.at("15:30").do(daily_task)``` makes all this run every day at the same time
5) normalize_data.py was created to convert data to the desired type
