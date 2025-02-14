import subprocess

def uninstall_software(software_name):
    """
    Uninstalls the specified software using PowerShell commands for both Store apps and traditional apps.
    
    :param software_name: The name of the software to uninstall
    """
    try:
        # Try removing Windows Store app first
        store_app_command = f'Get-AppxPackage *{software_name}* | Remove-AppxPackage'
        subprocess.run(['powershell', '-Command', store_app_command], 
                     shell=True,
                     capture_output=True)

        # Try removing traditional desktop app
        win32_command = (
            f'$app = Get-WmiObject -Class Win32_Product | '
            f'Where-Object {{$_.Name -like "*{software_name}*"}}; '
            f'if ($app) {{$app.Uninstall()}}'
        )
        result = subprocess.run(['powershell', '-Command', win32_command],
                              shell=True,
                              capture_output=True,
                              text=True)
        
        # Check Control Panel programs
        control_panel_command = (
            f'Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | '
            f'Where-Object {{$_.DisplayName -like "*{software_name}*"}} | '
            f'Select-Object DisplayName, UninstallString'
        )
        result = subprocess.run(['powershell', '-Command', control_panel_command],
                              shell=True,
                              capture_output=True,
                              text=True)
        
        if result.stdout.strip():
            print(f"Found {software_name}. Attempting to uninstall...")
            print("Please complete the uninstallation in any popup windows that appear.")
            return True
        else:
            print(f"Software '{software_name}' not found in the system")
            return False
            
    except Exception as e:
        print(f"An error occurred while trying to uninstall {software_name}: {e}")
        return False

# Example usage
if __name__ == "__main__":
    app_name = "WhatsApp"
    uninstall_software(app_name)
