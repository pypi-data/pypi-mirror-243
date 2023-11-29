import ipaddress
import logging
import re

from .common.utils import BaseRegistry
from .constants import SUBNET_REGEX_STR

# API_KEY = os.environ["PANOS_API_KEY"]
# PANORAMA = os.environ["PANOS_HOSTNAME"]


log = logging.getLogger("addresses.py")


class Addresses(BaseRegistry):
    def get_data(self):
        """
        Find all addresses on Panorama

        :return: list of dictonary for addresses and addresses_groups on Panorama
        """

        device_group = "DG1_GLOBAL"
        data = [
            ("addresses", self.client.objects.Addresses),
            ("address_groups", self.client.objects.AddressGroups),
            ("external_dyn_lists", self.client.objects.ExternalDynamicLists),
        ]
        result = []
        for source, object_type in data:
            objects = object_type.get(device_group=device_group)
            for o in objects:
                o["@source"] = source
                result.append(o)
        return result

    def find_by_name(self, name):
        if name == "any":
            return "any"
        return super().find_by_name(name)


def extract_addresses(data):
    addresses = []
    for rules in data:
        if rules["rules"] is None:
            continue
        for rule in rules["rules"]:
            addresses.extend(rule["source_addresses"])
            addresses.extend(rule["destination_addresses"])
    return addresses


def is_cidr(value):  # Logic from matthias, seems to be wrong ?
    try:
        ipaddress.ip_network(value, strict=False)
        return False
    except ValueError:
        return True


def remove_cidr_from_addresses(addresses):
    return [address for address in addresses if address and is_cidr(address)]


def get_addresses_to_create(addresses):
    return [name for name, value in addresses.items() if not value]


def check_addresses_to_create_length(addresses_to_create):
    too_long_addresses = [
        address for address in addresses_to_create if len(address) >= 63
    ]
    if len(too_long_addresses) > 0:
        raise SyntaxError(
            "ERROR: the following addresses are too long (above 63 chars): {}".format(
                too_long_addresses,
            ),
        )
    return addresses_to_create


def create_addresses(addresses_to_create, owner):
    addresses_to_return = []
    for address_to_create in addresses_to_create:
        if re.match(f"^(ip_){SUBNET_REGEX_STR}$", address_to_create):
            ip = address_to_create.replace("ip_", "").replace("-", "/")
            addresses_to_return.append(
                {
                    "name": address_to_create,
                    "owner": owner,
                    "type": "ip-netmask",
                    "value": ip,
                    "tags": ["terraform"],
                },
            )
        elif re.match("fqdn_(\S*\.*\S)+", address_to_create):
            fqdn = address_to_create.replace("fqdn_", "")
            addresses_to_return.append(
                {
                    "name": address_to_create,
                    "owner": owner,
                    "value": fqdn,
                    "tags": ["terraform"],
                },
            )
        else:
            raise SyntaxError(f"ERROR: address {address_to_create} malformed")
    return addresses_to_return
