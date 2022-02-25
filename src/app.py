import time
import smtplib
import requests
from decouple import config
from bs4 import BeautifulSoup
from email.message import EmailMessage

while True:
    print("-------------------------------- Last check: " + time.ctime() + "--------------------------------")

    response = requests.get(config('PRODUCT_URL'))
    body = response.content

    soup = BeautifulSoup(body, 'lxml')

    product_cart = soup.find('div', class_='product-add-to-cart')

    out_stock = product_cart.find('div', class_='out-of-stock')

    if not out_stock:
        message = EmailMessage()
        message['Subject'] = config('MAIL_SUBJECT')
        message['From'] = config('MAIL_FROM_ADDRESS')
        message['To'] = config('MAIL_TO_ADDRESS')
        message.set_content('epaaaa loco')

        mail_server = smtplib.SMTP_SSL(config('MAIL_HOST'), int(config('MAIL_PORT')))
        mail_server.login(config('MAIL_USERNAME'), config('MAIL_PASSWORD'))
        mail_server.send_message(message)
        mail_server.quit()
    time.sleep(int(config('CHECKER_FREQUENCY')))
