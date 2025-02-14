import random

responces_for_google_search = [
    "sir , i have found some results for you. look at this",
    "here are some search results for you, sir",
    "the rearch results are here, sir",
    "the resluts on your screen sir",
    "sir, I have found some information related to your query. Please have a look.",
    "here are the search results you requested, sir",
    "I've fetched the results for you, sir. Check them out.",
    "your search results are displayed on the screen, sir",
   "sir, the results of your search are right in front of you.",
   "I've got the search results for you, sir. Take a look.",
   "sir, I have retrieved some relevant information for you. See below.",
   "here are the results to your search query, sir",
   "sir, I've compiled some search results just for you.",
   "your search results are ready, sir. Please review them.",
   "I've pulled up the search results, sir. Have a glance.",
   "sir, here are the findings related to your search. Check it out."
]

responces_for_youtube_search = [
    "sir, I have found this on YouTube for you.",
    "here are some YouTube videos related to your search, sir.",
    "I've fetched some YouTube results just for you, sir.",
    "your YouTube search results are ready, sir. Please take a look.",
    "sir, I've compiled some YouTube videos based on your query.",
    "I've pulled up the YouTube search results, sir. Have a glance.",
    "sir, here are the YouTube videos related to your search. Check them out.",
    "the YouTube search results are here, sir",
    "sir, I have retrieved some relevant YouTube content for you. See below.",
    "I've got the YouTube search results for you, sir. Take a look.",
    "your search results on YouTube are displayed on the screen, sir",
    "sir, the results of your YouTube search are right in front of you.",
    "I've fetched the YouTube results for you, sir. Check them out.",
    "sir, I have found some interesting YouTube videos for you. Have a look.",
    "here are the YouTube results to your search query, sir"
]

software_installation_link = {
    "whatsapp": {
        "name": "WhatsApp",
        "type": "store",
        "url": "https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi",
        "store_id": "9NKSQGP7F2NH"
    },
    "chrome": {
        "name": "Google Chrome",
        "type": "web",
        "url": "https://www.google.com/chrome/",
        "exe_name": "ChromeSetup.exe"
    },
    "vscode": {
        "name": "Visual Studio Code",
        "type": "web",
        "url": "https://code.visualstudio.com/download",
        "exe_name": "VSCodeSetup.exe"
    },
    "windsurf":{
        "name": "Windsurf",
        "type": "web",
        "url": "https://windsurf-stable.codeiumdata.com/win32-x64-user/stable/599ce698a84d43160da884347f22f6b77d0c8415/WindsurfUserSetup-x64-1.1.2.exe",
        "exe_name": "WindsurfUserSetup-x64-1.1.2.exe"
    }
}

software_management_responses = {
    "install": [
        "Installing {} on your system, sir.",
        "I'll start the installation of {}, sir.",
        "Beginning to install {}, sir.",
        "Setting up {} for you, sir."
    ],
    "uninstall": [
        "Removing {} from your system, sir.",
        "I'll uninstall {} for you, sir.",
        "Starting the removal of {}, sir.",
        "Uninstalling {} as requested, sir."
    ],
    "already_installed": [
        "{} is already installed on your system, sir.",
        "Sir, {} is already present on your computer.",
        "I found that {} is already installed, sir."
    ],
    "not_found": [
        "Sorry sir, {} was not found on your system.",
        "I couldn't locate {} on your computer, sir.",
        "Sir, {} doesn't appear to be installed."
    ],
    "processing": [
        "Processing your request for {}, sir.",
        "Working on {} operation, sir.",
        "Executing your command for {}, sir."
    ],
    "invalid_command": [
        "I'm not sure what you want me to do with {}, sir.",
        "Could you please rephrase your command for {}, sir?",
        "I didn't understand the operation for {}, sir."
    ]
}

responces_for_task_completion = [
    "Task completed successfully, sir.",
    "All done, sir. Is there anything else you need?",
    "I've completed that task for you, sir.",
    "Mission accomplished, sir.",
    "Task executed successfully, sir.",
    "That's been taken care of, sir.",
    "Consider it done, sir.",
    "I've handled that for you, sir.",
    "Task finished as requested, sir.",
    "Operation completed successfully, sir.",
    "I've completed your request, sir.",
    "Done and dusted, sir.",
    "Task has been completed to your specifications, sir.",
    "All finished with that task, sir.",
    "Successfully completed as per your request, sir."
]

command_variations = {
    "install": [
        "install", "setup", "download", "get", "add",
        "install karo", "setup kardo", "download karo",
    ],
    "uninstall": [
        "uninstall", "remove", "delete", "hata do", "nikaal do",
        "system se remove", "uninstall karo", "hata do",
    ],
    "open": [
        "open", "launch", "start", "run", "kholo",
        "start karo", "launch karo", "khol do",
    ],
    "close": [
        "close", "end", "band", "stop", "band karo",
        "close karo", "stop karo", "band kar do",
    ]
}

suggestion_responses = {
    "activity": [
        "Sir, I notice you usually {} {} at this time.",
        "Would you like to {} {}, sir? You often do this now.",
        "Sir, shall I {} {} for you? You frequently use it at this hour.",
        "Based on your habits sir, would you like to {} {}?",
    ]
}

# Automation operation lists
AUTOMATION_OPERATIONS = {
    'open': ['open', 'launch', 'start', 'run'],
    'close': ['close', 'exit', 'quit', 'terminate'],
    'play': ['play', 'stream', 'watch'],
    'system': ['system report', 'mute', 'unmute', 'volume up', 'volume down'],
    'theme': ['dark mode', 'light mode'],
    'software': ['install', 'uninstall'],
    'media': ['take screenshot', 'start recording'],
    'files': ['optimize', 'organize'],
    'window': ['minimize', 'maximize', 'snap left', 'snap right', 'switch window', 'close window', 'show desktop'],
    'note': ['note', 'create note', 'take note'],
    'search': ['search in google', 'search on google', 'search in youtube', 'search on youtube'],
    'chrome': ['chrome incognito', 'chrome new tab', 'chrome history', 'chrome bookmark']
}

def is_automation_command(command: str) -> bool:
    """Check if a command is an automation command"""
    command = command.lower().strip()
    
    # Check each operation type and its variations
    for operation_type, variations in AUTOMATION_OPERATIONS.items():
        if any(variation in command for variation in variations):
            return True
    return False

def get_operation_type(command: str) -> str:
    """Get the type of automation operation from a command"""
    command = command.lower().strip()
    
    for operation_type, variations in AUTOMATION_OPERATIONS.items():
        if any(variation in command for variation in variations):
            return operation_type
    return "unknown"

def get_random_google_response():
    return random.choice(responces_for_google_search)

def get_random_youtube_response():
    return random.choice(responces_for_youtube_search)

def get_random_completion_response():
    return random.choice(responces_for_task_completion)

def get_software_response(response_type, software_name):
    """Get a random response for software management actions"""
    import random
    responses = software_management_responses.get(response_type, [])
    if responses:
        return random.choice(responses).format(software_name)
    return f"Processing {software_name}..."

def get_suggestion_response(action_type, target):
    """Get a random suggestion response"""
    template = random.choice(suggestion_responses["activity"])
    return template.format(action_type, target)