import pyautogui 

def chrome(text):
    commands = {
        "incognito": ('ctrl', 'shift', 'n'),
        "reload": ('ctrl', 'r'),
        "new tab": ('ctrl', 't'),
        "new window": ('ctrl', 'n'),
        "history": ('ctrl', 'h'),
        "bookmark": ('ctrl', 'd'),
        "download list": ('ctrl', 'j'),
        "delete history": ('ctrl', 'shift', 'del'),
        "switch tab": ('ctrl', 'tab'),
        "previous tab": ('ctrl', 'shift', 'tab'),
        "inspect": ('ctrl', 'shift', 'i'),
        "bookmark manager": ('ctrl', 'shift', 'o'),
        "chrome task manager": ('shift', 'esc'),
        "home page": ('alt', 'home'),
        "chrome menu": ('alt', 'f'),
        "print this page": ('ctrl', 'p'),
        "stop reloading": ('esc',),
        "search in chrome": ('ctrl', 'k')
    }
    
    for command, keys in commands.items():
        if command in text.lower():
            pyautogui.hotkey(*keys)
            return True
    return False
