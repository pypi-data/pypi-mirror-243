#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    获取 Zabbix 主机 inventory 信息并生成 ES 索引。
"""
import argparse
import logging
import time
from datetime import datetime
from lib.utils.esapis import ESManager

# calls = 0
# 初始化 ALL_ZABBIX_HOSTS 为一个空列表，代表了 Zabbix 的所有主机信息
ALL_ZABBIX_HOSTS = []


class ZbxHostIndex:
    def __init__(self, args):
        self.args = args
        self.localtime = time.strftime("%Y.%m.%d", time.localtime())
        self.es_client = ESManager(
            self.args.es_url,
            self.args.es_user,
            self.args.es_passwd
        )
        self.tpl_name = self.args.es_tpl
        self.lagency_index = self.args.lagency_index

    @property
    def zbx_hosts(self):
        """获取 Zabbix Server 所有主机信息"""
        # global calls
        # calls += 1
        return self.args.zapi.host.get(
            {
                "output": "extend",
                "selectGroups": "extend",
                "selectInterfaces": "extend",
                "selectInventory": "extend",
                "selectTags": "extend",
                "selectInheritedTags": "extend"
            }
        )

    def generate_host_index(self):
        """根据条件判断是否生成 ES 'zabbix-host-info-*' 索引"""
        body_datas = []
        if self.lagency_index:
            # 使用全局变量 ALL_ZABBIX_HOSTS，这样就避免重复调用 Zabbix API 接口以获取全部主机信息
            for host in ALL_ZABBIX_HOSTS:
                inventory = host.get("inventory") if isinstance(host.get("inventory"), dict) else {}
                body_datas.append(
                    {
                        "_id": host.get("hostid"),
                        "主机名称": inventory.get("name", host.get("host")),
                        "主机别名": inventory.get("alias", host.get("host")),
                        "接口地址": [
                            interface.get("ip") for interface in host.get("interfaces")
                            if host.get("interfaces")
                        ],
                        "主机组": [
                            group.get("name") for group in host.get("groups")
                            if host.get("groups")
                        ],
                        "OS": inventory.get("os"),
                        "OS_FULL": inventory.get("os_full"),
                        "OS_SHORT": inventory.get("os_short"),
                        "资产标签": inventory.get("asset_tag"),
                        "主负责人": inventory.get("poc_1_name"),
                        "次负责人": inventory.get("poc_2_name"),
                        "机架": inventory.get("chassis"),
                        "子网掩码": inventory.get("host_netmask"),
                        "主机网络": inventory.get("host_networks"),
                        "机房": inventory.get("location"),
                        "机柜": inventory.get("site_rack"),
                        "序列号": inventory.get("serialno_a"),
                        "管理IP": inventory.get("oob_ip"),
                        "MAC_A": inventory.get("macaddress_a"),
                        "MAC_B": inventory.get("macaddress_b"),
                        "硬件架构": inventory.get("hw_arch"),
                        "标签": inventory.get("tag"),
                        "类型": inventory.get("type"),
                        "具体类型": inventory.get("type_full"),
                        "型号": inventory.get("model"),
                        "供应商": inventory.get("vendor"),
                        "主机标签名称": [tag.get("tag") for tag in host.get("tags") if host.get("tags")],
                        "主机标签值": [tag.get("value") for tag in host.get("tags") if host.get("tags")],
                        "继承标签名称": [
                            tag.get("tag") for tag in host.get("inheritedTags")
                            if host.get("inheritedTags")
                        ],
                        "继承标签值": [
                            tag.get("value") for tag in host.get("inheritedTags")
                            if host.get("inheritedTags")
                        ],
                        "@timestamp": datetime.utcfromtimestamp(time.time())
                    }
                )
            index_of_host = "zabbix-host-info-" + self.localtime
            self.es_client.bulk(actions=body_datas, index=index_of_host)
            logging.info(
                "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
                self.args.es_url,
                index_of_host
            )

    def generate_raw_host_index(self):
        """生成 ES 'zabbix-raw-host-info-*' 索引"""
        # 将 ALL_ZABBIX_HOSTS 变量定义为全局变量
        # 然后将 self.zbx_hosts 属性获取到的 Zabbix 的所有主机信息赋给 ALL_ZABBIX_HOSTS 这个全局变量
        global ALL_ZABBIX_HOSTS
        ALL_ZABBIX_HOSTS = self.zbx_hosts
        for host in ALL_ZABBIX_HOSTS:
            host["_id"] = host["hostid"]
            host["@timestamp"] = datetime.utcfromtimestamp(time.time())
        self.es_client.put_template(tpl_name=self.tpl_name)
        index_of_raw_host = "zabbix-raw-host-info-" + self.localtime
        self.es_client.bulk(actions=ALL_ZABBIX_HOSTS, index=index_of_raw_host)
        logging.info(
            "\033[32m成功生成 ES 索引：'(ES Host)%s' => '(ES INDEX)%s'\033[0m",
            self.args.es_url,
            index_of_raw_host
        )


def main(args):
    """创建 ES 索引"""
    ZbxHostIndex(args=args).generate_raw_host_index()
    ZbxHostIndex(args=args).generate_host_index()
    # print(f"--- 总共调用 {calls} 次 ---")


parser = argparse.ArgumentParser(description="Gather zabbix host informations and create es index")
parser.add_argument(
    "--es_url",
    type=str,
    required=True,
    help="ElasticSearch server ip"
)
parser.add_argument(
    "--es_user",
    default="",
    help="ElasticSearch server login user"
)
parser.add_argument(
    "--es_passwd",
    default="",
    help="ElasticSearch server login password"
)
parser.add_argument(
    "--es_tpl",
    required=True,
    help="ElasticSearch index template name"
)
parser.add_argument(
    "--lagency_index",
    action="store_true",
    help="Wether to generate 'zabbix-host-info-*' index"
)
parser.set_defaults(handler=main)
