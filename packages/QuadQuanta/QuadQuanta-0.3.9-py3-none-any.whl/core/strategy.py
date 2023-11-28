#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   strategy.py
@Time    :   2021/05/14
@Author  :   levonwoo
@Version :   0.2
@Contact :   
@License :   (C)Copyright 2020-2021
@Desc    :   None
'''

import numpy as np
from src.data.get_data import get_bars
from src.portfolio.account import Account
from src.utils.logs import logger
from tqdm import tqdm


class BaseStrategy():
    """
    策略基类
    """
    def __init__(self,
                 code=None,
                 start_date=None,
                 end_date=None,
                 frequency='daily',
                 username='quadquanta',
                 passwd='quadquanta',
                 model='backtest',
                 init_cash=100000,
                 account_id=None,
                 mongo_db='QuadQuanta',
                 mongo_col='account',
                 solid=False):
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.code = code
        self.sys_init()
        self.init()
        self.acc = Account(
            username,
            passwd,
            model,
            init_cash,
            account_id,
            mongo_db,
            mongo_col,
            solid,
        )

    def sys_init(self):
        """
        系统初始化
        """
        # 初始化时加载日线数据
        logger.info("加载数据中...")
        self.day_data = get_bars(self.code, self.start_date, self.end_date, self.frequency)
        logger.info("数据加载完成")
        if self.code:
            self.subscribe_code = self.code
        else:
            self.subscribe_code = np.unique(self.day_data['code']).tolist()
        self.trading_date = np.sort(np.unique(self.day_data['date']))
        self.trading_datetime = np.sort(np.unique(self.day_data['datetime']))

    def init(self):
        """
        自定义初始化
        Returns
        -------

        """
        raise NotImplementedError

    def on_bar(self, bars):
        """
        策略函数
        """
        raise NotImplementedError

    def on_tick(self, tick):
        raise NotImplementedError

    def syn_backtest(self):
        """
        日线回测逻辑

        """
        for i in tqdm(range(0, len(self.trading_date))):
            date = self.trading_date[i]
            self.today_data = self.day_data[self.day_data['date'] == date]
            self.on_bar(self.today_data)


if __name__ == '__main__':
    strategy = BaseStrategy(code='000001',
                            start_date='2014-01-01',
                            end_date='2014-01-10',
                            frequency='day')
    strategy.syn_backtest()
