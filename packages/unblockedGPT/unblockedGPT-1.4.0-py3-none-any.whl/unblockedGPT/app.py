import streamlit as st
import requests
import openai
from unblockedGPT.rephrase import rephrase_2, rephrase_1
from unblockedGPT.auth import Database
from unblockedGPT.detection import ai_detection, ai_detection_2
from unblockedGPT.typeresponse import Typeinator
from unblockedGPT.saveResponse import saveResponse
from unblockedGPT.projectDataTypes import Conversation, FullConversation, AIScore, PageOptions
from unblockedGPT.GPTHeroAuth import gptHeroAuth
import time
import sys

# Decrypted API keys
auth = Database.get_instance()
openai_api_key = auth.get_settings(0)
stealthgpt_api_key = auth.get_settings(3)
gptzero_api_key = auth.get_settings(1)


#get args from command line
savePath = sys.argv[1]
#check if auth input already exists
opneai = st.text_input('OpenAI API Key', type="password")
gptzero = st.text_input('gptZero API Key (unnecessary)', type="password")
originality = st.text_input('Originality API Key (not necessary but can be helpful)', type="password")
stealthgpt = st.text_input('StealthGPT API Key (unnecessary)', key="stealthinput", type="password")
if st.button('Save Keys'):
    if opneai:
        auth.set_settings(0, opneai)
    if gptzero:
        auth.set_settings(1, gptzero)
    if originality:
        auth.set_settings(2, originality)
    if stealthgpt:
        auth.set_settings(3, stealthgpt)
    st.write("Saved")

if st.button("GPT Hero Auth"):
    gptHeroAuth()

if 'pageOptions' not in st.session_state:
    st.session_state.pageOptions = PageOptions()

if auth.get_settings(0) != False:
    st.session_state.pageOptions.openaiSet = True
else:
    st.write("Please enter OpenAI API Key")
if auth.get_settings(3) != False:
    st.session_state.pageOptions.stealthgptSet = True


if 'submitFlag' not in st.session_state:
    st.session_state.submitFlag = False
if st.session_state.pageOptions.openaiSet:
    # Title
    st.title('Totally Not ChatGPT')

    # Model selection
    model_selection = st.selectbox('Select the model:', ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4', 'gpt-4-1106-preview'])

    if st.button('Clear Conversation'):
        st.session_state.conversation = FullConversation()

    # User input
    user_input = st.text_area('You: ', height=200)
    if 'conversation' not in st.session_state:
        st.session_state.conversation = FullConversation()

    # Submit button
    if st.button('Submit'):
        st.session_state.submitFlag = True

    if user_input and st.session_state.submitFlag:
        st.session_state.submitFlag = False
        if openai_api_key != False:
            openai.api_key = openai_api_key
            try: 
                response = openai.ChatCompletion.create(
                model=model_selection,
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]
            )
                chatbot_response = response['choices'][0]['message']['content'].strip()
                st.session_state.conversation.addResponse(user_input, chatbot_response, 1, AIScore(ai_detection( chatbot_response, auth), ai_detection_2( chatbot_response, auth)))
            except:
                st.write("Invalid API Key")
        else:
            st.write("Please enter an API Key")
            
    # Rephrase button
    if st.button('Rephrase Text'):
        flag = True
        if auth.get_settings(7) == False:
            st.write("Please authenticate with GPT Hero")
            #if not gptHeroAuth():
            #    st.write("Error authenticating with GPT Hero, make sure you have openAI key saved!")
            #    flag = False
        if flag:
            response =  rephrase_2(st.session_state.conversation.getConversation()[0].response)
            if response['status']:
                aiscore = AIScore(ai_detection( response['msg'], auth), ai_detection_2( response['msg'], auth))
            else:
                aiscore = AIScore("N/A", "N/A")
            st.session_state.conversation.addResponse('Rephrase Text 2', response['msg'], 0, aiscore)
    if st.session_state.pageOptions.stealthgptSet: 
        # Rephrase button 2
        if st.button('Rephrase Text 2'):
            if stealthgpt_api_key != False:
                respones = rephrase_1(st.session_state.conversation.getConversation()[0].response)
                if response['status']:
                    aiscore = AIScore(ai_detection( response['msg'], auth), ai_detection_2( response['msg'], auth))
                else:
                    aiscore = AIScore("N/A", "N/A")
                st.session_state.conversation.addResponse('Rephrase Text 2', response['msg'], 0, aiscore)
            else:
                st.write("Please enter stealth API Key")

    # Type response
    if st.button('Type Response'):
        #type the most recent, using keyboard inputs
        typeinator = Typeinator()
        time.sleep(5)
        typeinator.type(st.session_state.conversation.getConversation()[0].response)

    st.write('Timed Typing')
    minutes = st.number_input('Minutes to type response', min_value=0, max_value=1000, step=1)
    if st.button('Timed Type Response') and minutes != 0:
        #type the most recent, using timed typing
        st.write('Typing in 5 seconds...')
        time.sleep(5)
        typeinator = Typeinator()
        typeinator.timeToType(st.session_state.conversation.getConversation()[0].response, minutes)
        minutes = 0

    # Display conversation and rephrases
    st.write(f'<div style="text-align: right; color: blue;">AI Detection Score: {st.session_state.conversation.getScore(1)}</div>', unsafe_allow_html=True )
    st.write(f'<div style="text-align: right; color: blue;">AI Detection Score 2: {st.session_state.conversation.getScore(2)}</div>', unsafe_allow_html=True)
    st.write("### Conversation:")
    conversation = st.session_state.conversation.getConversation()
    for turn in conversation:
        if turn.type == 1: 
            st.write(f'<div style="color: blue; background-color:{ "#E6EFFF" if turn.type == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>You:</b> {turn.prompt}</div>', unsafe_allow_html=True)
        st.write(f'<div style="color: black; background-color:{ "#DCDCDC " if turn.type == 1 else "#DFFFDF"}; padding: 10px; border-radius: 12px; margin: 5px;"><b>{"ChatGPT: " if turn.type == 1 else "Rephrase: "}</b> {turn.response} <br/> <div style="text-align: right; color: blue;">AI Detection Score: {turn.aiScore.score}<br>AI Detection Score 2:{turn.aiScore.score2}</div> </div>', unsafe_allow_html=True)
        if turn == conversation[0]:
            save = st.button('Save Response', key=turn.key)
            if save:
                if saveResponse(turn.response, savePath):
                    st.write("Saved")
                else:
                    st.write("Error saving")
