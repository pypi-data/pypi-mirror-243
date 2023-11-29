#!/usr/bin/env python
####
# fprime Python Package:
#
# The F prime python package represents the core data types required to use or develop F prime
# python code. This includes both the F prime GDS and Test API, as well as the Autocoding tools.
# To install this package, run the following commands:
#
# User Install / Upgrade:
# ```
# pip install --upgrade fprime-tools
# ```
#
# Developer and Dynamic Installation:
# ```
# pip install -e ./Fw/Python
# ```
###
from setuptools import find_packages, setup

# Setup a python package using setup-tools. This is a newer (and more recommended) technology
# then distutils.
setup(
    ####
    # Package Description:
    #
    # Basic package information. Describes the package and the data contained inside. This
    # information should match the F prime description information.
    ####
    name="fprime-tools",
    use_scm_version={"root": ".", "relative_to": __file__},
    license="Apache 2.0 License",
    description="F Prime Flight Software core data types",
    long_description="""
This package contains the necessary core data types used by F prime. Users who seek to develop tools,
utilities, and other libraries used to interact with F prime framework code can use these data types
to interact with the data coming from the FSW.
    """,
    url="https://github.com/nasa/fprime",
    keywords=["fprime", "embedded", "nasa"],
    project_urls={"Issue Tracker": "https://github.com/nasa/fprime/issues"},
    # Author of Python package, not F prime.
    author="Michael Starch",
    author_email="Michael.D.Starch@jpl.nasa.gov",
    ####
    # Included Packages:
    #
    # Will search for and included all python packages under the "src" directory.  The root package
    # is set to 'src' to avoid package names of the form src.fprime.
    ####
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "fprime": [
            "cookiecutter_templates/*",
            "cookiecutter_templates/*/*",
            "cookiecutter_templates/*/*/*",
            "cookiecutter_templates/*/*/*/*",
            "cookiecutter_templates/**/.*",
        ]
    },
    ####
    # Classifiers:
    #
    # Standard Python classifiers used to describe this package.
    ####
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    # Requires Python 3.8+
    python_requires=">=3.8",
    install_requires=[
        "lxml>=4.6.3",
        "Markdown>=3.3.4",
        "pexpect>=4.8.0",
        "pytest>=6.2.4",
        "Cheetah3>=3.2.6",
        "cookiecutter>=2.2.3",
        "gcovr>=6.0",
        "urllib3<2.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "black",
            "pylama",
            "pylint",
            "pre-commit",
            "sphinx",
            "sphinxcontrib.mermaid",
            "sphinx-rtd-theme",
            "sphinx-autoapi",
            "sphinx-autoapi",
            "recommonmark",
        ]
    },
    # Setup and test requirements, not needed by normal install
    setup_requires=["pytest-runner", "setuptools_scm"],
    tests_require=["pytest"],
    # Create a set of executable entry-points for running directly from the package
    entry_points={
        "console_scripts": [
            "fprime-util = fprime.util.__main__:main",
            "fprime-version-check = fprime.util.versioning:main",
        ],
        "gui_scripts": [],
    },
)
