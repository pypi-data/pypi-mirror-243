# Semversion
## Python Semantic Versioning Tool
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/gadc1996/python-workspace)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/gadc1996/semversion/actions/workflows/test.yml/badge.svg)](https://github.com/gadc1996/semversion/actions/workflows/test.yml)
[![Lint](https://github.com/gadc1996/semversion/actions/workflows/lint.yml/badge.svg)](https://github.com/gadc1996/semversion/actions/workflows/lint.yml)
[![Deploy to PyPI](https://github.com/gadc1996/semversion/actions/workflows/deploy_pypi.yml/badge.svg)](https://github.com/gadc1996/semversion/actions/workflows/deploy_pypi.yml)
[![Deploy to PyPI Test](https://github.com/gadc1996/semversion/actions/workflows/deploy_pypi_test.yml/badge.svg)](https://github.com/gadc1996/semversion/actions/workflows/deploy_pypi_test.yml)


`semversion` is a Python module designed to manage and easily modify semantic versions of your projects. With this tool, you can keep a version log and update it as needed.

### Installation

You can install `semversion` using pip:

```bash
$ pip install semversion
```

Running this command for the first time promts for the creation of the `.version` file if it doesnt exists.

Version file can be modified using envirment variable `SEMVERSION_FILE`

### Basic Usage
`semversion` can be used as a standalone python module, mainly for scripting.

```bash
$ python -m semversion <version_part>
```

### Example Usage
```python
from semversion import version, increment, initialize, SEMVERSION_FILE, MAJOR, MINOR, PATCH

# Get the current version
current_version = version()
print(f"Current version: {current_version}")

# Increment the minor version
new_version = increment(MINOR)
print(f"New version: {new_version}")
```


### Contribute

Feel free to contribute! Open an issue or send a pull request.
