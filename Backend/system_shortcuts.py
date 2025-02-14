import pyautogui
import os

class SystemShortcuts:
    @staticmethod
    def window_management(command):
        shortcuts = {
            "minimize": "win+down",
            "maximize": "win+up",
            "snap_left": "win+left",
            "snap_right": "win+right",
            "switch_window": "alt+tab",
            "close_window": "alt+f4",
            "desktop": "win+d"
        }
        if command in shortcuts:
            pyautogui.hotkey(*shortcuts[command].split('+'))
            return f"Executed {command} command"
