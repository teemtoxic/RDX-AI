import requests
import os
import shutil
import zipfile
import sys
import subprocess
from dotenv import dotenv_values
from rich import print

# Configuration
REPO_URL = "https://api.github.com/repos/Anuj-Yadav8/RDX-AI/releases/latest"
BACKUP_DIR = "_backup"
VERSION_FILE = "version.txt"
env_vars = dotenv_values(".env")

def check_for_update():
    try:
        response = requests.get(REPO_URL)
        if response.status_code == 200:
            latest_version = response.json()['tag_name']
            with open(VERSION_FILE, "r") as f:
                current_version = f.read().strip()
            return latest_version != current_version, latest_version
    except Exception as e:
        print(f"[red]Update check failed: {str(e)}[/red]")
    return False, None

def download_update(version):
    try:
        # Get download URL from GitHub release
        response = requests.get(REPO_URL)
        download_url = response.json()['zipball_url']
        
        # Download the release zip
        print(f"[yellow]Downloading update {version}...[/yellow]")
        response = requests.get(download_url)
        
        # Save the zip file
        with open("update.zip", "wb") as f:
            f.write(response.content)
            
        return True
    except Exception as e:
        print(f"[red]Download failed: {str(e)}[/red]")
        return False

def backup_current_version():
    try:
        if os.path.exists(BACKUP_DIR):
            shutil.rmtree(BACKUP_DIR)
        os.makedirs(BACKUP_DIR)
        
        # Copy all files except backup dir and update files
        for item in os.listdir():
            if item not in [BACKUP_DIR, "update.zip", "update"]:
                if os.path.isfile(item):
                    shutil.copy2(item, BACKUP_DIR)
                elif os.path.isdir(item):
                    shutil.copytree(item, os.path.join(BACKUP_DIR, item))
        return True
    except Exception as e:
        print(f"[red]Backup failed: {str(e)}[/red]")
        return False

def apply_update():
    try:
        # Extract update files
        with zipfile.ZipFile("update.zip") as zip_ref:
            zip_ref.extractall("update")
            
        # Get extracted folder name
        extracted_dir = os.path.join("update", os.listdir("update")[0])
        
        # Copy new files
        for item in os.listdir(extracted_dir):
            src = os.path.join(extracted_dir, item)
            dst = os.path.normpath(item)
            
            if os.path.exists(dst):
                if os.path.isfile(dst):
                    os.remove(dst)
                else:
                    shutil.rmtree(dst)
            
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            else:
                shutil.copytree(src, dst)
                
        # Cleanup
        shutil.rmtree("update")
        os.remove("update.zip")
        
        # Update version file
        needs_update, latest_version = check_for_update()
        with open(VERSION_FILE, "w") as f:
            f.write(latest_version)
            
        return True
    except Exception as e:
        print(f"[red]Update failed: {str(e)}[/red]")
        # Restore backup if available
        if os.path.exists(BACKUP_DIR):
            print("[yellow]Restoring backup...[/yellow]")
            for item in os.listdir(BACKUP_DIR):
                src = os.path.join(BACKUP_DIR, item)
                dst = os.path.normpath(item)
                
                if os.path.exists(dst):
                    if os.path.isfile(dst):
                        os.remove(dst)
                    else:
                        shutil.rmtree(dst)
                
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                else:
                    shutil.copytree(src, dst)
        return False

def restart_application():
    python = sys.executable
    subprocess.Popen([python, "main.py"])
    sys.exit()

def main():
    print("[bold]Checking for updates...[/bold]")
    needs_update, latest_version = check_for_update()
    
    if needs_update:
        print(f"[yellow]New version available: {latest_version}[/yellow]")
        if download_update(latest_version):
            if backup_current_version():
                if apply_update():
                    print("[green]Update successful! Restarting...[/green]")
                    # Update requirements
                    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                    restart_application()
    else:
        print("[green]Already up to date![/green]")

if __name__ == "__main__":
    main()
