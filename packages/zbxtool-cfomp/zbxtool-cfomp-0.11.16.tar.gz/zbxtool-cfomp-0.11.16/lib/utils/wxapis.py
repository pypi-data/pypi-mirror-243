#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from weworkapi.CorpApi import CORP_API_TYPE, CorpApi
from weworkapi.AbstractApi import ApiException
from .format import DiskCache

# 设置变量以保存企业微信全部部门信息（包含部门和部门下的子部门）
ALL_DEPARTMENTS = {}


class WxWorkApi:
    def __init__(self, corpid: str, agentid: str, secret: str):
        self._corpid = corpid
        self._agentid = agentid
        self._secret = secret
        self._corpapi = CorpApi(self._corpid, self._secret)

    @property
    def token(self):
        """
            获取企业微信应用的 access_token，默认缓存时间为 7200s:
                1. 需要注意的是，每个应用有独立的 secret，因而获取到的 access_token 只能在本应用内使用；
                2. 考虑到应用到多企业微信时 agentid 会有重复的情况，因而在设置缓存的 key 时，使用 "token_corpid_agentid" 的格式；
                3. access_token 的默认缓存时间为 7200s，考虑到函数执行时间和缓存时间的耗时，因而设置为 7100s。
        :return:
        """
        instance_ = DiskCache()
        if self._agentid:
            key = "token_" + str(self._corpid) + "_" + str(self._agentid)
            if instance_.get_cache(key):
                return instance_.get_cache(key)
            if self._secret:
                try:
                    instance_.set_cache(
                        key=key,
                        value=self._corpapi.getAccessToken(),
                        expire=7100,
                        retry=True
                    )
                except ApiException as err:
                    logging.error(msg="\033[31m" + str(err) + "\033[0m")
                else:
                    return instance_.get_cache(key)

    def _wework_request(self, api_type: str, params=None):
        """
            封装对 corpapi 的调用:
                1. 使用缓存的 token，避免重复调用接口获取；
                2. 请求接口时可以带上参数 params。
        :param api_type:
        :param params:
        :return:
        """
        try:
            if self.token:
                self._corpapi.access_token = self.token
                return self._corpapi.httpCall(api_type, params)
        except ApiException as err:
            logging.error(msg="\033[31m" + str(err) + "\033[0m")
            sys.exit(1)

    def get_all_departs(self):
        """
            获取企业微信中所有的部门信息：
                1. 当不指定 department_id 时，则获取企业微信全量的部门信息，包含部门及部门下的所有子部门信息。
        :return:
        """
        # 将 ALL_DEPARTMENTS 变量设置为全局变量，避免重复调用接口以获取企业微信全部部门信息
        global ALL_DEPARTMENTS
        ALL_DEPARTMENTS = self._wework_request(api_type=CORP_API_TYPE["DEPARTMENT_LIST"])

    def get_dep_users(self, dep_name: str):
        """
            根据部门名称获取其及其下所有子部门的所有员工信息：
                1. 在获取某个部门下的员工信息时，查询的参数为部门 id，而非部门名称；
                2. 在最新的企业微信开发文档中，已经舍弃了 "fetch_child" 这个参数，因而要获取某个部门下的所有子部门信息，
                   只能递归遍历。
        :param dep_name:
        :return:
        """
        user_list = []
        self.get_all_departs()
        all_depids = [
            dep.get("id") for dep in ALL_DEPARTMENTS.get("department")
            if dep.get("name") == dep_name if ALL_DEPARTMENTS.get("department")
        ]
        if not all_depids:
            logging.error(f"\033[31m企业微信中未找到部门: {dep_name}\033[0m")
            sys.exit(1)
        for depid in all_depids:
            sub_departs = self._wework_request(
                api_type=CORP_API_TYPE["DEPARTMENT_LIST"],
                params={"id": str(depid)}
            )
            depids = [
                dep.get("id") for dep in sub_departs.get("department")
                if sub_departs.get("department")
            ]
            for dep_id in depids:
                users = self._wework_request(
                    api_type=CORP_API_TYPE["USER_LIST"],
                    params={"department_id": str(dep_id)}
                )
                if users:
                    user_list += users.get("userlist")
        return user_list
