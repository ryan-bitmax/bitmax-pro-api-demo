#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20201117
# @Author  : ryan

from BitMaxService import BitMaxCli
from pprint import pprint

cli=BitMaxCli("../config_prod.json")

# pprint(cli.query_pub_assets())
#
# pprint(cli.query_pub_products())

# pprint(cli.query_pub_barhist("BTC/USDT","1",n=2))

# pprint(cli.query_pub_depth("BTC/USDT"))

# pprint(cli.query_pub_ticker("BTC/USDT"))

# pprint(cli.query_pub_trades("BTC/USDT", 1))