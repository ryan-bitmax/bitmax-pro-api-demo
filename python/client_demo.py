#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20201117
# @Author  : ryan

from BitMaxService import BitMaxCli
from pprint import pprint
from itertools import count
from time import sleep
import threading
import time

cli=BitMaxCli("../config_staging.json")

# pprint(cli.query_pub_assets())
#
# pprint(cli.query_pub_products())
#
# pprint(cli.query_pub_depth("BTC/USDT"))
#
# pprint(cli.query_pub_ticker("BTC/USDT"))
#
# pprint(cli.query_pub_trades("BTC/USDT", 1))

# pprint(cli.order_cancel_all())

# for i in range(70):
#     pprint(cli.order_new("cash", "BTC/USDT", "7200", "0.001", "limit", "sell", "ACCEPT", "GTC"))

# pprint(cli.get_open_orders(symbol='BTC/USDT'))

# pprint(cli.get_order_status(order_id='r176f5fef88cU3792951278sbtcukv94'))

# pprint(cli.query_prv_order_hist_v2(symbol='BTC-PERP'))

# pprint(cli.query_prv_account_info())
#
# pprint(cli.query_prv_balance())

def test_apis(id):
    print(f"{id} starts calling APIs ...")
    for i in count(1):
        print(id, 'iter', i)
        cli.query_prv_order_hist_v2()
        # cli.query_pub_market_data()['code']
        # cli.query_pub_market_data(isApi=False, symbol='BTC-PERP')
        # cli.query_pub_funding_rates(isApi=False, symbol='BTC-PERP', page=1, pageSize=1)
        cli.query_pub_funding_rates(symbol='BTC-PERP', page=1, pageSize=1)
        # cli.query_pub_ref_price()
        # cli.query_pub_ref_price(isApi=False)
        cli.query_pub_assets()
        cli.query_pub_products()
        cli.order_new("cash", "BTC/USDT", "7100", "0.001", "limit", "buy", "ACCEPT", "GTC")
        cli.query_pub_depth("BTC/USDT")
        cli.query_pub_ticker("BTC/USDT")
        cli.query_pub_trades("BTC/USDT", 1)
        orderId=cli.order_new("cash", "BTC/USDT", "7200", "0.001", "limit", "sell", "ACCEPT", "GTC")['data']['info']['orderId']
        cli.get_open_orders(symbol='BTC/USDT')
        cli.order_cancel_all()
        cli.get_order_status(order_id=orderId)
        cli.query_prv_account_info()
        cli.query_prv_balance()
        sleep(0.1)
        i+=1

try:
    for j in range(20):
        threading.Thread(target=test_apis, args=("thread %d"%j,)).start()
        sleep(0.2)
except:
    print("Error: unable to start thread")
