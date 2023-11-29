import ast
import logging

import click
from panos import panorama

from nagra_network_paloalto_utils.utils.locking_panorama import try_lock, unlock_pano
from nagra_network_paloalto_utils.utils.panorama import commit, push, revert_config

log = logging.getLogger(__name__)


@click.command(
    "lock",
    help="""\
Lock Palo Alto Panorama.
The command takes a json-formatted list of firewall to lock. (default to all)""",
)
@click.argument(
    "firewalls",
    envvar="FIREWALLS",
    type=ast.literal_eval,
    default="""["DG1_GLOBAL"]""",
)
@click.pass_obj
def cmd_lock(obj, firewalls):
    firewalls = [None] if "DG1_GLOBAL" in firewalls else firewalls
    if not try_lock(obj.URL, obj.API_KEY, firewalls=firewalls):
        exit(1)


@click.command(
    "unlock",
    help="""\
Unlock Palo Alto Panorama.
The command takes a json-formatted list of firewall to lock. (default to all)""",
)
@click.argument(
    "firewalls",
    envvar="FIREWALLS",
    type=ast.literal_eval,
    default="""["DG1_GLOBAL"]""",
)
@click.pass_obj
def cmd_unlock(obj, firewalls):
    panorama_instance = panorama.Panorama(obj.URL, api_key=obj.API_KEY)
    firewalls = [None] if "DG1_GLOBAL" in firewalls else firewalls
    # firewalls = ["shared"] if "DG1_GLOBAL" in firewalls else firewalls  # TODO: check if it makes sense
    # comment=f"Terraform pipeline {obj.CI_COMMIT_REF_NAME} {obj.CI_PROJECT_TITLE}"
    if not unlock_pano(panorama_instance, firewalls):
        exit(1)


@click.command("commit", help="Commit changes to Palo Alto Panorama")
@click.option(
    "--admin-name",
    "commiter_name",
    envvar="PANOS_ADMIN_NAME",
    help="The admin name under which to commit",
    required=True,
)
@click.option("--firewalls", default="['DG1_GLOBAL']")
@click.option("--branch")
@click.option("--no-push", "no_push", type=bool, default=False)
@click.option("--only-push", "only_push", type=bool, default=False)
@click.pass_obj
def cmd_commit(obj, commiter_name, firewalls, branch, no_push, only_push):
    """
    makes a partial commit under the admin name

    :return:
    """
    # all_firewalls = not firewalls or "DG1_GLOBAL" in firewalls
    if only_push:
        push(firewalls, branch)
        exit()

    description = "Automatic commit from {} {}.(Commit SHA : {})".format(
        obj.CI_PROJECT_TITLE,
        obj.CI_COMMIT_REF_NAME,
        obj.CI_COMMIT_SHA,
    )

    res = commit(commiter_name, commit_type="partial", description=description)
    if res == "success" and not no_push:
        log.info("Commit done.")
        if not no_push:
            log.info(f"Pushing the config to {firewalls} !")
            push(firewalls, branch)
    elif res == "same_config":
        log.info("Same configuration nothing to commit")
        # We should revert the changes..
        revert_config(obj.URL, obj.API_KEY, commiter_name)
    else:
        log.info(
            "Error. This is most likely because someone else is performing maintenance on the firewall."
            " You will need to manually commit-all",
        )
        exit(1)
