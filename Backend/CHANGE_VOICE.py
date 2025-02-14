from Backend.RDX_Male_Voice import RDX_Male_Voice
from Backend.RDX_Girl_Voice import RDX_Female_Voice
import json
import os

class VoiceManager:
    def __init__(self):
        self.config_file = "voice_config.json"
        self.current_voice = self.load_voice_preference()
        self.male_voices = ["Brian", "Justin"]
        self.female_voices = ["Aditi", "Salli", "Joanna"]

    def load_voice_preference(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {"type": "male", "name": "Brian"}  # Default voice
        except:
            return {"type": "male", "name": "Brian"}  # Default if error

    def save_voice_preference(self, voice_type, voice_name):
        with open(self.config_file, 'w') as f:
            json.dump({"type": voice_type, "name": voice_name}, f)
        self.current_voice = {"type": voice_type, "name": voice_name}

    def speak(self, text: str) -> None:
        """
        Speak text using current default voice
        Args:
            text (str): Text to speak
        """
        try:
            voice_type = self.current_voice["type"]
            voice_name = self.current_voice["name"]

            if voice_type.lower() == "male":
                RDX_Male_Voice(text, voice_name)
            else:
                RDX_Female_Voice(text, voice_name)
        except Exception as e:
            print(f"Error in speak: {str(e)}")

    def change_voice(self, voice_type: str, voice_name: str = None) -> None:
        """
        Change default voice settings
        Args:
            voice_type (str): "male" or "female"
            voice_name (str): Specific voice name (optional)
        """
        try:
            if voice_type.lower() not in ["male", "female"]:
                raise ValueError("Invalid voice type. Use 'male' or 'female'")

            available_voices = self.male_voices if voice_type == "male" else self.female_voices
            
            if voice_name and voice_name not in available_voices:
                raise ValueError(f"Invalid voice name. Available voices: {', '.join(available_voices)}")

            default_voice = "Brian" if voice_type == "male" else "Aditi"
            voice_name = voice_name if voice_name else default_voice
            
            self.save_voice_preference(voice_type, voice_name)
            return f"Voice changed to {voice_type} - {voice_name}"
        except Exception as e:
            print(f"Error changing voice: {str(e)}")
            return None

# Initialize voice manager (singleton)
voice_manager = VoiceManager()

# Global speak function for easy access
def speak(text: str):
    voice_manager.speak(text)

def handle_voice_command(text: str):
    """
    Handle voice commands and text-to-speech
    Returns: None
    """
    if "change your voice" in text.lower():
        print("\nAvailable Voice Options:")
        print("1. Male Voice")
        print("2. Female Voice")
        
        try:
            choice = input("Choose voice type (1/2): ")
            if choice == "1":
                voice_manager.change_voice("male", "Brian")
                speak("Voice changed to male")
            elif choice == "2":
                voice_manager.change_voice("female", "Aditi")
                speak("Voice changed to female")
            else:
                print("Invalid choice. Using current voice.")
        except Exception as e:
            print(f"Error changing voice: {str(e)}")
    else:
        speak(text)

# # Example usage
# if __name__ == "__main__":
#     while True:
#         text = input("\nEnter text (or 'exit' to quit): ")
#         if text.lower() == 'exit':
#             break
#         handle_voice_command(text)

#handle_voice_command("change your voice")
