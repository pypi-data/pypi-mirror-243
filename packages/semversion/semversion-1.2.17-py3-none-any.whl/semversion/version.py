from .constants import SEMVERSION_FILE


def version() -> str:
    try:
        with open(SEMVERSION_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The {SEMVERSION_FILE} file was not found. Please create the file with the version number."
        )
