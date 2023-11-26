#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""base_coll_filter, one process"""

import os
import time
import math
from cf.utils import print_cost_time
from cf import default_similar_func, CFType, U, T
from typing import Iterable, Mapping, Tuple, Generic


class BaseCollFilter(Generic[U, T]):

    def __init__(self, data: Iterable[Tuple[U, T, float]], similar_func=default_similar_func):
        self.similar_func = similar_func
        # {user_id: {item_id: rating},}  {item_id: {user_id: rating},}
        self.user_item_ratings, self.item_users = {}, {}
        start_time = time.perf_counter()
        cnt = 0
        for user_id, item_id, score in data:
            cnt += 1
            self._data_process(user_id, item_id, score)

        self.item_users = {item_id: list(set(users)) for item_id, users in self.item_users.items()}
        print_cost_time(f"数据处理, 当前进程: {os.getpid()}, 处理 {cnt} 条记录, "
                        f"user数: {len(self.user_item_ratings)}, item数: {len(self.item_users)}, 耗时", start_time)

    def user_cf(self, recall_num=10, similar_num=256, user_ids=None, user_similar=None):
        """
        用户协同过滤

        @param recall_num  每个用户推荐结果数目
        @param similar_num  用户相似矩阵最大个数
        @param user_ids  要推荐的用户列表
        @param user_similar  用户相似矩阵
        @return {user_id: [(item, score),],}
        """
        if user_similar is None:
            user_similar = self.cal_similar(CFType.UCF, similar_num)
        return self._do_cf(user_ids, user_similar, recall_num, CFType.UCF)

    def item_cf(self, size_per_user=10, similar_num=256, user_ids=None, item_similar=None):
        """
        物品协同过滤

        @param size_per_user  每个用户推荐结果数目
        @param similar_num  物品相似矩阵最大个数
        @param user_ids  要推荐的用户列表
        @param item_similar  物品相似矩阵
        @return {user_id: [(item, score),],}
        """
        if item_similar is None:
            item_similar = self.cal_similar(CFType.ICF, similar_num)
        return self._do_cf(user_ids, item_similar, size_per_user, CFType.ICF)

    def cal_similar(self, cf_type: CFType, similar_num=256):
        """
        计算相似度

        @return dict{:List()}    {user1: {user2: similar}}
        """
        print(f'开始{cf_type.value}相似度计算, similar_num = {similar_num}')
        func_start_time = time.perf_counter()
        dict1, items_list, cal_similar_func = self._get_cal_similar_inputs(cf_type)
        similar = cal_similar_func(dict1, items_list, self.similar_func)
        similar = self._sort_similar(similar, similar_num)
        print_cost_time(f"完成{cf_type.value}相似度计算, 当前进程: {os.getpid()}, 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        return similar

    def release(self):
        del self.user_item_ratings
        del self.item_users

    def _data_process(self, user_id: U, item_id: T, score: float):
        user_item_rating = self.user_item_ratings.get(user_id)
        if user_item_rating:
            user_item_rating[item_id] = user_item_rating.get(item_id, 0) + score
        else:
            self.user_item_ratings[user_id] = {item_id: score}

        item_user_rating = self.item_users.get(item_id)
        if item_user_rating:
            item_user_rating[user_id] = item_user_rating.get(user_id, 0) + score
        else:
            self.item_users[item_id] = {user_id: score}

    @staticmethod
    def _sort_similar(similar: Mapping, similar_num: int):
        for key, item_score in similar.items():
            similar[key] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:similar_num]
        return similar

    def _get_cal_similar_inputs(self, cf_type: CFType):
        if cf_type == CFType.UCF:
            return self.user_item_ratings, self.item_users.values(), self._cal_ucf_similar
        else:
            return self.item_users, self.user_item_ratings.values(), self._cal_icf_similar

    @staticmethod
    def _cal_ucf_similar(dict1: Mapping, items_list: Iterable[Iterable], similar_func):
        start_time = time.perf_counter()
        similar = {}

        for items in items_list:
            if len(items) <= 1:
                continue

            for item1 in items:
                if item1 not in similar:
                    similar[item1] = {}
                for item2 in items:
                    if item1 == item2:
                        continue
                    # 计算两个item间的相似性
                    similar[item1][item2] = similar[item1].get(item2, 0.0) + similar_func(list(dict1.get(item1, {}).keys()), list(dict1.get(item2, {}).keys()))
        print_cost_time(f"\t进程: {os.getpid()}, 生成 {len(similar)} 条记录, 耗时", start_time)
        return similar

    @staticmethod
    def _cal_icf_similar(dict1: Mapping, items_list: Iterable[Iterable], similar_func):
        start_time = time.perf_counter()
        similar = {}

        for items in items_list:
            if len(items) <= 1:
                continue

            for item1 in items:
                if item1 not in similar:
                    similar[item1] = {}
                for item2 in items:
                    if item1 == item2:
                        continue
                    # 计算两个item间的相似性
                    similar[item1][item2] = similar[item1].get(item2, 0.0) + similar_func(dict1.get(item1, []),
                                                                                          dict1.get(item2, []))
        print_cost_time(f"\t进程: {os.getpid()}, 生成 {len(similar)} 条记录, 耗时", start_time)
        return similar

    def _do_cf(self, user_ids, similar_dict, recall_num, cf_type: CFType):
        print(f'开始{cf_type.value}推理, recall_num = {recall_num}')
        func_start_time = time.perf_counter()
        user_items_list = map(lambda x: (x, self.user_item_ratings.get(x, [])), user_ids) if user_ids else self.user_item_ratings.items()

        if cf_type == CFType.UCF:
            cf_result = self._do_user_cf(self.user_item_ratings, similar_dict, user_items_list, recall_num)
        else:
            cf_result = self._do_item_cf(self.user_item_ratings, similar_dict, user_items_list, recall_num)
        print_cost_time(f"完成{cf_type.value}推理, 当前进程: {os.getpid()}, 生成{len(cf_result)}条记录, 总耗时", func_start_time)
        return cf_result

    @staticmethod
    def _do_user_cf(user_item_ratings, similar_dict, user_items_list, recall_num):
        start_time = time.perf_counter()
        result = {}
        for user_id, items in user_items_list:
            item_score = {}  # {item: score}
            # {user_id: [(user_id: similar),],}  用户间的相似度
            user_similar = similar_dict.get(user_id, [])
            for u2, similar in user_similar:  # 遍历相似度用户列表
                user_item_rating = user_item_ratings.get(u2, {})
                for item, rating in user_item_rating.items():  # 逐个获取相似用户的item列表
                    if item in items:  # item不在用户已消费的列表里
                        continue
                    item_score[item] = item_score.get(item, 0.0) + math.sqrt(similar * rating)
            if len(item_score) > 0:
                result[user_id] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:recall_num]
        print_cost_time(f"\t进程: {os.getpid()}, 处理 {len(user_items_list)} 条记录, 生成 {len(result)} 条记录, 耗时", start_time)
        return result

    @staticmethod
    def _do_item_cf(_user_item_ratings, similar_dict, user_items_list, recall_num):
        start_time = time.perf_counter()
        result = {}
        for user_id, item_ratings in user_items_list:
            item_score = {}  # {item: score}
            for item, rating in item_ratings.items():  # 遍历用户已消费的item
                # {item_id: similar,}
                item_similar = similar_dict.get(item, [])
                for item2, similar in item_similar:  # 与用户已消费item相似的item
                    if item2 in item_ratings:
                        continue
                    item_score[item2] = item_score.get(item2, 0.0) + math.sqrt(similar * rating)
            if len(item_score) > 0:
                result[user_id] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:recall_num]
        print_cost_time(f"\t进程: {os.getpid()}, 处理 {len(user_items_list)} 条记录, 生成 {len(result)} 条记录, 耗时", start_time)
        return result


if __name__ == '__main__':
    import json
    from cf.utils import read_data, pre_process
    # train_path = '/Users/summy/project/rust/ai/train.csv'
    # data = read_data(train_path)
    # data = pre_process(data)
    # cf = BaseCollFilter(data)
    # ucf = cf.user_cf()
    # with open('ucf_pool', 'w') as f:
    #     json.dump(ucf, f)
    # icf = cf.item_cf()
    # with open('icf_pool', 'w') as f:
    #     json.dump(icf, f)

    def handle(line) -> (int, str, float):
        user_id, item_id, _, _, _ = line.strip().split(",")
        return int(user_id), item_id, 1

    train_path = '/Users/summy/project/python/work/video_rec_recall/data/V0002_20_25.csv'
    data = read_data(train_path)[:50000]
    data = pre_process(data, handle)
    cf = BaseCollFilter(data)
    ucf = cf.user_cf()
    icf = cf.item_cf()


