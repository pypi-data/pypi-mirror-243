import logging
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils.object_deletion_checker import (
    get_all_used_objects,
    get_objects_to_delete,
)

log = logging.getLogger(__name__)


@click.command()
@click.argument("planfile", type=Path)
def check_delete(planfile):
    """
    Check if ...
    """
    objects_to_check = get_objects_to_delete(planfile)

    if not objects_to_check:
        log.info("No objects to delete")
        exit(0)

    used_objects = get_all_used_objects()

    objects_in_use = list(set(used_objects) & set(objects_to_check))

    if objects_in_use:
        log.error(
            f"Some objects that you are trying to delete are still in use: {objects_in_use}",
        )
        exit(1)
    else:
        log.info("None of the object to delete are in use.")
        exit(0)
