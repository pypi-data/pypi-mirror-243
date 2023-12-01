import csv
import logging
import re
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils import git_writer
from nagra_network_paloalto_utils.utils.addresses import (
    Addresses,
    check_addresses_to_create_length,
    create_addresses,
    extract_addresses,
    get_addresses_to_create,
)
from nagra_network_paloalto_utils.utils.addresses_remove import (
    addresses_from_csv,
    remove_addresses,
)
from nagra_network_paloalto_utils.utils.common import yamlizer
from nagra_network_paloalto_utils.utils.common.utils import expanded
from nagra_network_paloalto_utils.utils.common.yamlizer import get_yaml_data
from nagra_network_paloalto_utils.utils.constants import (
    DEFAULT_GIT_DIR,
    DEFAULT_TERRAFORM_PATH,
)

log = logging.getLogger(__name__)
# https://stackoverflow.com/questions/66743792/how-to-define-common-python-click-options-for-multiple-commands#:~:text=To%20use%20the%20same%20option%20across%20multiple%20commands,to%20a%20variable%20and%20then%20use%20it%20twice%3A
# @click.group()
# @click.option(
#     "-v",
#     "--verbose",
#     count=True,
#     default=0,
#     help="-v for DEBUG",
# )
# def addresses(verbose):
#     global VERBOSE
#     VERBOSE = verbose


@click.group()
def addresses():
    pass


@addresses.command()
@click.option("-f", "--file", type=Path)
@click.option("-a", "--address-tf-file", type=Path, default=DEFAULT_TERRAFORM_PATH)
@click.pass_obj
def remove(
    obj,
    file=None,
    address_tf_file=None,
):
    addresses = []
    if file:
        addresses.extend(addresses_from_csv(file))

    registry = Addresses(obj.URL, obj.API_KEY, verbose=obj.VERBOSE)
    remove_addresses(
        addresses,
        address_registry=registry,
        address_tf_file=address_tf_file,
    )


@addresses.command()
@click.option("-d", "--dest", type=Path, default="output", required=True)
@click.pass_obj
def export(obj, dest):
    registry = Addresses(obj.URL, obj.API_KEY)
    with Path(dest).open("x") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(("id", "created_by"))
        writer.writerows((key, "gui") for key in registry.addresses)


@addresses.command("generate", help="Generate missing addresses")
@click.option("-f", "--file", type=Path, help="Input file with rules", required=True)
@click.option(
    "--repo",
    "repository",
    type=expanded,
    default="https://pano_utils:$GITLAB_TOKEN@gitlab.kudelski.com/network/paloalto/global/objects",
    help="Gitlab repository in which is the file to modify",
)
@click.option(
    "--branch",
    "branch",
    envvar="CI_COMMIT_REF_NAME",
    help="Reference of the branch/tag/commit (e.g. 'refs/heads/master' )",
)
@click.option(
    "-o",
    "--output",
    "output",
    default=None,
    help="File in which to output the new tags",
)
@click.option("--commit_message", help="Commit message to use ")
@click.option(
    "--owner_email",
    "email",
    default="gitinetwork@nagra.com",
    help="email of the owner for the new tags",
)
@click.option("--push", type=bool, default=False)
@click.option("--test", type=bool, default=False)
@click.pass_obj
def cmd_generate_missing_addresses(
    obj,
    file,
    output,
    repository,
    branch,
    commit_message="",
    email="",
    push=False,
    test=False,
):
    repo = git_writer.get_repo(repository, branch)
    log.info(repo)
    input_objects = extract_addresses(get_yaml_data(file))
    addresses_from_firewall = Addresses(obj.URL, obj.API_KEY)
    addresses = addresses_from_firewall.find_addresses_by_name(input_objects)
    addresses_to_create = create_addresses(
        check_addresses_to_create_length(get_addresses_to_create(addresses)),
        re.findall("[\w\.]+@[\w\.]+", email)[0],
    )
    if not addresses_to_create:
        log.info("No address to create.")
        return
    if test:
        log.info(f"Missing {len(addresses_to_create)} addresses")
        return
    if not repository:
        log.warn("Repository is missing")
        return
    output = DEFAULT_GIT_DIR / Path(output)
    log.info(f"Creating {len(addresses_to_create)} addresses")
    yamlizer.add_elements_to_file(addresses_to_create, output)
    git_writer.git_commit_repo(repository, output, commit_message, push=push)
    log.info("Successfully created new addresses!\n")
