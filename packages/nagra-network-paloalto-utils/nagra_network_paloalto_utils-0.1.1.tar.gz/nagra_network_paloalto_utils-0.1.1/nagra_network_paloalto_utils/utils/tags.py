import logging

from .common.utils import BaseRegistry

# API_KEY = os.environ["PANOS_API_KEY"]
# PANORAMA = os.environ["PANOS_HOSTNAME"]

# if re.match("^blr.*", os.environ["CI_COMMIT_REF_NAME"]):
#     BRANCH = os.environ["CI_COMMIT_REF_NAME"]
# else:
#     BRANCH = None


log = logging.getLogger("tags.py")


class Tags(BaseRegistry):
    def get_data(self):
        """
        Find all tags

        :param address: FQDN address
        :return: list of 1 element containing the address object ( empty if no address object )
        """
        payload = {
            "device-group": "DG1_GLOBAL",
        }
        return self.client.policies.Tags.get(params=payload)


def create_missing_tags(tags, mail):
    return [{"name": name, "owner": mail} for name, value in tags.items() if not value]


def extract_tags(data):
    tags = []
    for rules in data:
        if rules["rules"] is None:
            continue
        for rule in rules["rules"]:
            tags.extend(rule["tags"])
    return tags
