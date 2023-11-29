import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kraken-thing",
    version="0.0.44",
    description="Kraken thing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tactik8/krakcn_class_thing_v4",
    author="Tactik8",
    author_email="info@tactik8.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(include=['kraken_thing', 'kraken_thing.*']),
    include_package_data=True,
    install_requires=['python-dateutil', 'sigfig', 'kraken-schema-org', 'requests', 'tabulate', 'bson', 'pymongo' , 'flask', 'aiohttp'],

)

