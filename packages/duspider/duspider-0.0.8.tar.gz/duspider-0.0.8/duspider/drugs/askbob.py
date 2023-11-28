# -*- coding: utf-8 -*-
# @project: duspider
# @Author：dyz
# @date：2023/11/13 9:35
# see https://www.jk.cn/ab-web/result/drugEntrance
from pydantic import BaseModel
from duspider.base import HEADERS, Spider

from typing import List
from pydantic import BaseModel


class ChildData(BaseModel):
    atcCode: str
    name: str
    level: int
    childList: List = []
    top: int


class RespData(ChildData):
    """响音数据"""
    childList: List[ChildData] = []


class AskBobHit(BaseModel):
    name: str
    top1: str
    top2: str

    def __json(self, val):
        if isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        return val

    def json(self) -> dict:
        return {k: self.__json(v) for k, v in self.dict().items()}


class AskBobDrug(Spider):
    """AskBob 药品"""

    def __init__(self, headers, max_retry=3, **kwargs):
        super().__init__()
        self.headers = headers  # *必填需要登陆
        self.start_url = 'https://srv.jk.cn/ab-gateway/pedia/drug/category/pc'
        self.top_url = 'https://srv.jk.cn/ab-gateway/pedia/drug/common/list/pc'
        self.product_url = 'https://srv.jk.cn/ab-gateway/pedia/drug/product/list'
        self.detail_url = 'https://srv.jk.cn/ab-gateway/pedia/drug/product/detail'
        self.params = {'type': 'X'}

    async def top1_list(self):
        """所有一级数据列表"""
        resp = await self.get(self.start_url, headers=self.headers)
        if resp.status_code == 200:
            data = [RespData(**i) for i in resp.json()['data']]
            async for row in self.to2_list(data):
                yield row

    async def to2_list(self, data_list: [RespData]):
        """解析二级列表"""
        for i in data_list:
            for chi in i.childList:
                params = {
                    'atcCode': chi.atcCode,
                    'pageSize': 10,
                    'offset': 0,
                }
                async for row in self.category_pages(params=params, top1=i.name, top2=chi.name):
                    yield row

    async def category_pages(self, params, top1, top2):
        """分类下的翻页"""
        while True:
            resp = await self.get(self.top_url, params=params, headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()['data']
                async for row in self.parse_category_list(data['list'], top1, top2):
                    yield row
                if not data['hasMore']:
                    break

    async def parse_category_list(self, data, top1, top2):
        """解析分类下的列表数据"""
        for hit in data:
            _key = hit['key']
            _type = hit['type']
            params = {
                'key': _key,
                'filterType': _type,
                'relationType': '',
                'specification': '',
                'forms': '',
                'offset': 0,
                'pageSize': 10,
            }
            async for row in self.name_pages(params, top1, top2):
                yield row

    async def name_pages(self, params, top1, top2):
        """同名数据的翻页"""
        while True:
            resp = await self.get(self.product_url, params=params, headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()['data']
                async for row in self.parse_name_list(data['list'], top1, top2):
                    yield row
                if not data['hasMore']:
                    break
            params['offset'] += 10

    async def parse_name_list(self, data, top1, top2):
        for row in data:
            key = row['key']
            yield await self.detail(key, top1, top2)

    async def detail(self, key, top1, top2):
        params = {
            'key': key,
            'relationType': '',
        }
        resp = await self.get(self.detail_url, params=params, headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()['data']
            data['top1'] = top1
            data['top2'] = top2
            return data

    async def run(self):
        async for row in self.top1_list():
            print(row)

    async def parse(self):
        pass


if __name__ == '__main__':
    headers = {
        'authority': 'srv.jk.cn',
        'ab-client': 'PC',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'antibot': 'antibot:bWdNZk51Y1dRallJSVRuYQ==',
        'authentication': 'eyJhbGciOiJIUzUxMiJ9.eyJhcHBsaWNhdGlvbkFjY291bnRJbmZvIjp7ImlkIjozMjAwMzg2LCJjaGFubmVsSWQiOiIxMTAwNDkwMDAwIiwiaW5zdGl0dXRpb25JZCI6IjEyNDQ0NDAzMDAwMDMzMTAwMDAwMDAiLCJyb2xlIjoxLCJzb3VyY2UiOjAsInNlc3Npb25UeXBlIjoid2ViIiwiaXNBdXRvTG9naW4iOmZhbHNlLCJjb21tb25Vc2VySWQiOjM2OTE2MCwicGF5bWVudExldmVsIjowLCJhcGlVc2VySWQiOm51bGwsInJlYWxBdXRob3JpemF0aW9uIjpudWxsLCJ0b2tlblVwZGF0ZVRpbWUiOm51bGx9LCJleHAiOjE3MTU0MTEyNjh9.voZanOyoTQNZXsoJMCfWAzeljNdMQG5VkApQqIn6PI8NvnbdGzTHh3yXmgNqvQPSw2BX1B4rumKeDIc60bf83g',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://www.jk.cn',
        'pragma': 'no-cache',
        'referer': 'https://www.jk.cn/',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'uniqueequipmenttype': '3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }
    s = AskBobDrug(headers)
    import asyncio

    asyncio.run(s.run())
