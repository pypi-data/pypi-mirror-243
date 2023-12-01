#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import sudo_file

def is_pipx_installed(package_name):
    """Check if a package is installed via pipx."""
    try:
        subprocess.check_output(['pipx', 'list', package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def ensure_hook():
    """Ensures the local apt hook file exists and contains the expected contents."""

    hook_file = "/etc/apt/apt.conf.d/100-robinsw"

    if is_pipx_installed('robin_sd_download'):
        # Adjust this path if the pipx bin directory is different
        pipx_bin_dir = '/home/robin/.local/bin'
        contents = f'APT::Update::Pre-Invoke {{"sudo -u robin {pipx_bin_dir}/robin-sd-download --pull";}};\n'
    else:
        contents = 'APT::Update::Pre-Invoke {"sudo -u robin python3 -m robin_sd_download --pull";};\n'

    if os.path.isfile(hook_file):
        logger.log(message="Hook file exists, checking contents.",
                   log_level="info", to_terminal=False)
        # Ensure the contents of the file match the contents of the variable
        with open(hook_file, "r") as stream:
            if stream.read() == contents:
                logger.log(message="Hook file contents match",
                           log_level="info", to_terminal=False)
                return True
            else:
                logger.log(message="Hook file contents do not match, overwriting.",
                           log_level="error", to_terminal=False)
                # Copy the current file to a backup
                sudo_file.rename_sudo_file(
                    old_path=hook_file, new_path=hook_file + ".bak")
                sudo_file.create_sudo_file(
                    full_path=hook_file, contents=contents)
                return True
    else:
        logger.log(message="Hook file does not exist, creating it at " +
                   hook_file, log_level="info", to_terminal=False)
        sudo_file.create_sudo_file(full_path=hook_file, contents=contents)
        return True
