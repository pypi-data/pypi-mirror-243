import json
from time import sleep

import click

from .silaspoofer import StartServers


@click.command()
# @click.argument("config", type=click.File("r"))
@click.argument("config", type=click.File("r"))
def main(config):
    config = json.load(config)

    StartServers(config)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")


# check how python handles this in a package
if __name__ == "__main__":
    main()
