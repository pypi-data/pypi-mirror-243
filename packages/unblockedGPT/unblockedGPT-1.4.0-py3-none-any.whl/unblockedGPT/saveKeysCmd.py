from unblockedGPT.auth import Database
from unblockedGPT.GPTHeroAuth import gptHeroAuth
import base64

def saveKeysCmd():
    auth = Database.get_instance()
    savedKeys = []
    print("This command is used to save your api keys. Only the openAI API key is required. ctrl+c to exit")
    openAIKey = input("OpenAI API Key(required): ")
    
    if openAIKey == "":
        print("OpenAI API Key is required")
        return
    savedKeys.append('OpenAI API Key saved')
    auth.set_settings(0, openAIKey)
    gptZeroKey = input("gptZero API Key (optional, leave blank to skip): ")
    if gptZeroKey != "":
        auth.set_settings(1, gptZeroKey)
        savedKeys.append('StealthGPT API Key saved')

    originalGPTKey = input("OriginalGPT API Key (optional but recommended, leave blank to skip): ")
    if originalGPTKey != "":
        auth.set_settings(2, originalGPTKey)
        savedKeys.append('OriginalGPT API Key saved')
    stealthGPTKey = input("StealthGPT API Key (optional, leave blank to skip): ")
    if stealthGPTKey != "":
        auth.set_settings(3, stealthGPTKey)
        savedKeys.append('StealthGPT API Key saved')
    
    if gptHeroAuth():
        savedKeys.append('GPTHero API Key Created')
    
    for key in savedKeys:
        print(key)

def saveKeys64Cmd():
    auth = Database.get_instance()
    savedKeys = []
    print("This command is used to save your api keys. Only the openAI API key is required. ctrl+c to exit")
    openAIKey = input("OpenAI API Key(required): ")
    
    if openAIKey == "":
        print("OpenAI API Key is required")
        return
    #decode key
    openAIKey = base64.b64decode(openAIKey).decode('utf-8')
    savedKeys.append('OpenAI API Key saved')
    auth.set_settings(0, openAIKey)
    gptZeroKey = input("gptZero API Key (optional, leave blank to skip): ")
    if gptZeroKey != "":
        gptZeroKey = base64.b64decode(gptZeroKey).decode('utf-8')
        auth.set_settings(1, gptZeroKey)
        savedKeys.append('StealthGPT API Key saved')
    
    originalGPTKey = input("OriginalGPT API Key (optional but recommended, leave blank to skip): ")
    if originalGPTKey != "":
        originalGPTKey = base64.b64decode(originalGPTKey).decode('utf-8')
        auth.set_settings(2, originalGPTKey)
        savedKeys.append('OriginalGPT API Key saved')
    stealthGPTKey = input("StealthGPT API Key (optional, leave blank to skip): ")
    if stealthGPTKey != "":
        stealthGPTKey = base64.b64decode(stealthGPTKey).decode('utf-8')
        auth.set_settings(3, stealthGPTKey)
        savedKeys.append('StealthGPT API Key saved')
    
    if gptHeroAuth():
        savedKeys.append('GPTHero API Key Created')
    
    for key in savedKeys:
        print(key)
    
        
    
    

