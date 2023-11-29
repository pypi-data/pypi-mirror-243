import logging
import re
from pathlib import Path

from . import rules_getter
from .panorama import get_all_device_groups

# PLAN = os.environ["PLAN"]

log = logging.getLogger("Object Deletion Checker")


def tf_plan_summary(line):
    return re.match("Plan: \d* to add, \d* to change, \d* to destroy.\s", line)


def tf_unchanged(line):
    return re.match("\s*# \(\d* unchanged (blocks|attributes) hidden\)\s", line)


def tf_mutated(line):
    return re.match(
        '(^\s*# module(.\d*)*\["\S*"\] will be (updated in-place|created))',
        line,
    )


def tf_destroyed(line):
    return re.match(
        '(^\s*# module(.\d*)*\["\S*"\] will be (updated in-place|created))',
        line,
    )


def get_objects_to_delete(plan_file):
    with Path(plan_file).open() as tf:
        text = tf.readlines()
    with Path(plan_file).open("w") as tf:
        useful = False
        for line in text:
            if "Terraform will perform the following actions:" in line:
                useful = True
            elif tf_plan_summary(line) or tf_unchanged(line):
                continue
            elif tf_mutated(line):
                useful = False
                continue
            elif tf_destroyed(line):
                tf.write(line.lstrip())
                useful = True
            if not useful:
                continue

            line = re.sub("^\s*- ", "", line)
            line = re.sub("( -> null)", "", line)
            tf.write(line.lstrip())

    with Path(plan_file).open() as tf:
        return [
            line.replace("name", "", 1).replace("=", "", 1).replace('"', "").strip()
            for line in tf
            if re.match('name\s*= "(\w|\d|-|_|\.)*"', line)
        ]


def get_all_used_objects(url, api_key):
    dgs = get_all_device_groups(url, api_key)

    data = []
    used_objects = []

    log.info("Getting all Security, NAT and PBF rules")
    for dg in dgs:
        sr = rules_getter.get_security_rules(url, api_key, dg)
        nat = rules_getter.get_nat_rules(url, api_key, dg)
        pbf = rules_getter.get_pbf_rules(url, api_key, dg)
        data.append(sr)
        data.append(nat)
        data.append(pbf)

    log.info("All rules pulled from Panorama!")
    for device in data:
        for rule in device:
            used_objects.extend(rule["source"]["member"])
            used_objects.extend(rule["destination"]["member"])
            # For NAT
            if rule.get("destination-translation"):
                used_objects.append(
                    rule["destination-translation"]["translated-address"],
                )
            if rule.get("source-translation"):
                try:
                    used_objects.append(
                        rule["source-translation"]["static-ip"]["translated-address"],
                    )
                except KeyError:
                    continue

    return list(dict.fromkeys(used_objects))
