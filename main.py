import os
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv


load_dotenv()
URL : str = os.getenv('URL') or ''
MY_EMAIL : str = os.getenv('MY_EMAIL') or ''
PASSWORD : str = os.getenv('MY_PASS') or ''
TO_EMAIL : str = os.getenv('TO_EMAIL') or ''
TARGET = 120000
HEADERS = {
    'accept-language' : 'en-US,en;q=0.7',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
    }

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, 'html.parser')

# pprint(soup)

product = soup.find(id="productTitle").get_text(strip=True)
price_s = soup.select_one('span.a-price-whole').get_text('',True)

# print(product)
# print(price_s)
digits = ''.join(c for c in price_s if c.isdigit())
price = int(digits) if digits else 0

# print(price)
from email.message import EmailMessage
import smtplib

if price < TARGET:
    msg = EmailMessage()
    msg["Subject"] = "AMAZON PRICE ALERT!"
    msg["From"] = MY_EMAIL
    msg["To"] = TO_EMAIL

    msg.set_content(
        f"""
The product:

{product}

has fallen below your target price.

Current Price: ₹{price}
Target Price: ₹{TARGET}

Product Link:
{URL}
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)

        print("Sending email...")
        connection.send_message(msg)
        print("Email sent!")

else:
    print("Not low enough price!")
