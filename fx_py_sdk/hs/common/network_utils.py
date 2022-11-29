# -*- coding:utf-8 -*-

import netifaces
import psutil

from hs.common.common_utils import get_logger

logging = get_logger(__name__)


invalid_macs_start_str = (
    '00-05-69',
    '00-1c-14',
    '00-0c-29',
    '00-50-56',
    '08-00-27',
    '0a-00-27',
    '00-03-ff',
    '00-15-5d'
)


def get_psutil_mac_address_list() -> dict:
    mac_addresses = {}

    addrs_info = psutil.net_if_addrs()
    stats_info = psutil.net_if_stats()

    for adapter in addrs_info:
        snicaddr_list = addrs_info[adapter]
        snicstats = stats_info[adapter]

        for snicaddr in snicaddr_list:
            if snicstats.isup and snicaddr.family.name in {'AF_LINK'}:
                mac = snicaddr.address
                if '-' in mac or ':' in mac:
                    if len(mac) == 17 and mac != '00:00:00:00:00:00' and mac != '00-00-00-00-00-00':
                        mac = mac.replace(':', '-').lower()
                        if not mac.startswith(invalid_macs_start_str):
                            mac_addresses[mac] = True
    return mac_addresses


def get_routing_nic_names() -> set:
    netifaces_gateways = netifaces.gateways()
    gateways = netifaces_gateways[netifaces.AF_INET]

    routing_nic_names = set()

    for gateway in gateways:
        routing_nic_names.add(gateway[1])
    return routing_nic_names


def get_netifaces_mac_address_list() -> list:
    mac_addresses = []

    routing_nic_names = get_routing_nic_names()

    for interface in netifaces.interfaces():
        if interface in routing_nic_names:
            routing_nic_mac_addr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            if len(routing_nic_mac_addr) == 17 and routing_nic_mac_addr != '00:00:00:00:00:00' and routing_nic_mac_addr != '00-00-00-00-00-00':
                routing_nic_mac_addr = routing_nic_mac_addr.replace(':', '-').lower()
                mac_addresses.append(routing_nic_mac_addr)

    mac_addresses.sort()
    return mac_addresses


def get_mac_address() -> str:
    psutil_mac_dict = get_psutil_mac_address_list()
    netifaces_mac_address_list = get_netifaces_mac_address_list()

    logging.info(f'psutil mac address : {psutil_mac_dict}')
    logging.info(f'netifaces mac address : {netifaces_mac_address_list}')
    result_list = []

    if len(netifaces_mac_address_list) == 0:
        for mac in psutil_mac_dict.keys():
            result_list.append(mac)
    elif len(psutil_mac_dict) == 0:
        for mac in netifaces_mac_address_list:
            result_list.append(mac)
    else:
        for mac in netifaces_mac_address_list:
            if mac in psutil_mac_dict and psutil_mac_dict[mac] == True:
                result_list.append(mac)

    if len(result_list) == 0:  # 都未获取到
        raise Exception('get mac address error, length 0')

    result_list.sort()
    logging.info(f'mac address result: {result_list}')
    return result_list[0]
