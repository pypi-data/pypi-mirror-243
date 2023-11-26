#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""coll filter"""

import os
import math
from enum import Enum
from typing import Iterable, Tuple, List, Mapping, Collection, Generic, TypeVar

U = TypeVar('U')
T = TypeVar('T')


class CFType(Enum):
    UCF = 'ucf'
    ICF = 'icf'


def default_similar_func(items: List, other: List) -> float:
    """两个item并集数

    以用户相似度为例，遍历item_users，每行用户间拥有共同的item，避免遍历userTtems大量用户间没有共同的item：
    item1: user1, user2, user3

    user1和user2共同有item1:
    user1: item1, item2, item3
    user2: item1, item4, item5

    传入此方法的参数为:
    items: [item1, item2, item3]
    other: [item1, item4, item5]
    """
    return 1.0 / float(len(set(items + other)))


def sqrt_similar_func(items: List, other: List) -> float:
    """两个item数相乘开根"""
    return 1.0 / math.sqrt(len(items) * len(other))


class CollFilter(Generic[U, T]):

    def __init__(self, data: Iterable[Tuple[U, T, float]], parallel_num=2 * os.cpu_count(), similar_func=default_similar_func):
        if parallel_num > 1:
            from cf.pool_coll_filter import PoolCollFilter
            self.coll_filter = PoolCollFilter(data, parallel_num, similar_func)
        else:
            from cf.base import BaseCollFilter
            self.coll_filter = BaseCollFilter(data, similar_func)

    def user_cf(self, recall_num=64,
                similar_num=256,
                user_ids: Collection[U] = None,
                user_similar: Mapping[U, Mapping[U, float]] = None
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        用户协同过滤
        @param recall_num  每个用户最大召回个数
        @param similar_num  每个用户最大相似用户个数
        @param user_ids  要推荐的用户列表
        @param user_similar  用户相似矩阵
        @return {userTd: [(item, score),],}
        """
        return self.coll_filter.user_cf(recall_num, similar_num, user_ids, user_similar)

    def item_cf(self, recall_num=64,
                similar_num=256,
                user_ids: Collection[U] = None,
                item_similar: Mapping[T, Mapping[T, float]] = None
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        物品协同过滤
        @param recall_num  每个用户最大召回个数
        @param similar_num  每个物品最大相似物品个数
        @param user_ids  要推荐的用户列表
        @param item_similar  物品相似矩阵
        @return {userTd: [(item, score),],}
        """
        return self.coll_filter.item_cf(recall_num, similar_num, user_ids, item_similar)

    def user_similar(self, similar_num=256) -> Mapping[U, List[Tuple[U, float]]]:
        """
        用户相似矩阵
        """
        return self.coll_filter.cal_similar(CFType.UCF, similar_num)

    def item_similar(self, similar_num=256) -> Mapping[T, List[Tuple[T, float]]]:
        """
        物品相似矩阵
        """
        return self.coll_filter.cal_similar(CFType.ICF, similar_num)

    def release(self):
        self.coll_filter.release()
