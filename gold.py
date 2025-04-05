import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

def send_telegram_message(message):
    bot_token = '8076360823:AAH9bk5Bewzd3IEU9HZVcvddNniQB8Q6uLY' 
    chat_id = '2104586242'  
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Notification sent to Telegram")
    else:
        print("Failed to send notification to Telegram")

def get_btmc_price():
    url = 'https://btmc.vn/'
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    row = rows[2]
    cells = row.find_all('td')
    if len(cells) > 3:
        gold_price = cells[3].text.strip()
        return f"Bảo Tín: {gold_price}"
    return None

def get_phuquy_price():
    url_phuquy = 'https://phuquygroup.vn/'
    response = requests.get(url_phuquy)
    response.raise_for_status()  
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    row = rows[2]
    cells = row.find_all('td')
    if len(cells) > 2:
        gold_price = cells[2].text.strip() 
        gold_price = gold_price.replace(',', '')
        gold_price = int(gold_price) / 1000  
        return f"Phú Quý: {int(gold_price)}"
    return None

def get_world_gold_price():
    url_world = 'https://giavang.org/the-gioi/'
    response = requests.get(url_world)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')
    price_element = soup.find('span', class_='crypto-price')
    
    if price_element and 'data-price' in price_element.attrs:
        world_gold_price = price_element['data-price']
        return f"Thế giới: {world_gold_price}"
    return None

def job():
    current_time = datetime.now(tz=None).strftime('%H:%M:%S %d/%m/%Y')
    print(f"Running job at: {current_time} (Hanoi Time)")
    btmc_price = get_btmc_price()
    phuquy_price = get_phuquy_price()
    world_gold_price = get_world_gold_price()

    message = f"⏰ {current_time} (Hanoi)\n"

    if btmc_price:
        message += f"🔴 {btmc_price}\n"
    if phuquy_price:
        message += f"❤️ {phuquy_price}\n"
    if world_gold_price:
        message += f"🌍 {world_gold_price}\n"

    send_telegram_message(message)

if __name__ == "__main__":
    schedule.every().day.at("00:45").do(job)
    print("Gold price notification scheduler started. Next run at 00:45 daily (Hanoi Time).")
    while True:
        schedule.run_pending()
        time.sleep(1)
