import logging

import click

from nagra_network_paloalto_utils.utils.git_writer import git_push_folder

log = logging.getLogger(__name__)


@click.command("push_folder")
@click.option(
    "--repository",
    "repo_name",
    help="Name of repository (e.g. network/paloalto/utils)",
)
@click.option(
    "--branch",
    "branch",
    envvar="CI_COMMIT_REF_NAME",
    help="Reference of the branch/tag/commit (e.g. 'refs/heads/master' )",
)
@click.option(
    "--git-server",
    "server",
    help="Name of server (e.g. gitlab.kudelski.com)",
    default="gitlab.kudelski.com",
)
def cmd_push_folder(repo_name, server, branch):
    if repo_name is not None:
        git_push_folder(repo_name, server, branch)
    else:
        git_push_folder(branch=branch)
