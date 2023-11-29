import logging
import re

from .common.utils import BaseRegistry

# API_KEY = os.environ["PANOS_API_KEY"]
# PANORAMA = os.environ["PANOS_HOSTNAME"]

# if re.match("^blr.*", os.environ["CI_COMMIT_REF_NAME"]):
#     BRANCH = os.environ["CI_COMMIT_REF_NAME"]
# else:
#     BRANCH = None

log = logging.getLogger("services.py")


class Services(BaseRegistry):
    def get_data(self):
        """
        Find all services
        :return: list of all services
        """
        dg1_global = {
            "device-group": "DG1_GLOBAL",
        }
        predefined = {
            "device-group": "predefined",
        }
        return [
            *self.client.objects.Services.get(params=dg1_global),
            *self.client.objects.ServiceGroups.get(params=dg1_global),
            *self.client.objects.Services.get(params=predefined),
        ]

    def find_by_name(self, name):
        if name in ("any", "application-default"):
            return name
        return super().find_by_name(name, False)


def extract_services(data):
    services = []
    for rules in data:
        if rules["rules"] is None:
            return []
        for rule in rules["rules"]:
            try:
                services.extend(rule["services"])
            except KeyError:
                continue
    return services


def create_services(services, owner):
    services_to_return = []
    for service in services:
        if re.match("service-(tcp|udp)(_\d{1,5})(-\d{1,5})?", service):
            services_to_return.append(
                {
                    "name": service,
                    "protocol": re.findall("(tcp|udp)", service)[0],
                    "destination": "".join(
                        re.findall("(\d{1,5})(-\d{1,5})?", service)[0],
                    ),
                    "tags": [owner, "terraform"],
                },
            )
        else:
            raise SyntaxError(f"ERROR: service {service} is malformed")
    return services_to_return
