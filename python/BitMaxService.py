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
              "\n  --host", self.__host,
              "\n  --group", self.__group,
              "\n  --apikey", self.__apikey[:5].ljust(10, "*"),
              "\n  --secret", self.__secret[:6].ljust(15, "*"), )

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
            "symbol": symbol,
            "interval": interval,
        }
        if frm: params['frm'] = frm
        if to: params['to'] = to
        if n: params['n'] = n

        res = requests.get(url, params=params)
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

    def query_pub_funding_rates(self, isApi=True, symbol='BTC-PERP', page=1, pageSize=20):
        url = f"{self.__host}/{ROUTE_PREFIX}/futures/funding-rates" if isApi \
            else f"{self.__host}/api/t/futures/funding-rates"
        params = dict(symbol=symbol,
                      page=page,
                      pageSize=pageSize)

        res = requests.get(url, params=params)
        return parse_response(res)

    def query_pub_ref_price(self, isApi=True, symbol=None):
        url = f"{self.__host}/{ROUTE_PREFIX}/futures/ref-px" if isApi else f"{self.__host}/api/t/futures/ref-px"
        params = dict()
        if symbol: params['symbol'] = symbol
        res = requests.get(url, params=params)
        return parse_response(res)

    def query_pub_market_data(self, isApi=True, symbol=None):
        url = f"{self.__host}/{ROUTE_PREFIX}/futures/market-data" if isApi else f"{self.__host}/api/t/futures/market-data"
        params = dict()
        if symbol: params['symbol'] = symbol
        res = requests.get(url, params=params)
        return parse_response(res)

    '''
    ======================
    Order API
    ======================
    '''
    def order_new(self, account, symbol, price, qty, order_type, side, resp_inst, time_in_force):
        url = f"{self.__host}/{self.__group}/api/pro/v1/{account}/order"

        ts = utc_timestamp()

        order = dict(
            id=uuid32(),
            time=ts,
            symbol=symbol.replace("-", "/"),
            orderPrice=str(price),
            orderQty=str(qty),
            orderType=order_type,
            side=side.lower(),
            timeInForce=time_in_force,
            respInst=resp_inst,
        )

        headers = make_auth_headers(ts, "order", self.__apikey, self.__secret)
        res = requests.post(url, headers=headers, json=order)
        return parse_response(res)

    def order_query(self):
        pass

    def order_cancel(self):
        pass

    def order_cancel_all(self, account="cash", symbol=None):

        method = "order/all"

        url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}/{method}"

        params = {}
        if symbol:  params["symbol"] = symbol

        ts = utc_timestamp()
        headers = make_auth_headers(ts, method, self.__apikey, self.__secret)

        res = requests.delete(url, headers=headers, json=params)
        return parse_response(res)

    def query_prv_order_hist_v2(self, account="cash", symbol=None, start_time=None, end_time=None, seq_num=None,
                                limit=None):

        url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX_V2}/order/hist"

        ts = utc_timestamp()
        headers = make_auth_headers(ts, "order/hist", self.__apikey, self.__secret)
        params = dict(
            account=account,
        )
        if symbol: params['symbol'] = symbol
        if start_time: params['startTime'] = start_time
        if end_time: params['endTime'] = end_time
        if seq_num: params['seqNum'] = seq_num
        if limit: params['limit'] = limit

        res = requests.get(url, headers=headers, params=params)
        return parse_response(res)

    def get_hist_orders(self, symbol, start_time, end_time, order_type, side, account="cash",
                        method="order/hist/current"):
        base_url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}"
        ts = utc_timestamp()
        url = "{}/{}".format(base_url, method)
        headers = make_auth_headers(ts, method, self.__apikey, self.__secret)
        params = {"symbol": symbol, "startTime": start_time, "endTime": end_time, "orderType": order_type, "side": side}
        res = requests.get(url, headers=headers, params=params)
        return parse_response(res)

    def get_open_orders(self,  symbol, account="cash", method="order/open"):
        base_url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}"
        ts = utc_timestamp()
        url = "{}/{}".format(base_url, method)
        headers = make_auth_headers(ts, method, self.__apikey, self.__secret)
        params = {"symbol": symbol}
        res = requests.get(url, headers=headers, params=params)
        return parse_response(res)

    def get_order_status(self, order_id, account="cash", method="order/status"):
        base_url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}"
        url = "{}/{}".format(base_url, method, order_id)
        ts = utc_timestamp()
        headers = make_auth_headers(ts, method, self.__apikey, self.__secret)
        res = requests.get(url, headers=headers, params={"orderId": order_id})
        return parse_response(res)

    '''
    ======================
    Account API
    ======================
    '''

    def query_prv_account_info(self):
        ts = utc_timestamp()
        headers = make_auth_headers(ts, "info", self.__apikey, self.__secret)
        url = f"{self.__host}/{ROUTE_PREFIX}/info"

        res = requests.get(url, headers=headers)
        return parse_response(res)

    def query_prv_balance(self, asset=None, account='cash', show_all=False):
        ts = utc_timestamp()
        if account=="futures":
            headers = make_auth_headers(ts, "futures/collateral-balance", self.__apikey, self.__secret)
            url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}/collateral-balance"
        else:
            headers = make_auth_headers(ts, "balance", self.__apikey, self.__secret)
            url = f"{self.__host}/{self.__group}/{ROUTE_PREFIX}/{account}/balance"
        params = dict(showAll=show_all)
        if asset: params['asset'] = asset

        res = requests.get(url, headers=headers, params=params)
        return parse_response(res)
