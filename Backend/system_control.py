import subprocess
import ctypes
import time
import winreg as reg
import os
import pythoncom  # Add this import at the top
import re
from time import sleep
class SystemControl:
    def __init__(self):
        self.reg_paths = {
            'personalize': r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            'desktop': r"Control Panel\Desktop",
            'explorer': r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            'power': r"System\CurrentControlSet\Control\Power\PowerSettings",
            'defender': r"SOFTWARE\Microsoft\Windows Defender",
            'mouse': r"Control Panel\Mouse",
            'keyboard': r"Control Panel\Keyboard"
        }
        self.reg_paths.update({
            'dwm': r"SOFTWARE\Microsoft\Windows\DWM",
            'desktop': r"Control Panel\Desktop",
            'personalization': r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            'network': r"SYSTEM\CurrentControlSet\Control\Network",
            'defender': r"SOFTWARE\Microsoft\Windows Defender",
            'explorer_adv': r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            'wsearch': r"SOFTWARE\Microsoft\Windows Search",
            'uwp': r"SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current",
            'network_adapters': r"SYSTEM\CurrentControlSet\Control\Network",
            'wifi_settings': r"SOFTWARE\Microsoft\Windows\CurrentVersion\Network\Windows Connection Manager"
        })

    @staticmethod
    def run_command(command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"Error executing command: {e}")
            return None

    def toggle_wifi(self, action="toggle"):
        """
        Control WiFi adapter using registry and netsh
        :param action: "on", "off", or "toggle"
        """
        try:
            # Get list of network adapters
            adapters_cmd = 'powershell "Get-NetAdapter | Where-Object {$_.InterfaceDescription -Match \'Wireless|WiFi|802.11\'} | Select-Object -ExpandProperty Name"'
            wifi_adapters = subprocess.check_output(adapters_cmd, shell=True, text=True).strip().split('\n')
            
            if not wifi_adapters:
                print("No WiFi adapter found")
                return False

            wifi_adapter = wifi_adapters[0].strip()
            
            # Get current state using PowerShell
            state_cmd = f'powershell "Get-NetAdapter -Name \'{wifi_adapter}\' | Select-Object -ExpandProperty Status"'
            current_state = subprocess.check_output(state_cmd, shell=True, text=True).strip()
            
            # Determine action
            if action.lower() in ["on", "enable", "turn on"]:
                if current_state.lower() != "up":
                    enable_cmd = f'netsh interface set interface name="{wifi_adapter}" admin=enabled'
                    subprocess.run(enable_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f"WiFi adapter '{wifi_adapter}' enabled successfully")
                else:
                    print("WiFi is already enabled")
                return True
                
            elif action.lower() in ["off", "disable", "turn off"]:
                if current_state.lower() != "disabled":
                    disable_cmd = f'netsh interface set interface name="{wifi_adapter}" admin=disabled'
                    subprocess.run(disable_cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    print(f"WiFi adapter '{wifi_adapter}' disabled successfully")
                else:
                    print("WiFi is already disabled")
                return True
            
            # Toggle current state
            else:
                if current_state.lower() == "up":
                    return self.toggle_wifi("off")
                else:
                    return self.toggle_wifi("on")

        except Exception as e:
            print(f"Error controlling WiFi: {e}")
            return False


    @staticmethod
    def set_brightness(level):
        """Set screen brightness (0-100)"""
        try:
            # Initialize COM for this thread
            pythoncom.CoInitialize()
            
            level = max(0, min(100, int(level)))  # Ensure level is between 0-100
            import wmi
            brightness = None
            methods = None
            
            try:
                brightness = wmi.WMI(namespace='wmi')
                methods = brightness.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(level, 0)
                print(f"Successfully set brightness to {level}%")
                return True
            finally:
                # Properly release WMI objects
                if methods:
                    methods = None
                if brightness:
                    brightness = None
                # Clean up COM
                pythoncom.CoUninitialize()
                
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False

    def toggle_airplane_mode(self, action="toggle"):
        """Control airplane mode"""
        try:
            NETWORK_ADAPTER_GUID = "{A48F1177-C907-4DCD-973A-E17DD1B34D72}"
            if action.lower() == "on":
                self.run_command(f"netsh interface set interface '{NETWORK_ADAPTER_GUID}' disabled")
                return "Airplane mode turned on"
            elif action.lower() == "off":
                self.run_command(f"netsh interface set interface '{NETWORK_ADAPTER_GUID}' enabled")
                return "Airplane mode turned off"
            else:
                current_state = self.run_command(f"netsh interface show interface '{NETWORK_ADAPTER_GUID}'")
                if "Disabled" in current_state:
                    return self.toggle_airplane_mode("off")
                else:
                    return self.toggle_airplane_mode("on")
        except Exception as e:
            return f"Error controlling airplane mode: {e}"

    def lock_screen(self):
        """Lock the computer screen"""
        ctypes.windll.user32.LockWorkStation()
        return "Screen locked"

    def toggle_night_light(self, action="toggle"):
        """Control night light feature"""
        try:
            import winreg as reg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.bluelightreductionstate\windows.data.bluelightreduction.bluelightreductionstate"
            
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS) as key:
                if action.lower() == "on":
                    reg.SetValueEx(key, "Data", 0, reg.REG_BINARY, b'\x02\x00\x00\x00')
                    return "Night light turned on"
                elif action.lower() == "off":
                    reg.SetValueEx(key, "Data", 0, reg.REG_BINARY, b'\x00\x00\x00\x00')
                    return "Night light turned off"
                else:
                    current_state = reg.QueryValueEx(key, "Data")[0]
                    if current_state == b'\x00\x00\x00\x00':
                        return self.toggle_night_light("on")
                    else:
                        return self.toggle_night_light("off")
        except Exception as e:
            return f"Error controlling night light: {e}"

    def set_registry_value(self, key_path, name, value, value_type=reg.REG_DWORD):
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, name, 0, value_type, value)
            return True
        except Exception as e:
            print(f"Error setting registry value: {e}")
            return False

    def toggle_hidden_files(self, show=True):
        """Show/hide hidden files and folders"""
        value = 1 if show else 2
        return self.set_registry_value(self.reg_paths['explorer'], "Hidden", value)

    def toggle_file_extensions(self, show=True):
        """Show/hide file extensions"""
        value = 0 if show else 1
        return self.set_registry_value(self.reg_paths['explorer'], "HideFileExt", value)

    def set_mouse_settings(self, speed=10, double_click=500):
        """Configure mouse settings"""
        self.set_registry_value(self.reg_paths['mouse'], "MouseSpeed", str(speed), reg.REG_SZ)
        self.set_registry_value(self.reg_paths['mouse'], "DoubleClickSpeed", str(double_click), reg.REG_SZ)

    def set_keyboard_settings(self, repeat_delay=500, repeat_rate=31):
        """Configure keyboard settings"""
        self.set_registry_value(self.reg_paths['keyboard'], "KeyboardDelay", str(repeat_delay), reg.REG_SZ)
        self.set_registry_value(self.reg_paths['keyboard'], "KeyboardSpeed", str(repeat_rate), reg.REG_SZ)

    def toggle_transparency(self, enable=True):
        """Enable/disable transparency effects"""
        value = 1 if enable else 0
        return self.set_registry_value(r"SOFTWARE\Microsoft\Windows\DWM", "TransparencyEnabled", value)

    def set_power_plan(self, plan="balanced"):
        """Set power plan (balanced, power_saver, high_performance)"""
        plans = {
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a",
            "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
        }
        if plan in plans:
            self.run_command(f"powercfg /s {plans[plan]}")
            return f"Power plan set to {plan}"
        return "Invalid power plan"

    def toggle_taskbar_settings(self, combine="always"):
        """Configure taskbar button combining"""
        values = {"always": 0, "full": 1, "never": 2}
        if combine in values:
            return self.set_registry_value(self.reg_paths['explorer'], "TaskbarGlomLevel", values[combine])
        return False

    def toggle_game_mode(self, enable=True):
        """Enable/disable Windows Game Mode"""
        value = 1 if enable else 0
        return self.set_registry_value(
            r"Software\Microsoft\GameBar",
            "AllowAutoGameMode",
            value
        )

    def toggle_system_sounds(self, enable=True):
        """Enable/disable system sounds"""
        value = 1 if enable else 0
        return self.set_registry_value(
            r"AppEvents\Schemes",
            "App",
            value
        )

    def toggle_fast_startup(self, enable=True):
        """Enable/disable fast startup"""
        value = 1 if enable else 0
        try:
            with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Power", 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, "HiberbootEnabled", 0, reg.REG_DWORD, value)
            return True
        except Exception:
            return False

    def set_accent_color(self, enable=True, color=None):
        """Set system accent color"""
        self.set_registry_value(self.reg_paths['dwm'], "ColorPrevalence", 1 if enable else 0)
        if color:
            self.set_registry_value(self.reg_paths['dwm'], "AccentColor", color, reg.REG_DWORD)

    def set_wallpaper(self, image_path):
        """Set desktop wallpaper"""
        if os.path.exists(image_path):
            self.set_registry_value(self.reg_paths['desktop'], "Wallpaper", image_path, reg.REG_SZ)
            self.run_command(f'RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True')
            return True
        return False

    def disable_lock_screen(self, disable=True):
        """Disable/enable lock screen"""
        return self.set_registry_value(self.reg_paths['personalization'], "NoLockScreen", 1 if disable else 0)

    def toggle_hibernation(self, enable=True):
        """Enable/disable system hibernation"""
        value = "enable" if enable else "disable"
        return self.run_command(f"powercfg /h {value}")

    def manage_startup_program(self, program_path, name, add=True):
        """Add/remove program from startup"""
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
                if add:
                    reg.SetValueEx(key, name, 0, reg.REG_SZ, program_path)
                else:
                    reg.DeleteValue(key, name)
            return True
        except Exception as e:
            print(f"Error managing startup: {e}")
            return False

    def set_default_apps(self, app_type, app_path):
        """Set default applications"""
        app_types = {
            "browser": "http",
            "mail": "mailto",
            "music": "audio",
            "video": "video",
            "photo": "image",
            "pdf": "pdf"
        }
        if app_type in app_types:
            protocol = app_types[app_type]
            try:
                key_path = f"SOFTWARE\\Classes\\{protocol}\\shell\\open\\command"
                with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key_path, 0, reg.KEY_SET_VALUE) as key:
                    reg.SetValueEx(key, "", 0, reg.REG_SZ, f'"{app_path}" "%1"')
                return True
            except Exception:
                return False
        return False

    def toggle_cortana(self, enable=True):
        """Enable/disable Cortana"""
        return self.set_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            "AllowCortana",
            1 if enable else 0
        )

    def toggle_search_indexing(self, enable=True):
        """Enable/disable Windows Search indexing"""
        service_command = "start" if enable else "stop"
        self.run_command(f"net {service_command} WSearch")
        return True

    def set_mouse_settings(self, speed=None, double_click=None, scroll_lines=None):
        """Configure mouse settings"""
        if speed:
            self.set_registry_value(self.reg_paths['mouse'], "MouseSensitivity", str(speed), reg.REG_SZ)
        if double_click:
            self.set_registry_value(self.reg_paths['mouse'], "DoubleClickSpeed", str(double_click), reg.REG_SZ)
        if scroll_lines:
            self.set_registry_value(self.reg_paths['mouse'], "WheelScrollLines", str(scroll_lines), reg.REG_SZ)

    def toggle_taskbar_features(self, feature, enable=True):
        """Configure taskbar features"""
        features = {
            "small_icons": ("TaskbarSmallIcons", 1 if enable else 0),
            "combine": ("TaskbarGlomLevel", 0 if enable else 2),
            "recent_apps": ("Start_TrackProgs", 1 if enable else 0)
        }
        if feature in features:
            name, value = features[feature]
            return self.set_registry_value(self.reg_paths['explorer_adv'], name, value)

if __name__ == "__main__":

    system_control = SystemControl()
    # system_control.toggle_wifi("off")  # Turn off WiFi
