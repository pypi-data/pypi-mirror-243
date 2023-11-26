#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""pool_coll_filter"""

import os
import time
import math
from multiprocessing import Pool
from cf.base import BaseCollFilter
from cf.utils import print_cost_time
from typing import Iterable, Tuple
from cf import default_similar_func, CFType, U, T


class PoolCollFilter(BaseCollFilter):

    def __init__(self, data: Iterable[Tuple[U, T, float]], parallel_num=0, similar_func=default_similar_func):
        super().__init__(data, similar_func)
        cpu_count = os.cpu_count()
        self.parallel_num = cpu_count if parallel_num <= 1 else parallel_num
        self.pool = Pool(cpu_count - 1) if self.parallel_num >= cpu_count else Pool(self.parallel_num - 1)

    def cal_similar(self, cf_type: CFType, similar_num=256):
        """
        计算相似度

        计算用户相似度：cal_similar(user_items, item_users)
        计算物品相似度：cal_similar(item_users, user_items)

        item_users:
        user1: item1, item2, item3
        user2: item2, item3, item4

        item_users:
        item2: user1, user2
        item3: user1, user2

        @return dict{:dict}    {user1: {user2: similar}}
        """
        print(f'开始{cf_type.value}相似度计算, similar_num: {similar_num}')
        func_start_time = time.perf_counter()
        dict1, items_list = self._get_cal_similar_inputs(cf_type)
        items_list = list(items_list)
        size = len(items_list)
        split_size = math.ceil(size / self.parallel_num)
        results = [self.pool.apply_async(func=self._do_cal_similar,
                                         args=(dict1,
                                               items_list[i:i+split_size],
                                               self.similar_func
                                               )
                                         )
                   for i in range(split_size, size, split_size)]

        similar = self._do_cal_similar(dict1, items_list[:split_size], self.similar_func)

        for result in results:
            for key, items in result.get().items():
                if key in similar:
                    for item, score in items.items():
                        similar[key][item] = similar[key].get(item, 0.0) + score
                else:
                    similar[key] = items

        similar = self._sort_similar(similar, similar_num)
        print_cost_time(f"完成{cf_type.value}相似度计算, 当前进程: {os.getpid()}, 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        return similar

    def release(self):
        super().release()
        self.pool.close()

    def _do_cf(self, user_ids, similar_dict, recall_num, cf_type: CFType):
        size = len(self.user_item_ratings)
        print(f'开始{cf_type.value}推理, recall_num: {recall_num}')
        func_start_time = time.perf_counter()
        user_items_list = list(map(lambda x: (x, self.user_item_ratings.get(x, [])), user_ids) if user_ids else self.user_item_ratings.items())

        if cf_type == CFType.UCF:
            cf_func = self._do_user_cf
        else:
            cf_func = self._do_item_cf

        split_size = math.ceil(size / self.parallel_num)
        results = [self.pool.apply_async(func=cf_func,
                                         args=(self.user_item_ratings,
                                               similar_dict, user_items_list[i:i + split_size],
                                               recall_num
                                               )
                                         )
                   for i in range(split_size, size, split_size)]

        cf_result = cf_func(self.user_item_ratings, similar_dict, user_items_list[:split_size], recall_num)

        for result in results:
            cf_result.update(result.get())

        print_cost_time(f"完成{cf_type.value}推理, 当前进程: {os.getpid()}, 生成{len(cf_result)}条记录, 总耗时",
                        func_start_time)
        return cf_result


if __name__ == '__main__':
    import json
    from cf.utils import read_data, pre_process
    # train_path = '/Users/summy/project/rust/ai/train.csv'
    # data = read_data(train_path)
    # data = pre_process(data)
    # cf = PoolCollFilter(data, 4)
    # ucf = cf.user_cf()
    # with open('../ucf_op', 'w') as f:
    #     json.dump(ucf, f)
    # icf = cf.item_cf()
    # with open('../icf_op', 'w') as f:
    #     json.dump(icf, f)

    def handle(line) -> (int, str, float):
        user_id, item_id, _, _, _ = line.strip().split(",")
        return int(user_id), item_id, 1

    train_path = '/Users/summy/project/python/work/video_rec_recall/data/V0002_20_25.csv'
    data = read_data(train_path)[:50000]
    data = pre_process(data, handle)
    cf = PoolCollFilter(data, 8)
    ucf = cf.user_cf()
    icf = cf.item_cf()


