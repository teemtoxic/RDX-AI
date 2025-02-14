import requests
import subprocess
import os
from Data.responces import software_installation_link

# ...existing code...

def download_application(url, destination):
    """
    Downloads an application from the given URL to the specified destination.
    
    :param url: The URL to download the application from.
    :param destination: The file path to save the downloaded application.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded application from {url} to {destination}")
        install_application(destination)
    else:
        print(f"Failed to download application from {url}. Status code: {response.status_code}")

def install_application(file_path):
    """
    Installs the application from the given file path.
    
    :param file_path: The file path of the downloaded application.
    """
    try:
        subprocess.run([file_path], check=True)
        print(f"Installed application from {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install application from {file_path}. Error: {e}")

def download_and_install_software(software_name):
    software_name = software_name.lower().strip()
    software_name = software_name.replace("install", "").strip()
    """
    Finds the download link for the given software name and downloads and installs the software.
    
    :param software_name: The name of the software to download and install.
    """
    url = software_installation_link.get(software_name.lower())
    if url:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        destination = os.path.join(downloads_folder, f"{software_name}_installer.exe")
        download_application(url, destination)
    else:
        print(f"No download link found for software: {software_name}")



