import cohere
from rich import print
from dotenv import dotenv_values
import re

env_vars = dotenv_values(".env")

cohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=cohereAPIKey)


funcs = [
"exit", "general", "realtime", "open", "close", "play",
"generate image", "system", "content", "google search",
"youtube search","uninstall","install","note",
"organize","window"
]

messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
-> Respond with 'install (software name)' if a query is asking to install any software like 'install chrome', 'install notepad', etc. but if the query is asking to install multiple software, respond with 'install 1st software, install 2nd software' and so on.
-> Respond with 'organize (directory name)' if a query is asking to organize a directory like 'organize desktop', 'organize documents', etc. but if the query is asking to organize multiple directories, respond with 'organize 1st directory, organize 2nd directory' and so on.
-> Respond with 'uninstall (software name)' if a query is asking to uninstall any software like 'uninstall chrome', 'uninstall notepad', etc. but if the query is asking to uninstall multiple software, respond with 'uninstall 1st software, uninstall 2nd software' and so on.
-> Respond with 'window (task name)' if a query is asking to change the window like 'window minimize', 'window maximize', etc. but if the query is asking to change multiple windows, respond with 'window 1st task, window 2nd task', etc.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
*** Hindi Support ***
- For Hindi/English mix queries:
  "rdx instagram aur facebook kholo" → "open instagram open facebook"
  "rdx chrome band karo" → "close chrome"
  "rdx whatsapp aur telegram install karo" → "install whatsapp install telegram"
"""

ChatHistory = [
    {"role": "User", "message": "hello"},
    {"role": "user", "message": "general hello"},
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "uninstall whatsapp"},
    {"role": "Chatbot", "message": "uninstall whatsapp"},
    {"role": "User", "message": "Rdx chrome uninstall karo"},
    {"role": "Chatbot", "message": "uninstall chrome"},
    {"role": "User", "message": "rdx remove vs code"},
    {"role": "Chatbot", "message": "uninstall vs code"},
    {"role": "User", "message": "rdx uninstall vs code and install whatsapp"},
    {"role": "Chatbot", "message": "uninstall vs code install whatsapp"},
    {"role": "User", "message": "rdx uninstall vs code install whatsapp and uninstall chrome"},
    {"role": "Chatbot", "message": "uninstall vs code install whatsapp, uninstall chrome"},
    {"role": "User", "message": "install discord rdx"},
    {"role": "Chatbot", "message": "install discord"},
    {"role": "User", "message": "install facebok and whatsapp"},
    {"role": "Chatbot", "message": "install facebook install whatsapp"},
    {"role": "User", "message": "uninstall github and vs code"},
    {"role": "Chatbot", "message": "uninstall github uninstall vs code"},
    {"role": "User", "message": "install chrome and what is the time and open chrome"},
    {"role": "Chatbot", "message": "install chrome general what is the time, open chrome"},
    {"role": "User", "message": "write an application for a job"},
    {"role": "Chatbot", "message": "content application for a job"},
    {"role": "User", "message": "write a letter to my friend"},
    {"role": "Chatbot", "message": "content letter to my friend"},
    {"role": "User", "message": "minimaize this window"},
    {"role": "Chatbot", "message": "window minimize"},
    {"role": "User", "message": "remember me i have to go for a meeting"},
    {"role": "Chatbot", "message": "note i have to go for a meeting"},
    {"role": "User", "message": "note i am a good boy"},
    {"role": "Chatbot", "message": "note i am a good boy"},
    {"role": "User", "message": "download folder arrange karo"},
    {"role": "Chatbot", "message": "organize downloads"},
    {"role": "User", "message": "optimize desktop folder"},
    {"role": "Chatbot", "message": "organize desktop folder"},
    {"role": "User", "message": "rdx wifi off karo"},
    {"role": "Chatbot", "message": "system wifi off"},
    {"role": "User", "message": "set brightness to 50"},
    {"role": "Chatbot", "message": "system set brightness 50"},
    {"role": "User", "message": "rdx instagram aur facebook kholo"},
    {"role": "Chatbot", "message": "open instagram open facebook"},
    {"role": "User", "message": "chrome aur whatsapp band karo"},
    {"role": "Chatbot", "message": "close chrome close whatsapp"},
    {"role": "User", "message": "rdx spotify aur youtube chalao"},
    {"role": "Chatbot", "message": "open spotify open youtube"},
]


def FirstLayerDMM(prompt: str = "test"):
# Add the user's query to the messages list.
    messages.append( {"role": "user", "content": f"{prompt}"})

# Create a streaming chat session with the Cohere model.
    stream = co.chat_stream(
       model='command-r-plus', # Specify the Cohere model to use.
       message=prompt, # Pass the user's query.
       temperature=0.7, # Set the creativity level of the model.
       chat_history=ChatHistory, # Provide the predefined chat history for context.
       prompt_truncation='OFF', # Ensure the prompt is not truncated.
       connectors=[], # No additional connectors are used.
       preamble=preamble # Pass the detailed instruction preamble.
     )

    # Initialize an empty string to store the generated response.
    response = ""

   # Iterate over events in the stream and capture text generation events.
    for event in stream:
        if event.event_type == "text-generation":
           response += event.text # Append generated text to the response.

          # Modified response processing
    response = response.replace("\n", "")
    
    # Modified command splitting logic
    response = re.split(r'(open |close |play |generate image |system |install |uninstall |note |organize |window |reminder |content |google search |youtube search )', response)
    
    # Recombine commands with their verbs
    processed = []
    current_command = ""
    for part in response:
        if part.strip() in funcs:
            if current_command:
                processed.append(current_command.strip())
            current_command = part
        else:
            current_command += part
    if current_command:
        processed.append(current_command.strip())

    # Special handling for open commands
    final_commands = []
    for cmd in processed:
        while any(cmd.startswith(f"{verb} ") for verb in funcs):
            # Find the first matching verb
            for verb in funcs:
                if cmd.startswith(f"{verb} "):
                    # Split at the end of the verb
                    remaining = cmd[len(verb)+1:]
                    final_commands.append(f"{verb} {remaining.split(' ', 1)[0]}")
                    cmd = remaining.split(' ', 1)[1] if ' ' in remaining else ''
                    break
            else:
                break

    # Rest of filtering logic
    response = [cmd for cmd in final_commands if any(cmd.startswith(f) for f in funcs)]

# Initialize an empty list to filter valid tasks.
    temp = []

    for task in response:
      for func in funcs:
          if task.startswith(func):
              temp.append(task)
              break  # Prevent multiple matches

# Add valid tasks to the filtered list.

# Update the response with the filtered list of tasks.
    response = temp

# If '(query)' is in the response, recursively call the function for further clarification.
    if "(query)" in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse # Return the clarified response.
    else:
        return response # Return the filtered response.

#Entry point for the script.
def RDX_Brain():
    while True:
        try:
            # Get user input
            user_input = input("\nEnter query (or 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                break
                
            # Process query
            result = FirstLayerDMM(user_input)
            print(f"Classification: {result}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    RDX_Brain()