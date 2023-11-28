#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mongodb_api.py
@Time    :   2021/05/29
@Author  :   levonwoo
@Version :   0.1
@Contact :   
@License :   (C)Copyright 2020-2021
@Desc    :   mongodb数据库API
'''

import pandas as pd
# here put the import lib
import pymongo
from pymongo.errors import DuplicateKeyError
from src.config import config
from src.utils.logs import logger


def query_mongodb(db_name,
                  coll_name,
                  sql=None,
                  uri=config.mongodb_uri,
                  sort_id='_id',
                  sort_type=1,
                  **kwargs):
    """
    mongodb数据库查询

    Parameters
    ----------
    coll_name : str
        集合名
    db_name : str
        数据库名
    sql : dict, optional
        查询语句, by default None, None表示返回所有
    uri : str, optional
        mongodb uri, by default 'mongodb://127.0.0.1:27017'
    sort_id : str
        排序字段
    sort_type :
        排序类型,1表示升序，-1表示降序

    Returns
    -------
    [type]
        format参数指定返回格式, 默认list,'pd'返回pandas.DataFrame

    Raises
    ------
    NotImplementedError
        [description]
    """
    client = pymongo.MongoClient(uri)
    collection = client[db_name][coll_name]
    if kwargs.get('format') == None:
        return list(collection.find(sql).sort(sort_id, sort_type))
    elif kwargs.get('format') in ['pd', 'pandas']:
        return pd.DataFrame(list(collection.find(sql).sort(sort_id, sort_type))).set_index('_id')
    else:
        raise NotImplementedError
    client.close()


def insert_mongodb(db_name, coll_name, documents, uri=config.mongodb_uri):
    """[summary]

    Parameters
    ----------
    db_name : str
        [description]
    coll_name : str
        集合名
    documents : list or dict
        文档列表
    uri : str, optional
        mongodb uri, by default 'mongodb://127.0.0.1:27017'
    """
    client = pymongo.MongoClient(uri)
    collection = client[db_name][coll_name]
    try:
        if isinstance(documents, list):
            collection.insert_many(documents)
        elif isinstance(documents, dict):
            collection.insert_one(documents)
        else:
            raise NotImplementedError
    except DuplicateKeyError:
        logger.warning(DuplicateKeyError)
    except Exception as e:
        logger.warning(e)
    client.close()


def save_mongodb(db_name, coll_name, document, uri=config.mongodb_uri):
    """
    保存mongodb数据库，主键存在就更新，不存在就插入

    Parameters
    ----------
    db_name : str
        [description]
    coll_name : str
        集合名
    documents : list
        文档
    uri : str, optional
        mongodb uri, by default 'mongodb://127.0.0.1:27017'
    """
    client = pymongo.MongoClient(uri)
    collection = client[db_name][coll_name]
    try:
        if isinstance(document, dict):
            collection.save(document)
        else:
            raise NotImplementedError
    except Exception as e:
        logger.warning(e)
    client.close()


if __name__ == '__main__':
    data = query_mongodb('QuadQuanta', 'N_limit')
    print(data[0])
