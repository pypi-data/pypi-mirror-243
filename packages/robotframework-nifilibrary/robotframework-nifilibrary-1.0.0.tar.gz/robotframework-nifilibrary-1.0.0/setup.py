from setuptools import setup, find_packages
import re

# Read version from file without loading the module
with open('NifiLibrary/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)

with open("README.md", "r") as fh:
    long_description = fh.read()

if version_match:
    VERSION = version_match.group(1)
else:
    VERSION = '0.1'

REQUIREMENTS = [
    i.strip() for i in open("requirements.txt", encoding="utf8").readlines()
]

TEST_REQUIREMENTS = [
    'coverage', 'wheel', 'unittest'
]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Testing",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup(
    name="robotframework-nifilibrary",
    version=VERSION,
    author="Weeraporn.pai",
    author_email="weeraporn.pa@gmail.com",
    description="Nifi library for robotframework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    license="MIT",
    packages=find_packages(),
    package_dir={'robotframework-nifilibrary': 'NifiLibrary'},
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    classifiers=CLASSIFIERS
)