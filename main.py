#
# This file is part of The Principles of Modern Game AI.
# Copyright (c) 2015, AiGameDev.com KG.
#

import vispy                    # Main application support.

import window                   # Terminal input and display.

import brain # module for HAL's brain
import speech_recognition as sr
import speech
import logging
import sys

class HAL9000(speech.SpeechMixin):
#class HAL9000(object):

    def __init__(self, terminal, brain):
        super().__init__()
        """Constructor for the agent, stores references to systems and initializes internal memory.
        """
        self.terminal = terminal
        self.brain = brain
        self.location = 'unknown'
        
        logging.basicConfig(filename="std.log")
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)
        self.log = root
#        self.r = sr.Recognizer()
#        self.r.energy_threshold = 1000           # Tune based on ambient noise levels [1000,4000].

    def __del__(self):
        self.stop()

    def on_input(self, evt):
        """Called when user types anything in the terminal, connected via event.
        """
        self.terminal.log(self.brain.get_response(evt.text), align='right', color='#00805A')

    def on_command(self, evt):
        """Called when user types a command starting with `/` also done via events.
        """
        if evt.text == 'quit':
            vispy.app.quit()

        elif evt.text.startswith('relocate'):
            self.terminal.log('', align='center', color='#404040')
            self.terminal.log('\u2014 Now in the {}. \u2014'.format(evt.text[9:]), align='center', color='#404040')
            self.brain.relocate_to(evt.text[9:])
        elif evt.text.startswith('listen'):
            self.terminal.log('Listening', align='right', color='#ff3000')
#            with sr.Microphone() as source:     # Use the default microphone as the audio source.
#                audio = self.r.listen(source)        # Listen for single phrase and extract as audio.
#            try:
#                text = self.r.recognize_google(audio)       # Extract text using Google Speech Recognition.
#            except LookupError:
#                text = "Did not understand"                     # Could not recognize anything from audio...
#            print(text)
            #self.listen()
        else:
            self.terminal.log('Command `{}` unknown.'.format(evt.text), align='left', color='#ff3000')    
            self.terminal.log("I'm afraid I can't do that.", align='right', color='#00805A')

    def onMessage(self, source, message):
        if(message is None or message == ""):
            self.terminal.log("Heard something inaudible")
        else:
            self.terminal.log('Heard from microphone: ' + message)
            self.terminal.log(self.brain.get_response(message), align='right', color='#00805A')

    def update(self, _):
        """Main update called once per second via the timer.
        """
        pass


class Application(object):
    
    def __init__(self):
        # Create and open the window for user interaction.
        self.window = window.TerminalWindow()
        
        # Initialize HAL's brain
        self.brain = brain.Brain()
        
        # Print some default lines in the terminal as hints.
        self.window.log('Operator started the chat.', align='left', color='#808080')
        self.window.log('HAL9000 joined.', align='right', color='#808080')

        # Construct and initialize the agent for this simulation.
        self.agent = HAL9000(self.window, self.brain)

        # Connect the terminal's existing events.
        self.window.events.user_input.connect(self.agent.on_input)
        self.window.events.user_command.connect(self.agent.on_command)

    def run(self):
        timer = vispy.app.Timer(interval=1.0)
        timer.connect(self.agent.update)
        timer.start()
        
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
