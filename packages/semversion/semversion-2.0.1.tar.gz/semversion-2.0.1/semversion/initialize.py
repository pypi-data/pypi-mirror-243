from .constants import SEMVERSION_FILE, INITIAL_VERSION


def initialize():
    with open(SEMVERSION_FILE, "w") as file:
        file.write(INITIAL_VERSION)
