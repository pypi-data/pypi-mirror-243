import logging

import click
from nagra_network_misc_utils.logger import set_default_logger

from .dump_dir import dump_dir

set_default_logger()
logging.getLogger().setLevel(logging.INFO)


@click.group()
def cli():
    pass


cli.add_command(dump_dir)

if __name__ == "__main__":
    cli()
