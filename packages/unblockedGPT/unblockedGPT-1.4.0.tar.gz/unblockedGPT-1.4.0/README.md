# UnblockedGPT
A simple Streamlit chatbot that can be installed via pip.

# Installations
1. Ensure Python is Installed on Your Device: [https://www.python.org/downloads/](url)  
2. Ensure Pip is Installed on Your Device:  
To install pip, open terminal or command prompt (cmd) and enter these commands:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
```
python get-pip.py
```

# How to Run
In terminal or command prompt (cmd):  
```
pip install unblockedGPT
```
```
chat
```
Then enter API keys (only OpenAI API key is required, but others are recommended) button and press save keys button. No need to enter api keys again - they will be saved on your system and cannot be accessed by anyone else. 

# Commands
Chat Command:
- Starts a web app that is an interface for the chatbot. Go to the url that is printed in the terminal to access the web app. 
- Must set api keys in the web app for any GPT functionality to work.
- To run the chatbot, run the command `chat` in the terminal.

typetext Command:
- Command will write text from a text file with keyboard inputs. 
- typetext -p [path to text file/file in curent dir] (optional) -t [time in minutes to type the text] (optional)

typeGPT Command:
- Command to type a prompt into the GPT model and write the output to keyboard inputs.

saveHero
- Command to save the results from GPTHero to a text file.
- `saveHero -p [path to text file/file in curent dir]`

saveStealth
- Command to save the results from StealthGPT to a text file.
- `saveStealth -p [path to text file/file in curent dir]`

setKeys Command:
- Command to set api keys for the chatbot.
- Run the command `setKeys` and follow the instructions in the terminal.
- Use the `-b64` flag to enter base64 encoded api keys.

# API Keys
Note none of these can be taken from you because this runs locally on your computer. Some require subscriptions but OpenAI API key is required. Other ones are set by default or need your input. Copy and paste these links into browser.
- OpenAI: [https://platform.openai.com/account/api-keys](url)
- GPTHero API Key: Set automatically (no manual changes needed).
- StealthGPT API Key: get from [https://www.stealthgpt.ai/](url) (requires paid subscription)
- GPTZero: https://app.gptzero.me/app/api-subscription
- Originality: https://app.originality.ai/api-access
