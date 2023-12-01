#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import sys
import datetime


def validate_config(config):
    if config is None:
        return False, "Could not parse YAML config file"

    required_keys = {
        'api_url': "api_url is not defined in config",
        'customer': "customer is not defined in config",
        'customer.name': "customer.name is not defined in config",
        'log': "log is not defined in config",
        'log.file': "log.file is not defined in config",
        'log.level': "log.level is not defined in config",
        'radar_id': "radar_id is not defined in config",
        'robin_email': "radar_email is not defined in config",
        'robin_password': "radar_password is not defined in config",
        'slack': "slack is not defined in config",
        'slack.channel': "slack.channel is not defined in config",
        'slack.token': "slack.token is not defined in config",
        'static': "static is not defined in config",
        'static.app_name': "static.app_name is not defined in config",
        'static.download_location': "static.download_location is not defined in config"
    }

    for key, error_msg in required_keys.items():
        keys = key.split('.')
        value = config
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return False, error_msg

    return True, "Config is valid"


def check_file_format(file_path):
    try:
        with open(file_path, 'r') as config_file:
            yaml.safe_load(config_file)
        return True
    except yaml.YAMLError as e:
        print(f"Error: {file_path} is not in valid yaml format. {e}")
        return False


def get_keys(config):
    return list(config.keys()) if config else None


def check_and_ask(config):
    if isinstance(config, dict):
        for key in config:
            if config[key] is None:
                config[key] = input(f"Please enter a value for {key}: ")
            elif isinstance(config[key], dict):
                check_and_ask(config[key])


def parse_config():
    config_files = [
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), ".sd-download-config.yml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), ".sd-download-config.yaml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), "sd-download-config.yml"),
        os.path.join(os.path.expanduser(
            "/opt/robin/config/sd-download"), "sd-download-config.yaml"),
        os.path.join(os.path.expanduser("~"), ".sd-download-config.yml"),
        os.path.join(os.path.expanduser("~"), ".sd-download-config.yaml"),
        "sd-download-config.yml",
        "sd-download-config.yaml"
    ]

    config = None
    file = None

    for cfg_file in config_files:
        if os.path.isfile(cfg_file) and check_file_format(cfg_file):
            with open(cfg_file, 'r') as config_file:
                config = yaml.safe_load(config_file)
                file = cfg_file
                print_used_config_file(cfg_file)
                break

    if not config:
        admin_interface = "https://software-api-admin.robinradar.systems"
        doc_pages = "https://robinradar.atlassian.net/wiki/spaces/DEV/pages/284033095/Software+Deployment+API"
        print(f"Error: no config file found, or its contents are missing. Please check it.")
        print(f"Please browse to {admin_interface} to create a config file.")
        print(f"Please browse to {doc_pages} to learn how to create a config file.")
        sys.exit(0)

    is_valid, result = validate_config(config)
    if not is_valid:
        error_message = f"Configuration error: {result}"
        print(error_message)
        sys.exit(1)

    return config


def print_used_config_file(cfg_file):
    if print_used_config_file.last_cfg_file != cfg_file:
        cet_tz = datetime.timezone(datetime.timedelta(hours=1), 'CET')
        print(f"{datetime.datetime.now(cet_tz).strftime('%Y-%m-%d %H:%M:%S')} +0100 - INFO - Using config file: {cfg_file}")
        print_used_config_file.last_cfg_file = cfg_file


print_used_config_file.last_cfg_file = None
