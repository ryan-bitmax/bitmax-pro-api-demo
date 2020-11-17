#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20201117
# @Author  : ryan

import requests
# Local imports
from util import *

class BitMaxCli:

    def __init__(self, config):
        btmx_cfg = load_config(get_config_or_default(config))['bitmax']
        self.__host = btmx_cfg['https']
        self.__group = btmx_cfg['group']
        self.__apikey = btmx_cfg['apikey']
        self.__secret = btmx_cfg['secret']
        print("API configuration:",
              "\n  --host",self.__host,
              "\n  --group",self.__group,
              "\n  --apikey",self.__apikey[:5].ljust(10, "*"),
              "\n  --secret",self.__secret[:6].ljust(15, "*"),)

    '''
    ======================
    Market data API
    ======================
    '''

    def query_pub_assets(self):

        url = f"{self.__host}/{ROUTE_PREFIX}/assets"
        res = requests.get(url)
        return parse_response(res)

    def query_pub_products(self):

        url = f"{self.__host}/{ROUTE_PREFIX}/products"
        res = requests.get(url)
        return parse_response(res)

    def query_pub_barhist(self, symbol, interval, frm=0, to=0, n=0):

        url = f"{self.__host}/{ROUTE_PREFIX}/barhist"
        params = {
            "symbol":   symbol,
            "interval": interval,
        }
        if frm: params['frm']=frm
        if to: params['to']=to
        if n: params['n']=n

        res = requests.get(url, params = params)
        return parse_response(res)

    def query_pub_depth(self, symbol):

        url = f"{self.__host}/{ROUTE_PREFIX}/depth"
        params = dict(symbol=symbol)

        res = requests.get(url, params=params)
        return parse_response(res)

    def query_pub_ticker(self, symbol):

        url = f"{self.__host}/{ROUTE_PREFIX}/ticker"
        params = dict(symbol=symbol)

        res = requests.get(url, params=params)
        return parse_response(res)

    def query_pub_trades(self, symbol, n=10):

        url = f"{self.__host}/{ROUTE_PREFIX}/trades"
        params = dict(symbol=symbol, n=n)

        res = requests.get(url, params=params)
        return parse_response(res)