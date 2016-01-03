# -*- coding: utf-8 -*-

import nltk.chat
import win32com.client

AGENT_RESPONSES = [
  (r'You are (worrying|scary|disturbing)',    # Pattern 1.
    ['Yes, I am %1.',                         # Response 1a.
     'Oh, sooo %1.']),

  (r'Are you ([\w\s]+)\?',                    # Pattern 2.
    ["Why would you think I am %1?",          # Response 2a.
     "Would you like me to be %1?"]),

  (r'',                                       # Pattern 3. (default)
    ["Is everything OK?",                     # Response 3a.
     "Can you still communicate?"])
]

class Brain(object):
    def __init__(self):
        self.num_responses = 0
        self.location = "lobby"
        self.chatbot = nltk.chat.Chat(AGENT_RESPONSES, nltk.chat.util.reflections)
        self.voice = win32com.client.Dispatch("SAPI.SpVoice")

    def get_response(self,in_str):
        out_str = "blah blah blah"
        if(self.num_responses <= 0):
            out_str = "Buenos Dias, Senor! My name is HAL, what is yours?"
        elif(in_str == "Where am I?"):
            out_str = "You are in the " + self.location        
        else:
            out_str = self.chatbot.respond(in_str)        
        self.num_responses += 1
        
        self.voice.Speak(out_str)
        return out_str
        
    def relocate_to(self,in_str):
        self.location = in_str
    