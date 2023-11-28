import pyautogui
import random
import string
import sys
import time
import re
class Typeinator():
    def __init__(self):
        self.delay = 0.02
        self.punctuationPause = .75
        self.buletPointFlag = False
        #check if windows
        self.comandKey = ''
        if sys.platform == 'win32':
            self.comandKey = 'ctrl'
        #check if mac
        elif sys.platform == 'darwin':
            self.comandKey = 'command'
        else:
            self.comandKey = 'ctrl'
    def timeToType(self, text: str, timeIn:int) -> None:
        """
            function to type text given the minutes to type the str
            input: text to be typed, and minutes to type
            output: None
        """
        timeIn = timeIn * 60
        #split text into chunks at the end of a sentance
        textGroups = re.findall(r'(.+?[.!?])(?:\s+|$)', text)
        #join the chunks into chunks 2-6 sentances long
        toType = []
        while textGroups != []:
            rand = random.randint(2, 6)
            if len(textGroups) < rand:
                rand = len(textGroups)
            hold = textGroups[0:rand]
            #remove the chunks that are to be joined
            textGroups = textGroups[rand:]
            #join the chunks and add them to the toType list
            toType.append(' '.join(hold))
        

        for subtext in toType:
            if len(subtext) > 0:
                maxTime = len(subtext) * self.delay
                punctuationPauses = 0
                shortPunctuationPauses = 0
                #calculate the theorectical max time it would take to type the text
                #count the number of punctuation pauses
                for i in subtext:
                    if i == '.' or i == '!' or i == '?':
                        punctuationPauses += 1
                    elif i == ',' or i == ';':
                        shortPunctuationPauses += 1
                #add the punctuation pauses to the max time
                maxTime += punctuationPauses * 5
                maxTime += shortPunctuationPauses * 3.5
                #type the text and comapre the time it took to type it to the max time
                startTime = time.time()
                self.type(subtext)
                endTime = time.time()
                timeToType = endTime - startTime
                timeToMatch = timeIn / len(toType)
                if subtext != toType[-1]:
                    #if the time to type is less than the time to match, sleep for the difference
                    if timeToType < timeToMatch:
                        time.sleep(timeToMatch - timeToType)
                    else:
                        print("Took too long to type section. The text may take longer than the time provided.")
                

        #take a random amount of the begining text to type and track the time it takes to type it
        

    
    def type(self, text: str) -> None:
        """
            function to type text
            input: text to be typed
            output: None
        """
        if '.' not in text and '!' not in text and '?' not in text:
            text += '.'
        if '...' in text:
            text = text.replace('...', './DOTS/')
        sentances = text.split('.')
        for sentance in sentances:
            #add back punctuation
            #will bold whole sentace
            if sentance != sentances[-1]:
                sentance += '.'
            if '/I/' in sentance:
                pyautogui.hotkey(self.comandKey, 'i')
                sentance = sentance.replace('/I/', '')
            if '/B/' in sentance:
                pyautogui.hotkey(self.comandKey, 'b')
                sentance = sentance.replace('/B/', '')
            if '/U/' in sentance:
                pyautogui.hotkey(self.comandKey, 'u')
                sentance = sentance.replace('/U/', '')
            if '/T/' in sentance:
                sentance = sentance.replace('/T/', '\t')
            
            if '/+/' in sentance:
                split = sentance.split('/+/')
                self.writer(split[0] + '\n' )
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                self.writer(split[1] + '')
            elif '/-/' in sentance:
                split = sentance.split('/-/')
                self.writer(split[0])
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                self.writer(split[1] + '')
            
            
                
            else:
                
                if random.random() < 0.02:  # 2% chance of a typo
                    #chose a random word in the sentance
                    words = sentance.split(' ')
                    #randomly choose an index from words list
                    index = random.randint(0, len(words) - 1)
                    #type sentance up to the word
                    self.writer(' '.join(words[:index]))
                    #type the word with a typo
                    word = words[index]
                    typo_part = word + random.choice(string.ascii_lowercase)
                    self.writer(typo_part)

                    # 90% chance to recognize and fix the typo
                    if random.random() < 0.90:
                        time.sleep(self.punctuationPause)
                        # Delete the incorrect word
                        for _ in range(len(typo_part)):
                            pyautogui.press('backspace')
                            time.sleep(self.delay)
                        # Retype the word correctly
                        self.writer(word)
                        #type the rest of the sentance
                        self.writer(' '.join(words[index + 1:]))
                    else:
                        #type the rest of the sentance
                        self.writer(' '.join(words[index + 1:]))
                        time.sleep(self.punctuationPause)
                else:
                    self.writer(sentance)
      
    def writer(self, text:str):

        punctuationFlag = False
        punctuation = {
            'comma': {'val':False, 'char':',', 'pause': 1},
            'simicolon': {'val':False, 'char':';', 'pause': 2},
            'explination': {'val':False, 'char':'!', 'pause': 3},
            'question': {'val':False, 'char':'?', 'pause': 4},
            'pause': {'val':False, 'char':'/P/', 'pause': 5},
            'colon': {'val':False, 'char':':', 'pause': 6},
            'custom': {'val':False, 'char':',', 'pause': 7},
            'none': {'val':False, 'char':'', 'pause': 8},
        }
        pauseRef = [0]
        #random chance to not pause 25% of the time
        if random.random() < 0.25:
            pauseRef = [8]
        customPauses = []
        # 35% chance to pause for 2.5 seconds after a comma
        if ',' in text and random.random() < 0.65:
            punctuation['comma']['val'] = True
            punctuationFlag = True
        # 60% chance to pause for 2.5 seconds after a semicolon
        if ';' in text and random.random() < 0.6:
            punctuation['simicolon']['val'] = True
            punctuationFlag = True
        # Pause for 2.5 seconds after every period, exclamation mark, or question mark
        if '!' in text:
            punctuation['explination']['val'] = True
            punctuationFlag = True
        if '?' in text:
            punctuation['question']['val'] = True
            punctuationFlag = True
        if ':' in text:
            punctuation['colon']['val'] = True
            punctuationFlag = True
        if '/P/' in text:
            punctuation['pause']['val'] = True
            punctuationFlag = True
        pause_match = re.search(r'/(\d+)/', text)
        if pause_match:
            punctuation['custom']['val'] = True
            punctuationFlag = True
            customPauses = re.findall(r'/(\d+)/', text)
            
        #type the sentance and pause for any punctuation that is true
        if punctuationFlag:
            split = [text]

            #split sentance on commas if punctuation['comma'] is true, and replace the commas
            for key in punctuation:
                if punctuation[key]['val']:
                    for x in range(len(split)):
                        if punctuation[key]['char'] in split[x] or re.search(r'/(\d+)/', split[x]):
                            #split the sentance on the punctuation
                            if key == 'custom':
                                hold = re.split(r'/(\d+)/', split[x] )
                                #remove string that was split on
                                for i in customPauses:
                                    if i in hold:
                                        hold.remove(i)
                                holdTime = [punctuation[key]['pause'] for i in range(len(hold) - 1)]

                            else:
                                hold = split[x].split(punctuation[key]['char'])
                                holdTime = [punctuation[key]['pause'] for i in range(len(hold) - 1)]

                            #add punctuation back to the end of each split
                            if key != 'pause' and key != 'custom':
                                for i in range(len(hold) - 1):
                                    hold[i] += punctuation[key]['char']
                            


                            #add the split to the split list and remove the original sentance
                            split[x:x+1] = hold
                            #add the pause to the pause list
                            pauseRef= pauseRef[:x] + holdTime + pauseRef[x:]

            for i in range(len(split)):
                pyautogui.typewrite(split[i], interval=self.delay)
                
                if punctuation['custom']['pause'] == pauseRef[i]:
                    time.sleep(int(customPauses[0]))
                    customPauses.pop(0)
                else:
                    time.sleep(self.getPauseTime(pauseRef[i]))
                    
            
        else:
            #check there is more than one word
            if ' ' in text:
                #pick random work to pause for 
                words = text.split(' ')
                index = random.randint(0, len(words) - 1)
                pyautogui.typewrite(' '.join(words[:index]), interval=self.delay)
                pyautogui.typewrite(' '+words[index]+' ', interval=self.delay)
                #pause
                time.sleep(self.getPauseTime(9))
                pyautogui.typewrite(' '.join(words[index + 1:]), interval=self.delay)
            else:
                pyautogui.typewrite(text, interval=self.delay)
                time.sleep(self.getPauseTime(9))
        #time.sleep(self.punctuationPause)
    def getPauseTime(self, key:int = 0)-> float:
        """
            given a key, return the pause time
            input: key
            output: pause time in seconds
        """
        if key == 8:
            return 0
        if key == 5:
            return 10
        pauseTime = {
            0: [10,15],
            1: [7.5,10],
            2: [2.5,3.5],
            3: [3.5,5],
            4: [3.5,5],
            6: [2.5,3.5],
            9: [2.5,3.5]
        }
        #create random float between puasetime['key'][0 and 1] and return it as a float with 2 decimal places
        return round(random.uniform(pauseTime[key][0], pauseTime[key][1]), 2)


if __name__ == '__main__':

    exampleParagraph = """
Lorem ipsum /P/ dold/45/ictum /p/lorem.
    """
    time.sleep(5)
    Typeinator().timeToType(exampleParagraph, 3)