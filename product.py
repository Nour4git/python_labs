import requests
from bs4 import BeautifulSoup
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

SENDER_EMAIL = 'nour@gmail.com' 
SENDER_PASSWORD = 'nour' 
RECEIVER_EMAIL = 'nourda@gmail.com'  

TARGET_PRICE = 100 

conn = sqlite3.connect('product_prices.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products
             (name TEXT, url TEXT, current_price REAL, last_checked TIMESTAMP)''')

def send_email(product_name, product_url, price):
    """Send email notification when price drops below the target price."""
    subject = f"Price Drop Alert: {product_name}"
    body = f"The price of {product_name} has dropped to {price}. Visit the link: {product_url}"

=    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        print(f"Price drop alert sent for {product_name}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def track_price(url, product_name):
    """Track the price of the product."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        price = soup.find(id="priceblock_ourprice").get_text() 
    except AttributeError:
        try:
            price = soup.find(id="priceblock_dealprice").get_text() 
        except AttributeError:
            print("Could not retrieve the price.")
            return

    price = float(price.replace('$', '').replace(',', '').strip())
    if price < TARGET_PRICE:
        send_email(product_name, url, price)

    c.execute('INSERT INTO products (name, url, current_price, last_checked) VALUES (?, ?, ?, ?)',
              (product_name, url, price, time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()

def main():
    products_to_track = [
        ("Product 1", "https://www.amazon.com/dp/product_id_1"),
        ("Product 2", "https://www.amazon.com/dp/product_id_2"),
        ("Product 3", "https://www.amazon.com/dp/product_id_3")
    ]

=    for product_name, url in products_to_track:
        track_price(url, product_name)
    
    conn.close()

if __name__ == "__main__":
    main()
