import click

from .addresses import addresses
from .applications import applications
from .services import services
from .tags import tags


@click.group()
def objects():
    pass


objects.add_command(addresses)
objects.add_command(services)
objects.add_command(tags)
objects.add_command(applications)
