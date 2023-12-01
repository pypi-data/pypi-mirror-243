import logging
import re
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils import git_writer
from nagra_network_paloalto_utils.utils.common.yamlizer import (
    add_elements_to_file,
    get_yaml_data,
)
from nagra_network_paloalto_utils.utils.constants import DEFAULT_GIT_DIR
from nagra_network_paloalto_utils.utils.services import (
    Services,
    create_services,
    extract_services,
)

log = logging.getLogger(__name__)


@click.group()
def services():
    pass


@services.command("generate")
@click.option("--file", "source_file", type=Path, help="Input file with rules")
@click.option(
    "--repo",
    "repo",
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
    "output_file",
    type=Path,
    help="File in which to output the new tags",
)
@click.option("--commit_message", "commit_message", help="Commit message to use ")
@click.option(
    "--owner_email",
    "email",
    default="gitinetwork@nagra.com",
    help="email of the owner for the new tags",
)
@click.option("--push", type=bool, default=False)
@click.option("--test", type=bool, default=False)
@click.pass_obj
def cmd_generate_missing_services(
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
    output = DEFAULT_GIT_DIR / Path(output)
    data = list(get_yaml_data(file))
    input_objects = extract_services(data)

    services_from_firewall = Services(obj.URL, obj.API_KEY)
    to_create = services_from_firewall.find_missing(input_objects)
    services_to_create = create_services(
        to_create,
        re.findall("[\w\.]+@[\w\.]+", email)[0],
    )
    if services_to_create:
        log.info("No service to create.")
        return
    if test:
        log.info(f"Missing {len(services_to_create)} services")
        return
    if not repository:
        log.warn("Missing repository")
        return
    log.info(f"Creating {len(services_to_create)} services")
    git_writer.get_repo(repository, branch)
    add_elements_to_file(services_to_create, output)
    git_writer.git_commit_repo(repository, output, commit_message, push=push)
    log.info("Successfully created new services!\n")
