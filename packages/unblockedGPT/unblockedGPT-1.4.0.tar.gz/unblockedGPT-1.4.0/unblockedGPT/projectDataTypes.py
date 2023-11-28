import streamlit as st


class AIScore:
    def __init__(self, score:str, score2:str) -> None:
        self.score = score
        self.score2 = score2

class Conversation:
    def __init__(self, prompt, response, type, key, aiScore:AIScore = AIScore("N/A", "N/A")) -> None:
        """
            class that represents a single propt-response pair
            input: None
            output: None
        """
        self.prompt = prompt
        self.response = response
        self.type = type
        self.key = key
        self.aiScore = aiScore

class FullConversation:
    def __init__(self):
        """
            class that represents a full conversation
            input: None
            output: None
        """
        self.conversation = []
        self.position = 0
        self.ai_detection_score = AIScore("N/A", "N/A")
    def addResponse(self, prompt:str, response:str, type:int, ai_detection:AIScore):
        """
            function that adds a response to the conversation
            input: prompt, response, type
            output: None
        """
        self.conversation.insert(0, Conversation(prompt, response, type, self.position, ai_detection))
        self.position += 1
        self.ai_detection_score = ai_detection
    def getConversation(self):
        """
            function that returns the conversation
            input: None
            output: conversation
        """
        return self.conversation
    def getScore(self, option:int = 0 ):
        """
            function that returns the most recent score
            input: None
            output: score
        """
        if option == 1:
            return self.ai_detection_score.score
        elif option == 2:
            return self.ai_detection_score.score2
        return self.ai_detection_score

class AuthValue():
    def __init__(self,  value:str,key:int, lable:str = "") -> None:
        """
            class that represents a single auth value
            input: key, value
            output: None
        """
        self.key = key
        self.value = value
        self.label = lable

class PageOptions():
    def __init__(self) -> None:
        """
            represents the page state
        """
        self.openaiSet = False
        self.stealthgptSet = False