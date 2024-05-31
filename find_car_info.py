import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from re import match


def find_phone_number(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)
    driver.get(url)

    phone_number = None

    driver.execute_script("window.scrollBy(0, 750)")
    search_box = driver.find_element(By.CSS_SELECTOR, 'span.phone')
    search_box.click()

    phone_number_element = driver.find_element(By.CSS_SELECTOR, '.popup-successful-call-desk')
    phone_number = phone_number_element.get_attribute('textContent')
    driver.quit()
    if not phone_number:
        phone_number = 'Do not found'

    return phone_number


def valid_car_number(car_number):
    pattern = r'^[A-Z]{2} \d{4} [A-Z]{2}$'
    is_valid = match(pattern, car_number)
    if is_valid is not None:
        if is_valid:
            return car_number
    return 'Do not found'


def fetch_car_data_from_page(used_car_url):
    response = requests.get(used_car_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    search_results = soup.find_all('div', class_='content')
    results = []

    for result in search_results:
        url = result.find('a', class_='address')['href']

        response = requests.get(url)
        car_inf = BeautifulSoup(response.content, 'html.parser')

        price_usd = car_inf.find('div', class_='price_value').find('strong', class_='').text

        try:
            odometer_label = car_inf.find('span', class_='label', text='Пробіг від продавця')
            odometer = odometer_label.find_next('span', class_='argument').text.strip()
        except AttributeError:
            odometer = car_inf.find('span', class_='label', text='Пробіг').find_next('span',
                                                                                     class_='argument').text.strip()

        try:
            username = car_inf.find('section', id='userInfoBlock').find('div', 'seller_info_name bold').text
        except AttributeError:
            username = 'Company: ' + car_inf.find('h4', class_='seller_info_name').find('a').text

        phone_number = find_phone_number(url)

        image_url = car_inf.find('span', class_='seller_info_img').find('img', class_='img')['src']

        images_count = len(car_inf.find('div', id='photosBlock').find_all('div', class_='photo-620x465'))

        try:
            car_number = valid_car_number(car_inf.find('div', class_='t-check').text[1:11])
        except AttributeError:
            car_number = 'Do not found'

        try:
            vin_element = car_inf.find('div', class_='t-check').find('span', class_='label-vin')
            if vin_element:
                car_vin = vin_element.text.strip()[:17]
            else:
                vin_element = car_inf.find('span', class_='vin-code')
                car_vin = vin_element.text.strip()[:17] if vin_element else 'VIN not found'
        except AttributeError:
            car_vin = 'Do not found'

        results.append({
            'url': url,
            'price_usd': price_usd,
            'odometer': odometer,
            'username': username,
            'phone_number': phone_number,
            'image_url': image_url,
            'images_count': images_count,
            'car_number': car_number,
            'car_vin': car_vin,
        })
    return results


def fetch_car_data_from_site():
    count = 0
    results = []
    while True:
        url = f'https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page={count}&size=20&scrollToAuto=36549938'
        data = fetch_car_data_from_page(url)
        if len(data) == 0:
            return results
        results.extend(data)
        count += 1
