from .version import version
from .constants import SEMVERSION_FILE, MAJOR, MINOR, PATCH


def _write_version(new_version):
    with open(SEMVERSION_FILE, "w") as version_file:
        version_file.write(new_version)


def increment(part):
    try:
        current_version = version()
        components = list(map(int, current_version.split(".")))

        if part == MAJOR:
            components[MAJOR] += 1
            components[MINOR] = 0
            components[PATCH] = 0
        elif part == MINOR:
            components[MINOR] += 1
            components[PATCH] = 0
        elif part == PATCH:
            components[PATCH] += 1

        new_version = ".".join(map(str, components))
        _write_version(new_version)
        return new_version
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The {SEMVERSION_FILE} file was not found. Please create the file with the version number."
        )
