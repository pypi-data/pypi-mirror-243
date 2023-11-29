import logging
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils.applications import (
    Applications,
    extract_applications,
    find_missing_application,
)
from nagra_network_paloalto_utils.utils.common.yamlizer import get_yaml_data

log = logging.getLogger(__name__)


@click.group()
def applications():
    pass


@applications.command("generate")
@click.option("--file", type=Path, help="Input file with rules")
@click.pass_obj
def generate_missing(obj, file):
    data = list(get_yaml_data(file))
    input_applications = extract_applications(data)

    applications_from_firewall = Applications(obj.URL, obj.API_KEY)
    applications = applications_from_firewall.find_by_names(input_applications)
    applications = find_missing_application(applications)
    if applications:
        log.error(f"Some applications do not exist: {applications}")
        raise ValueError

    log.info("No application missing to create")
