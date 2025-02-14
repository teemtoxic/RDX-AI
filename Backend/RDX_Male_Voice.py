import requests
import playsound
import os
import random
from typing import Union

def generate_audio(message: str, voice: str = "Brian"):
    """
    Text to speech using StreamElements API

    Parameters:
        message (str): The text to convert to speech
        voice (str): The voice to use for speech synthesis. Default is "Brian".

    Returns:
        result (Union[str, None]): Temporary file path or None in failure
    """
    # Base URL for provider API
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"

    # Request headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    # Try to send request or return None on failure
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None


def RDX_Male_Voice(message: str, voice: str = "Brian", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    """
    Enhanced TTS with text length management

    Args:
        result_content (bytes): The content to be saved and played.
        folder (str): The folder to save the file in. Default is "Voice Audio/". 
        extension (str): The extension of the file. Default is ".mp3".

    Returns:
        None, String
    """
    
    # List of responses for long text
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        # ...more responses can be added here
    ]

    try:
        # Split text into sentences
        sentences = str(message).split(".")
        
        # Check if text is too long
        if len(sentences) > 4 and len(message) > 250:
            # Take first two sentences and add notification
            limited_text = ". ".join(sentences[0:2]) + ". " + random.choice(responses)
            result_content = generate_audio(limited_text, voice)
        else:
            result_content = generate_audio(message, voice)

        if result_content is None:
            return "Failed to generate audio"

        # Handle file operations
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        
        # Play audio and cleanup
        playsound.playsound(file_path)
        os.remove(file_path)
        return None
        
    except Exception as e:
        return f"Error playing TTS: {str(e)}"
