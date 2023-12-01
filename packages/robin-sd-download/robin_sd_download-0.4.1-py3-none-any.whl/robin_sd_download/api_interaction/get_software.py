#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import datetime
import glob
import re

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger


def generate_response_content(response, chunk_size=8192):
    try:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                yield chunk
    except KeyboardInterrupt:
        response.close()
        raise


def create_backup_if_exists(folder_path):
    if os.path.exists(folder_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_folder = os.path.join(os.path.dirname(folder_path), "backup")
        os.makedirs(backup_folder, exist_ok=True)

        backup_file_name = f"{os.path.basename(folder_path)}_backup_{timestamp}.zip"
        backup_file_path = os.path.join(backup_folder, backup_file_name)

        with zipfile.ZipFile(backup_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(
                        file_path, folder_path))

        logger.log(
            message=f"Created a backup: {backup_file_path}", log_level="info", to_terminal=True)

        # Keep only the last 3 backup files
        backup_files = glob.glob(os.path.join(
            backup_folder, f"{os.path.basename(folder_path)}_backup_*.zip"))
        backup_files.sort(key=os.path.getctime, reverse=True)

        while len(backup_files) > 3:
            oldest_file = backup_files.pop()
            os.remove(oldest_file)
            logger.log(
                message=f"Removed old backup: {oldest_file}", log_level="info", to_terminal=True)


def extract_version(file_name):
    version_pattern = re.compile(r'\d+\.\d+\.\d+')
    match = version_pattern.search(file_name)

    if match:
        return match.group(0)
    else:
        return None


def get_local_version(file_location):
    local_software_files = glob.glob(os.path.join(file_location, "*"))
    local_software_files.sort(key=os.path.getctime, reverse=True)

    if local_software_files:
        return extract_version(local_software_files[0])
    else:
        return None


def get_server_version(response):
    file_name = response.headers.get("Content-Disposition").split("=")[1]
    file_name = file_name.replace('"', '').replace('.zip', '')
    return extract_version(file_name), file_name


def download_file(response, file_location, file_name):
    write_file = os.path.join(file_location, f"{file_name}.zip")

    with open(write_file, 'wb') as f:
        try:
            for chunk in generate_response_content(response, chunk_size=8192):
                f.write(chunk)
        except KeyboardInterrupt:
            logger.log(
                message="Download interrupted by user, cleaning up...",
                log_level="warning", to_terminal=True)
            f.close()
            os.remove(write_file)
            return 1

    logger.log(message="Downloaded to " + write_file,
               log_level="info", to_terminal=True)

    return write_file


def extract_and_cleanup(file_location, file_name, write_file):
    extracted_folder_path = os.path.join(file_location, f"{file_name}")

    try:
        create_backup_if_exists(extracted_folder_path)

        with zipfile.ZipFile(write_file, "r") as zip_ref:
            zip_ref.extractall(extracted_folder_path)
    except zipfile.BadZipFile:
        logger.log(message="The downloaded file is not a valid zip file",
                   log_level="error", to_terminal=True)
        return 1

    os.remove(write_file)
    return 0


def get_software():
    config = yaml_parser.parse_config()
    radar_id = config['radar_id']
    request_url = config['api_url']
    file_location = config['static']['download_location']

    # Get bearer_token
    try:
        bearer_token = str(get_bearer_token.get_bearer_token())
    except Exception as e:
        logger.log(
            message=f"Failed to get bearer token: {str(e)}", log_level="error", to_terminal=True)
        return 1

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_endpoint = '/api/radars/' + radar_id + '/software'

    # Get server response
    try:
        response = requests.get(
            request_url + api_endpoint, allow_redirects=True, headers=headers, stream=True)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.log(
            message=f"Failed to get software: {str(e)}", log_level="error", to_terminal=True)
        return 1

    server_version, file_name = get_server_version(response)
    local_version = get_local_version(file_location)

    if server_version and local_version and server_version == local_version:
        logger.log(
            message="The latest software version is already present. Skipping download.",
            log_level="info", to_terminal=True)
        return 0

    os.makedirs(file_location, exist_ok=True)

    write_file = download_file(response, file_location, file_name)
    if write_file == 1:
        return 1

    return extract_and_cleanup(file_location, file_name, write_file)
