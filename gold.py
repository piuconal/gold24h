import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os  # Để truy cập environment variables (cho secrets)

def send_telegram_message(message):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    if not bot_token or not chat_id:
        print("Error: Telegram bot token or chat ID not set as environment variables.")
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Notification sent to Telegram")
    else:
        print(f"Failed to send notification to Telegram. Status code: {response.status_code}, Response: {response.text}")

def get_btmc_price():
    url = 'https://btmc.vn/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        if len(rows) > 2:
            row = rows[2]
            cells = row.find_all('td')
            if len(cells) > 3:
                gold_price = cells[3].text.strip()
                return f"Bảo Tín: {gold_price}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTMC price: {e}")
    except Exception as e:
        print(f"Error parsing BTMC price: {e}")
    return None

def get_phuquy_price():
    url_phuquy = 'https://phuquygroup.vn/'
    try:
        response = requests.get(url_phuquy)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        if len(rows) > 2:
            row = rows[2]
            cells = row.find_all('td')
            if len(cells) > 2:
                gold_price = cells[2].text.strip()
                gold_price = gold_price.replace(',', '')
                try:
                    gold_price = int(gold_price) / 1000
                    return f"Phú Quý: {int(gold_price)}"
                except ValueError:
                    print(f"Could not convert Phú Quý price to integer: {gold_price}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Phú Quý price: {e}")
    except Exception as e:
        print(f"Error parsing Phú Quý price: {e}")
    return None

def get_world_gold_price():
    url_world = 'https://giavang.org/the-gioi/'
    try:
        response = requests.get(url_world)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('span', class_='crypto-price')

        if price_element and 'data-price' in price_element.attrs:
            world_gold_price = price_element['data-price']
            return f"Thế giới: {world_gold_price}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching world gold price: {e}")
    except Exception as e:
        print(f"Error parsing world gold price: {e}")
    return None

def main():
    current_time = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    btmc_price = get_btmc_price()
    phuquy_price = get_phuquy_price()
    world_gold_price = get_world_gold_price()

    message = f"{current_time}\n"

    if btmc_price:
        message += f"🔴 {btmc_price}\n"
    if phuquy_price:
        message += f"❤️ {phuquy_price}\n"
    if world_gold_price:
        message += f"🌍 {world_gold_price}\n"

    send_telegram_message(message)

if __name__ == "__main__":
    main()