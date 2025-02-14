from AppOpener import close, open as appopen # Import functions to open and close apps.
from webbrowser import open as webopen # Import web browser functionality.
from pywhatkit import search, playonyt # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content.
from rich import print # Import rich for styled console output.
from groq import Groq # Import Groq for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests # Import requests for making HTTP requests.
import keyboard # Import keyword to check for Python keywords.
import asyncio # Import asyncio for asynchronous operations.
import os # Import os for file path handling.
from PIL import Image
from time import sleep
from random import randint
import ctypes
import time

# Fix imports - change from relative to absolute
from Backend.system_theme import WindowsThemeManager
from Backend.system_shortcuts import SystemShortcuts
from Backend.system_monitor import check_system_resources
from Backend.software_installer import download_and_install_software
from Backend.software_uninstaller import uninstall_software
from Backend.quick_notes import NotesManager
from Backend.file_manager import FileManager
from Backend.system_control import SystemControl

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
HF_API_KEY = env_vars.get("HuggingFaceAPIKey")

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKDO sY7ric", "ZØLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
            "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTMI, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
"Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
"I'm at your service for any additional questions or support you may need don't hesitate to ask.",
]
# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters"}]

# Initialize new system managers
theme_manager = WindowsThemeManager()
shortcuts = SystemShortcuts()
notes_manager = NotesManager()
file_manager = FileManager()
system_control = SystemControl()

# Constants
WEB_APPS = {
    # Social Media
    'instagram': 'https://www.instagram.com/',
    'facebook': 'https://www.facebook.com/',
    'twitter': 'https://x.com/',
    'linkedin': 'https://www.linkedin.com/',
    'whatsapp': 'https://web.whatsapp.com/',
    'telegram': 'https://web.telegram.org/',
    'discord': 'https://discord.com/',
    'reddit': 'https://www.reddit.com/',
    'pinterest': 'https://www.pinterest.com/',
    
    # Shopping
    'amazon': 'https://www.amazon.com/',
    'flipkart': 'https://www.flipkart.com/',
    'myntra': 'https://www.myntra.com/',
    'meesho': 'https://www.meesho.com/',
    'ajio': 'https://www.ajio.com/',
    'snapdeal': 'https://www.snapdeal.com/',
    'nykaa': 'https://www.nykaa.com/',
    
    # Entertainment
    'netflix': 'https://www.netflix.com/',
    'primevideo': 'https://www.primevideo.com/',
    'hotstar': 'https://www.hotstar.com/',
    'spotify': 'https://open.spotify.com/',
    'youtube': 'https://www.youtube.com/',
    
    # Food Delivery
    'zomato': 'https://www.zomato.com/',
    'swiggy': 'https://www.swiggy.com/',
    
    # Travel
    'makemytrip': 'https://www.makemytrip.com/',
    'irctc': 'https://www.irctc.co.in/',
    'goibibo': 'https://www.goibibo.com/',
    
    # Education
    'udemy': 'https://www.udemy.com/',
    'coursera': 'https://www.coursera.org/',
    'edx': 'https://www.edx.org/',
    
    # Productivity
    'gmail': 'https://mail.google.com/',
    'drive': 'https://drive.google.com/',
    'github': 'https://github.com/',
    'notion': 'https://www.notion.so/'
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
GROQ_MODEL = "llama3-70b-8192"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Tndicate success.


# Function to generate content using AI and save it to a file.
def Content(Topic):
    Topic = Topic.replace("Content ", "").strip()
    
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": Topic}],
            temperature=0.7,
            max_tokens=2048,
            stream=True
        )
        
        content = "".join([
            chunk.choices[0].delta.content
            for chunk in response
            if chunk.choices[0].delta.content
        ])
        
        filename = f"Data/{Topic.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        subprocess.Popen(['notepad.exe', filename])
        return True
        
    except Exception as e:
        print(f"Content generation failed: {str(e)}")
        return False


def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True



# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True



def OpenApp(app_name: str, session=requests.Session()) -> bool:
    """
    Handles application opening with multiple fallback strategies
    Returns True if any method succeeds
    """
    # Try web app first
    if app_name.lower() in WEB_APPS:
        webbrowser.open(WEB_APPS[app_name.lower()])
        return True

    # Try different opening methods
    methods = [
        lambda: appopen(app_name, match_closest=True, throw_error=False),
        lambda: subprocess.Popen(app_name, shell=True),
        lambda: subprocess.run(['start', app_name], shell=True, check=True),
        lambda: os.startfile(app_name)
    ]

    for method in methods:
        try:
            method()
            return True
        except Exception as e:
            print(f"Failed to open {app_name} with {method.__name__}: {str(e)}")
            continue

    # Fallback to web search
    try:
        search_query = f"{app_name} official site"
        response = session.get(
            f"https://www.google.com/search?q={search_query}",
            headers={'User-Agent': USER_AGENT}
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        if main_link := soup.find('a', jsname='UWckNb'):
            webbrowser.open(main_link['href'])
            return True
    except Exception as e:
        print(f"Web search fallback failed: {str(e)}")

    return False

def CloseApp(app_name: str) -> bool:
    """Handles application closing with multiple strategies"""
    try:
        close(app_name, match_closest=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error closing {app_name}: {str(e)}")
        return False


def System(command: str):
    command = command.lower().strip()
    actions = {
        'mute': lambda: keyboard.press('volume mute'),
        'unmute': lambda: keyboard.press('volume mute'),
        'volume up': lambda: keyboard.press('volume up'),
        'volume down': lambda: keyboard.press('volume down'),
        'dark mode': lambda: theme_manager.set_theme(0),
        'light mode': lambda: theme_manager.set_theme(1),
        'lock': ctypes.windll.user32.LockWorkStation,
        'sleep': lambda: os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep"),
        'system report': check_system_resources,
        'wifi on': lambda: system_control.toggle_wifi(True),
        'wifi off': lambda: system_control.toggle_wifi(False)
    }
    
    if action := actions.get(command):
        try:
            result = action()
            return result if result is not None else True
        except Exception as e:
            print(f"System command failed: {str(e)}")
            return False
    return False


# Add new functions for software management and notes
def InstallSoftware(software_name):
    return download_and_install_software(software_name)

def UninstallSoftware(software_name):
    return uninstall_software(software_name)

def CreateNote(content, title=None):
    return notes_manager.create_note(content, title)

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        try:
            if command.startswith("open "):
                if "open it" in command or "open file" == command:
                    continue
                # Fix removeprefix syntax
                app_name = command.replace("open ", "", 1).strip()
                fun = asyncio.to_thread(OpenApp, app_name)
                funcs.append(fun)

            elif command.startswith("close "):
                app_name = command.replace("close ", "", 1).strip()
                fun = asyncio.to_thread(CloseApp, app_name)
                funcs.append(fun)

            elif command.startswith("google search "):
                query = command.replace("google search ", "", 1).strip()
                fun = asyncio.to_thread(GoogleSearch, query)
                funcs.append(fun)

            elif command.startswith("youtube search "):
                query = command.replace("youtube search ", "", 1).strip()
                fun = asyncio.to_thread(YouTubeSearch, query)
                funcs.append(fun)

            elif command.startswith("system "):
                action = command.replace("system ", "", 1).strip()
                fun = asyncio.to_thread(System, action)
                funcs.append(fun)
            elif command.startswith("play "):
                query = command.replace("play ", "", 1).strip()
                fun = asyncio.to_thread(PlayYoutube, query)
                funcs.append(fun)
            elif command.startswith("generate image "):
                prompt = command.replace("generate image ", "", 1).strip()
                fun = GenerateImages(prompt)
                funcs.append(fun)
            elif command.startswith("install "):
                software = command.replace("install ", "", 1).strip()
                fun = asyncio.to_thread(InstallSoftware, software)
                funcs.append(fun)

            elif command.startswith("uninstall "):
                software = command.replace("uninstall ", "", 1).strip()
                fun = asyncio.to_thread(UninstallSoftware, software)
                funcs.append(fun)

            elif command.startswith("note "):
                content = command.replace("note ", "", 1).strip()
                fun = asyncio.to_thread(CreateNote, content)
                funcs.append(fun)

            elif command.startswith("window "):
                action = command.replace("window ", "", 1).strip()
                fun = asyncio.to_thread(shortcuts.window_management, action)
                funcs.append(fun)
            elif command.startswith("Content "):
                action = command.replace("Content ", "", 1).strip()
                fun = asyncio.to_thread(Content, action)
                funcs.append(fun)
            else:
                print(f"No Function Found for {command}")

        except Exception as e:
            print(f"Error processing command '{command}': {e}")
            continue

    try:
        results = await asyncio.gather(*funcs)
        for result in results:
            yield result
    except Exception as e:
        print(f"Error executing commands: {e}")
        yield False

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass
    return True

# Add image generation API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {env_vars.get('HuggingFaceAPIKey')}"}

# Add image generation functions
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    #    print(f"Generating image for prompt: {prompt}")

    image_bytes_list = await asyncio.gather(*tasks)
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ','_')}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)
            print(f"Saved image {i+1} for prompt: {prompt}")

async def GenerateImages(prompt: str):
    await generate_images(prompt)
    print(f"Generated images for prompt: {prompt}")
    open_images(prompt)
    return True

# if __name__ == "__main__":
#     # Test social media opening
#     asyncio.run(Automation([
#         "open instagram",
#         "open twitter",
#         "open notepad",
#         "open calculator"
#     ]))

