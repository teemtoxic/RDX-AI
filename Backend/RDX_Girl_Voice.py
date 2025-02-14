import requests
import os
from playsound import playsound
from typing import Union
from os import getcwd
from urllib.parse import quote
import random

def generate_audio(message: str, voice: str = "Aditi"):
    # URL encode the message
    encoded_message = quote(message)
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={encoded_message}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        result = requests.get(url=url, headers=headers)
        if result.status_code == 200:
            return result.content
        return None
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def RDX_Female_Voice(message: str, voice: str = "Aditi", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    try:
        # Split text into sentences
        sentences = str(message).split(".")
        
        # Process text based on length
        if len(sentences) > 4 and len(message) > 250:
            limited_text = ". ".join(sentences[0:2]) + ". " + random.choice(responses)
            result_content = generate_audio(limited_text, voice)
        else:
            result_content = generate_audio(message, voice)

        if result_content is None:
            return "Failed to generate audio"
            
        # Create full file path
        file_path = os.path.join(getcwd(), f"{voice}{extension}")
        
        # Write and play audio
        with open(file_path, "wb") as file:
            file.write(result_content)
        
        # Play using playsound
        playsound(file_path)
        
        # Cleanup
        os.remove(file_path)
        return None
        
    except Exception as e:
        print(f"Error in speak function: {e}")
        return str(e)

if __name__ == "__main__":
    while True:
        text = input("\nEnter text to speak (or 'exit' to quit): ")
        if text.lower() == 'exit':
            break
        RDX_Female_Voice(text)
