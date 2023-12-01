#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pypi_simple import PyPISimple
import sys
import warnings
from pypi_simple.util import UnexpectedRepoVersionWarning

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download import _version


def check_latest_version():
    """Check if the latest version is installed and document how to update if needed."""
    config = yaml_parser.parse_config()

    package_name = config['static']['app_name']

    current_version = _version.__version__

    pypi = PyPISimple()

    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter(
                "always", category=UnexpectedRepoVersionWarning)
            page = pypi.get_project_page(package_name)
            latest_version = page.packages[-1].version

            if any(issubclass(warning.category, UnexpectedRepoVersionWarning) for warning in w):
                logger.log(message="Consider updating to Python 3.7 or higher to avoid unexpected PyPiSimple version checker behavior.",
                           log_level="warning", to_terminal=True)
    except Exception as e:
        logger.log(message="Failed to connect to PyPISimple (version checker). Check your internet connection.",
                   log_level="error", to_terminal=True)
        sys.exit(1)

    if current_version == latest_version:
        logger.log(message="Latest version detected, proceeding.",
                   log_level="info", to_terminal=False)
    else:
        logger.log(message="Newer version detected, please update.",
                   log_level="error", to_terminal=True)
        logger.log(message="Current version: " + current_version,
                   log_level="error", to_terminal=True)
        logger.log(message="Latest version: " + latest_version,
                   log_level="error", to_terminal=True)
        logger.log(message="To update, run: pip3 install --upgrade " +
                   package_name, log_level="error", to_terminal=True)
        sys.exit(1)
