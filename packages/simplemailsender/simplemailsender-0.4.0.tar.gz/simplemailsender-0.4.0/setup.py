# setup.py
# Setup installation for the application

from setuptools import find_namespace_packages, setup
import os

BASE_DIR = os.environ.get("BASE_DIR", None)
BASE_DIR = "." if BASE_DIR is None else BASE_DIR

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simplemailsender",
    version="0.4.0",
    license="Apache",
    description="A simple mail sender.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alberto Burgos Plaza",
    author_email="albertoburgosplaza@gmail.com",
    url="https://github.com/aburgoscimne/simplemailsender",
    keywords=[
        "e-mail",
    ],
    packages=find_namespace_packages(),
    python_requires=">=3.8",
)
