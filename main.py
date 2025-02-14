from Backend.Model import FirstLayerDMM
from Backend.RealTimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import threading
import json
import os
from Backend.update import main as check_updates



# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

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

def GenerateImage(prompt):
    # Placeholder function for image generation
    print(f"Generating image for prompt: {prompt}")
    # Add actual image generation logic here
    return "Image generated successfully."

def MainExecution():
    TaskExecution = False
    print(f"\n{Assistantname} is listening...")
    Query = SpeechRecognition()
    # Query = input(">> ") #SpeechRecognition()
    print(f"\n{Username}: {Query}")
    
    print("\nProcessing...")
    Decision = FirstLayerDMM(Query)
    print(f"Decision: {Decision}\n")

    # Process automation commands
    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    # Handle chat responses
    for Queries in Decision:
        if "general" in Queries:
            QueryFinal = Queries.replace("general ", "")
            Answer = ChatBot(QueryModifier(QueryFinal))
            print(f"{Assistantname}: {Answer}")
            TextToSpeech(Answer)
            return True
            
        elif "realtime" in Queries:
            QueryFinal = Queries.replace("realtime ", "")
            Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
            print(f"{Assistantname}: {Answer}")
            TextToSpeech(Answer)
            return True

        elif "generate image" in Queries:
            QueryFinal = Queries.replace("generate image ", "")
            Answer = GenerateImage(QueryModifier(QueryFinal))
            print(f"{Assistantname}: {Answer}")
            TextToSpeech(Answer)
            return True

        elif "exit" in Queries:
            Answer = "Goodbye!"
            print(f"{Assistantname}: {Answer}")
            TextToSpeech(Answer)
            os._exit(0)

def Main():
    check_updates()
    while True:
        MainExecution()

if __name__ == "__main__":
    Main()
