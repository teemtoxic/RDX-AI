import datetime # Importing the datetime module for real-time date and time information.
from dotenv import dotenv_values # Importing dotenv_values to read environment variables from a .env file.
from groq import Groq
from json import dump, load
# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

try:
   with open(r"Data\ChatLog.json", "r") as f:
       messages = load(f) # Load existing messages from the chat log.
except FileNotFoundError:
# If the file doesn't exist, create an empty JSON file to store chat logs.
    with open(r"Data\ChatLog.json", "w") as f:
       dump([], f)


def RealtimeInformation():
    current_date_time = datetime.datetime.now() # Get the current date and time.
    day = current_date_time. strftime("%A") # Day of the week.
    date = current_date_time. strftime("%d") # Day of the month.
    month = current_date_time. strftime("%B") # Full month name.
    year = current_date_time. strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time. strftime( "%S")

# Format the information into a string.
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes :{second} seconds .\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n') # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()] # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines) # Join the cleaned lines back together.
    return modified_answer

def ChatBot(Query):
   """This Function sennds the user's query to Chatbot and returns the AI's Response."""
   try:
       with open(r"Data\ChatLog.json", "r") as f:
          messages = load(f)

# Append the user's query to the messages list.
       messages.append( {"role": "user", "content": f"{Query}"})

# Make a request to the Groq API
       # Make a request to the Groq API for a response.
       completion = client.chat.completions.create(
          model="llama3-70b-8192", # Specify the AI model to use.
          messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation( ) } ] + messages,
          max_tokens=1024, # Limit the maximum tokens in the response.
          temperature=0.7, # Adjust response randomness (higher means more random).
          top_p=1, # Use nucleus sampling to control diversity.
          stream=True,
          stop=None
       )
       Answer = ""

       for chunk in completion:
          if chunk. choices[0].delta.content: # Check if there's content in the current chunk.
              Answer += chunk. choices[0].delta.content # Append the content to the answer.

       Answer = Answer.replace("</s>", "") # Clean up any unwanted tokens from the response.

# Append the chatbot's response to the messages list.
       messages.append( {"role": "assistant", "content": Answer})

# Save the updated chat log to the JSON file.
       with open(r"Data\ChatLog.json", "w") as f:
           dump(messages, f, indent=4)

# Return the formatted response.
       return AnswerModifier(Answer=Answer)

   except Exception as e:
# Handle errors by printing the exception and resetting the chat log.
      print(f"Error: {e}")
      with open(r"Data\ChatLog.json", "w") as f:
          dump([], f, indent=4)
      return ChatBot(Query)



if __name__ == "__main__":
    while True:
       user_input = input("Enter Your Question: ")
       print(ChatBot(user_input))