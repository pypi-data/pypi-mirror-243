import json
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


with open('locker/__about__.json', 'r') as fd:
    __version__ = json.load(fd).get("version")


def _requirements():
    with open('requirements.txt', 'r') as f:
        return [name.strip() for name in f.readlines()]


def _requirements_test():
    with open('requirements-test.txt', 'r') as f:
        return [name.strip() for name in f.readlines()]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="lockerpm",
    version=__version__,
    author="CyStack",
    author_email="contact@locker.io",
    url="https://locker.io",
    download_url="",
    description="Locker Secret Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "django",
        "vault management",
        "security"
    ],
    # license = BSD-3-Clause  # Example license
    include_package_data=True,
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
            "venv",
            "projectenv",
            "*.sqlite3"
        ]
    ),
    python_requires=">=3.6",
    install_requires=_requirements(),
    tests_require=_requirements_test(),
    cmdclass={
        'test': PyTest,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
