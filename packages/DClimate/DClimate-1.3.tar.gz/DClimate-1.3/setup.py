# pylint: disable=C0114
from pathlib import Path
import setuptools


setuptools.setup(
    name="DClimate",
    version="1.3",
    author="DayaJangam",
    long_description=Path("README.md").read_text(),  # pylint: disable=W1514
    packages=setuptools.find_packages(exclude=["tests", "data"])

)
