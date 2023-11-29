import logging

from .common.utils import BaseRegistry

log = logging.getLogger(__name__)


# API_KEY = os.environ["PANOS_API_KEY"]
# PANORAMA = os.environ["PANOS_HOSTNAME"]


class Applications(BaseRegistry):
    def get_data(self):
        """
        Find all applications
        :return: list of all applications
        """
        dg1_global = {
            "device-group": "DG1_GLOBAL",
        }
        predefined = {
            "location": "predefined",
        }
        return [
            self.client.objects.Applications.get(params=dg1_global),
            self.client.objects.Applications.get(params=predefined),
        ]


def extract_applications(data):
    applications = []
    for rules in data:
        if rules["rules"] is None:
            continue
        for rule in rules["rules"]:
            try:
                applications.extend(rule["applications"])
            except KeyError:
                continue
    return applications


def find_missing_application(applications):
    applications_to_return = []
    for application in applications:
        if application == "any":
            continue
        if not applications[application]:
            applications_to_return.append(application)
    return applications_to_return
