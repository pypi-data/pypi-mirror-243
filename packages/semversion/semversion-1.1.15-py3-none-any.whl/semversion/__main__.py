import click

from .version import version
from .initialize import initialize
from .increment import increment
from .constants import MAJOR, MINOR, PATCH


@click.command()
@click.argument("version_part", type=click.Choice(["minor", "major", "patch"]))
def main(version_part):
    """Manage project version"""

    try:
        current_version = version()
        click.echo(f"Current version: {current_version}")
        click.echo(f"Updating {version_part} version...")
    except FileNotFoundError:
        click.confirm(".version file not found. Do you want to create it?", abort=True)
        initialize()
        click.secho(".version file created sucessfully", fg="green")

    if version_part == "minor":
        new_version = increment(MINOR)
    elif version_part == "major":
        new_version = increment(MAJOR)
    elif version_part == "patch":
        new_version = increment(PATCH)

    click.secho(f"New version: {new_version}", fg="green")


if __name__ == "__main__":
    main()
