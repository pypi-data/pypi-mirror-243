import requests
from unblockedGPT.auth import Database
from unblockedGPT.GPTHeroAuth import gptHeroAuthLogin
# Define the base URL of your FastAPI-based API
#stealthGPT 
def rephrase_1(essay: str) -> dict:
    """
        This function rephrases the result using the 1st rephasing API.
        returns a dictionary with status bool and msg str
        input: text
        output: dictionary with status bool and msg str
    """
    auth = Database.get_instance()
    if auth.get_settings(3) == False:
        return {'status':False, 'msg':"check that your StealthGPT API key is set in the app."}

    headers = {'api-token': auth.get_settings(3), 'Content-Type': 'application/json'}
    data = {'prompt': essay, 'rephrase': True}
    try:
        r = requests.post('https://stealthgpt.ai/api/stealthify', headers=headers, json=data)
    except:
        return {'status':False, 'msg':"Error connecting to StealthGPT, Use VPN and Retry"}
    if r.status_code == 200:
        rephrased_text = r.json()
        rephrased_text = rephrased_text['result']
        return {'status':True, 'msg':rephrased_text}
    elif r.status_code == 401:
        return {'status':False, 'msg':"Invalid API Key"}
    else:
        return {'status':False, 'msg':"Could not rephrase. Try again later"}

def rephrase_2(essay: str) -> dict:
    """
        This function rephrases the result using the 2nd rephasing API.
        returns a dictionary with status bool and msg str
    """
    base_url = "https://gpthero.dev/api/"

    # Define the request payload
    auth = Database.get_instance()
    hero = auth.get_settings(7)
    if hero == False:
        return {'status':False, 'msg':"check that your chat GPT API key is set in the app."}
    request_payload = {
        "prompt": {
            "essay": essay,
            "approach": "Creative",
            "context": True,
            "randomness": 6,
            "tone": "informative",
            "difficulty": "easy to understand, very common vocabulary",
            "additional_adjectives": "concise and precise, to the point",
            "model": "GPT-3",
        },
        "user": {
            "auth_token": hero
        },
    }

    # Send a POST request to the /rephrase_essay endpoint
    try:
        response = requests.post(f"{base_url}/rephrase_essay", json=request_payload)
    except:
        return {'status':False, 'msg':"Error connecting to GPT Hero, Use VPN and Retry"}

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        rephrased_essay = response.json()
        rephrased_essay = rephrased_essay['rephrased_essay']
        return {'status':True, 'msg':rephrased_essay}
    elif response.status_code == 401:
        # Invalid API key
        return {'status':False, 'msg':"Invalid API key"}
        
    else:
        # Request failed
        error_message = response.json()

        return {'status':False, 'msg':f"Failed to rephrase essay\n {error_message['detail'][0]['msg']}"}

if __name__ == "__main__":
    essay = "Tz."
    print(rephrase_2(essay))
