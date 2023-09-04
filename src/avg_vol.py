import os
import json
from datetime import datetime, time, timedelta
from collections import deque

import matplotlib.pyplot as plt
from dotenv import load_dotenv
import requests

from src.utils import MovingAverages


def download(ticker: str):
    load_dotenv()
    polygon_api_key = os.getenv('POLYGON_API_KEY')
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}'
    url += f'/range/15/minute/2021-09-01/2023-09-01?adjusted=true&sort=asc&limit=50000&apiKey={polygon_api_key}'
    resp = requests.get(url).json()
    with open(f'{ticker.lower()}.json', 'w') as _f:
        json.dump(resp, _f, indent=4)


def check_for_breakouts(stock_data: list[dict]):
    ma_daily = MovingAverages(period=-1)  # no max len
    ma_30_day = MovingAverages()

    prev_bar = stock_data[0]
    for bar in stock_data[1:]:
        # determine times
        cur_dt = datetime.fromtimestamp(bar['t'] / 1000)
        last_dt = datetime.fromtimestamp(prev_bar['t'] / 1000)
        is_new_day = (cur_dt.date() - last_dt.date()).days > 0

        # up daily sums and ma
        p = abs(bar['c'] - bar['o']) / 2
        ma_daily.update(p, bar['v'])

        # EOD CALCS
        if is_new_day:
            print(ma_daily.ma_price, ma_daily.ma_vol)
            ma_daily.reset()

        prev_bar = bar


if __name__ == '__main__':
    with open('../dat/igex.json') as f:
        dat = json.load(f)['results']
        check_for_breakouts(dat)
