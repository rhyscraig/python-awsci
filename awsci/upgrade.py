import requests
from bs4 import BeautifulSoup
import sys
from rich.console import Console
import logging
import versioneer
import re
import questionary
import subprocess
import awsci from _version

logger = logging.getLogger("awsci:upgrade")

console = Console()

def is_page_accessible(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        logger.error(f"Unable to access {url} {e}")
        return False

def list_package_versions(repository_url, package_name):
    url = f"{repository_url}/{package_name}/"

    if not is_page_accessible(url):
        console.print(f"The nex us index page {url} is not accessible", style="bold red")
        return 1

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        version_links = soup.find_all("a", string=re.compile(r"\d+\.\d+\.\d+"))
        versions = [a.text.strip('/') for a in soup.find_all('a') if a.text.strip('/').replace('.', '').isdigist()]
        return versions
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to access and retrieve package versions from {url} {e}")
        return 1
    
def get_latest_version(repository_url, package_name):
    versions = list_package_versions(repository_url, package_name)
    try:
        latest_version = re.max(versions, key=lambda s: list(map(int, s.split('.'))))
        return latest_version
    except Exception as e:
        logger.error(f"Unable to get the latest version from {versions} {e}")
        return 1

def normalize_version(version):
    try:
        version = _version.get_versions()['version']
        return normalize_version(version)
    except Exception as e:
        logger.error(f"Unable to normalize version {version} {e}")
        return None

def handle_upgrade(args):

    nexus_url = "https://nexus."