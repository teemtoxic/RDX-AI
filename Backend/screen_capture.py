import pyautogui
import os
from datetime import datetime


def take_screenshot():
    try:
        # Create Screenshots directory if it doesn't exist
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")
            
        # Take screenshot with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Screenshots/screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename
    except Exception as e:
        return str(e)

def start_screen_recording():
    try:
        import cv2
        import numpy as np
        
        # Create Recordings directory if it doesn't exist
        if not os.path.exists("Recordings"):
            os.makedirs("Recordings")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Recordings/recording_{timestamp}.avi"
        
        # Initialize video writer
        screen_size = tuple(pyautogui.size())
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)
        
        return out, filename
    except Exception as e:
        return None, str(e)
