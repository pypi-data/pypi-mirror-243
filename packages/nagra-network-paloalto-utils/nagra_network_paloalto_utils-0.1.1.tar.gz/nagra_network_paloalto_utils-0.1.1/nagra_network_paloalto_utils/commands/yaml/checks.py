import logging
from pathlib import Path

import click

from nagra_network_paloalto_utils.utils.checks import (
    check_duplicates,
    check_name_length,
    check_tag_presence,
)
from nagra_network_paloalto_utils.utils.common.yamlizer import get_yaml_data

log = logging.getLogger(__name__)


@click.command("check")
@click.option("--file", "source_file", type=Path, help="Input file with rules")
@click.option(
    "--top-level-entry",
    "top_level_entry",
    type=str,
    help="Top level entry of file",
)
@click.option("--tag", help="Tag to check")
@click.option("--max-size", "max_size", type=int, default=None, help="Tag to check")
def check_yamls(source_file, top_level_entry, tag, max_size):
    """
    Used here (updated on 24.11.2023):
    - https://gitlab.kudelski.com/network/paloalto/corporate/nat/-/blob/main/.gitlab-ci.yml?ref_type=heads
    - https://gitlab.kudelski.com/network/paloalto/global/objects/-/blob/master/.gitlab-ci.yml?ref_type=heads
    """
    for file, objects in get_yaml_data(source_file, with_files=True):
        entries = objects[top_level_entry]
        if tag and any(check_tag_presence(entries, tag)):
            raise ValueError(
                f"One or more entry is missing the tag {tag} in file {file}",
            )
        if max_size and any(check_name_length(entries, max_size)):
            raise ValueError(
                f"One or more entry is bigger than {max_size} chars in file {file}",
            )
        duplicates = list(check_duplicates(entries))
        if duplicates:
            raise ValueError(
                f"The following duplicates have been found in file {file.name}: {duplicates}",
            )
