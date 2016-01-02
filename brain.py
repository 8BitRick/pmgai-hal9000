# -*- coding: utf-8 -*-

class Brain(object):
    def __init__(self):
        self.num_responses = 0
        self.location = "lobby"
    
    def get_response(self,in_str):
        out_str = "blah blah blah"
        if(self.num_responses <= 0):
            out_str = "Buenos Dias, Senor! My name is HAL, what is yours?"
        elif(in_str == "Where am I?"):
            out_str = "You are in the " + self.location                            
        self.num_responses += 1
        return out_str
        
    def relocate_to(self,in_str):
        self.location = in_str
    