from setuptools import setup, find_packages
from semversion import version

setup(
    name="semversion",
    version=version(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "semversion=semversion.__main__:main",
        ],
    },
    install_requires=[
        "click",
    ],
)
