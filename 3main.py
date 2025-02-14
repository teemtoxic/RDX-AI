import os
import sys
from time import sleep
import subprocess
from dotenv import dotenv_values
import asyncio
import pygame
from concurrent.futures import ThreadPoolExecutor

# Initialize pygame mixer once
pygame.mixer.init()

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

def check_and_run_offline_mode():
    try:
        from Offline.online_check import is_Online
        if not is_Online():
            print("No internet connection detected. Switching to offline mode...")
            offline_script = os.path.join(os.path.dirname(__file__), 'Offline', 'comain.py')
            subprocess.run([sys.executable, offline_script])
            sys.exit(0)
    except Exception as e:
        print("Internet connection error. Switching to offline mode...")
        offline_script = os.path.join(os.path.dirname(__file__), 'Offline', 'comain.py')
        subprocess.run([sys.executable, offline_script])
        sys.exit(0)

def load_online_dependencies():
    try:
        global FirstLayerDMM, RealtimeSearchEngine, Automation, ChatBot, TextToSpeech
        from Backend.Model import FirstLayerDMM
        from Backend.RealTimeSearchEngine import RealtimeSearchEngine
        from Backend.Automation import Automation
        from Backend.Chatbot import ChatBot
        from Backend.TextToSpeech import TextToSpeech
        return True
    except Exception as e:
        print(f"Failed to load online dependencies: {e}")
        return False

# Constants
Functions = [
    # File and App Control
    "open", "close", 
    
    # Media Control
    "play", "pause", "stop", "next", "previous",
    
    # System Operations
    "system", "shutdown", "restart", "sleep", "lock",
    
    # Volume Control
    "volume", "mute", "unmute",
    
    # Web Actions
    "google", "youtube", "search",
    
    # Screen Actions
    "screenshot", "screen record",
    
    # System Settings
    "brightness", "wifi", "bluetooth",
    
    # Clipboard Operations
    "copy", "paste", "select", "cut",
    
    # Window Management
    "minimize", "maximize", "switch window", "show desktop",
    
    # Image Generation
    "generate image",  # Add image generation to supported functions
    
    # System Management
    "dark mode", "light mode", "system report",
    "organize", "stats",
    
    # Software Management
    "install", "uninstall",
    
    # Notes
    "note",
    
    # Window Management
    "window minimize", "window maximize", "window switch",
    "window desktop",
    
    # File Organization
    "organize downloads", "organize documents", "organize desktop",
    "stats downloads", "stats documents", "stats desktop",
    
    # System Controls
    "wifi on", "wifi off",
    "bluetooth on", "bluetooth off",
    "brightness",
    "airplane mode on", "airplane mode off",
    "lock screen",
    "night light on", "night light off",
    
    # File System Controls
    "show extensions", "hide extensions",
    "show hidden", "hide hidden",
    
    # System Appearance
    "enable transparency", "disable transparency",
    
    # Gaming
    "enable game mode", "disable game mode",
    
    # Power Management
    "power balanced", "power saver", "power performance",
    
    # Desktop and Lock Screen
    "set wallpaper",
    "disable lock screen", "enable lock screen",
    
    # Power Management
    "enable hibernation", "disable hibernation",
    
    # Startup Management
    "add startup", "remove startup",
    
    # Windows Features
    "enable cortana", "disable cortana",
    "enable indexing", "disable indexing",
    
    # Mouse Settings
    "mouse speed", "mouse double click",
    
    # Taskbar Customization
    "taskbar small icons", "taskbar large icons",
    "taskbar combine always", "taskbar combine never",
]

def QueryModifier(Query):
    new_query = Query.lower().strip()
    if new_query[-1] not in ['.', '?', '!']:
        new_query += "."
    return new_query.capitalize()

async def MainExecution():
    TaskExecution = False
    print(f"\n{Assistantname} is listening...")
    
    try:
        Query = input(">> ")
        print(f"\n{Username}: {Query}")
        
        Decision = FirstLayerDMM(Query)
        
        # Process automation commands
        for queries in Decision:
            if not TaskExecution:
                if any(queries.startswith(func) for func in Functions):
                    async with asyncio.TaskGroup() as tg:
                        await tg.create_task(Automation(list(Decision)))
                    TaskExecution = True
                    break

        # Handle chat responses with thread pool
        with ThreadPoolExecutor() as pool:
            for Queries in Decision:
                if "general" in Queries:
                    QueryFinal = Queries.replace("general ", "")
                    Answer = await asyncio.to_thread(ChatBot, QueryModifier(QueryFinal))
                    print(f"{Assistantname}: {Answer}")
                    await asyncio.to_thread(TextToSpeech, Answer)
                    return True
                
                elif "realtime" in Queries:
                    QueryFinal = Queries.replace("realtime ", "")
                    Answer = await asyncio.to_thread(RealtimeSearchEngine, QueryModifier(QueryFinal))
                    print(f"{Assistantname}: {Answer}")
                    await asyncio.to_thread(TextToSpeech, Answer)
                    return True

                elif "exit" in Queries:
                    Answer = "Goodbye!"
                    print(f"{Assistantname}: {Answer}")
                    await asyncio.to_thread(TextToSpeech, Answer)
                    pygame.mixer.quit()
                    os._exit(0)
    
    except Exception as e:
        print(f"Error in MainExecution: {e}")
        return False

def main():
    print(f"Welcome to {Assistantname}!")
    print("Listening for commands...")
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        try:
            loop.run_until_complete(MainExecution())
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    loop.close()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()