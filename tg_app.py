import requests
import time
from datetime import datetime

#url
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/i8-eSIwhtP2ftDetg-aGzgTb4kj7TpMtLLfM7HGopBD'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_webhooks_event = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_webhooks_event, json=data)

def format_bitcoin_dict(bitcoin_dict):
    rows = []
    for bitcoin_price in bitcoin_dict:
        date = bitcoin_price['date'].strftime('%d.%m.%Y. %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date,price)
        rows.append(row)

    return '<br>'.join(rows)

BITCOIN_PRICE_THRESHOLD = 10000

def main():
    bitcoin_dict = []
    cur = 0

    while 1:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_dict.append({'date': date, 'price': price})

        if price < BITCOIN_PRICE_THRESHOLD & cur != 1:
            cur = 1
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_dict) == 6:
            post_ifttt_webhook('bitcoin_price_update',
                                format_bitcoin_dict(bitcoin_dict))
            bitcoin_dict = []
        time.sleep(60*60)

if __name__ == '__main__':
    main()
