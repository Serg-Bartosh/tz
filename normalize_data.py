import logging
from re import search
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def normalize_data(data):
    normalized_data = []
    for item in data:
        normalized_item = {
            'url': item.get('url', ''),
            'price_usd': normalize_price(item.get('price_usd')),
            'odometer': normalize_odometer(item.get('odometer')),
            'username': item.get('username', ''),
            'phone_number': normalize_phone_number(item.get('phone_number', '')),
            'image_url': item.get('image_url', ''),
            'images_count': item.get('images_count', 0),
            'car_number': item.get('car_number', ''),
            'car_vin': item.get('car_vin', ''),
        }
        normalized_data.append(normalized_item)
    return normalized_data


def normalize_price(price):
    if price:
        price = price.replace('$', '').replace(' ', '').replace(',', '')
        if 'грн' in price:
            price = price.replace('грн', '')
            try:
                return int(price) / 40
            except ValueError:
                logging.error(f"Failed to normalize price: {price}")
                return None
        else:
            try:
                return int(price)
            except ValueError:
                logging.error(f"Failed to normalize price: {price}")
                return None
    logging.error(f"Price is not exist")
    return None


def normalize_odometer(odometer):
    if odometer:
        match = search(r'\b(\d+)\b', odometer)
        if match:
            return int(match.group(1)) * 1000
        else:
            logging.error(f"Failed to normalize odometer: {odometer}")
    logging.error(f"Odometer is not exist")
    return None


def normalize_phone_number(phone_number):
    if phone_number:
        return phone_number.replace('(', '').replace(')', '').replace(' ', '')
    logging.error(f"Phone_number is not exist or is invalid")
    return None
