import logging
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils import git_writer
from nagra_network_paloalto_utils.utils.common.yamlizer import (
    add_elements_to_file,
    get_yaml_data,
)
from nagra_network_paloalto_utils.utils.constants import DEFAULT_GIT_DIR
from nagra_network_paloalto_utils.utils.tags import Tags, extract_tags

log = logging.getLogger(__name__)


@click.group()
def tags():
    pass


@tags.command("generate", help="Generate tags")
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
    "--output",
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
@click.option("--test", type=bool, default=False)
@click.option("--push", type=bool, default=False)
@click.pass_obj
def cmd_generate_missing_tags(
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
    input_tags = extract_tags(get_yaml_data(file))
    tags_from_firewall = Tags(obj.URL, obj.API_KEY)
    missing_tags = tags_from_firewall.find_missing(input_tags)
    tags = [{"name": tag, "owner": email} for tag in missing_tags]
    if not tags:
        log.info("No tag to create")
        return
    if test:
        log.info(f"Missing {len(tags)} tags")
    if not repository:
        log.warn("Repository is missing")
        return
    log.info(f"Creating {len(tags)} tag(s)")
    git_writer.get_repo(repository, branch)
    add_elements_to_file(tags, output)
    git_writer.git_commit_repo(repository, output, commit_message, push=push)
    log.info("Successfully created new tags!\n")
