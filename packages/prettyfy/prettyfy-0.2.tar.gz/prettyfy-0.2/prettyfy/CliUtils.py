from .Decor import Decor
from .ANSI_Colorizer import ANSI_Colorizer
from .Win7_Colorizer import Win7_Colorizer
from .MenuDriver import MenuDriver

import sys
import platform

menuDriver = MenuDriver
decor = Decor
TextColorizer = Win7_Colorizer if "Windows" in platform.platform() and int(platform.release()) < 10 else ANSI_Colorizer


class CliUtils:
    def __init__(self):
        
        self.shellArgs = sys.argv[1::]

        self.commands = {}

    def __call__(self, func):
        self.command(func)
        self._execute()
        

    def command(self, func):
        self.commands[func.__name__] = func

    def getargs(self):
        command = self.shellArgs[0]
        options = [opts for opts in self.shellArgs if opts.startswith("-")]
        args = self.shellArgs[-1] if self.shellArgs[-1] not in command and self.shellArgs[-1] not in options else None

        return command, options, args
    def getCommands(self):
        return self.commands
    
    def _execute(self):
        command, options, args = self.getargs() 

        if command in list(self.commands.keys()):
            try:
                self.commands[command](options, args)
            except:
                self.commands[command](args)
    


# ------------------------------------Extra function------------------------------------------

def colorizeText(string = "", FgColor : str = None, BgColor : str = None, JustTextBG: bool = False):

    only_text = JustTextBG

    TextColorizer(string = string, FgColor = FgColor, BgColor = BgColor).Colorize(JustTextBG = only_text)


def Input(prompt = "", FgColor : str = None, BgColor : str = None):
    value = TextColorizer(FgColor = FgColor, BgColor = BgColor).Input(prompt=prompt)
    return value


def Print(*text, sep: str = " ", end: str = "\n"):
    TextColorizer.Print(*text, sep = sep, end = end)


def init_boxStyle(StyleName: str, BoxChars: tuple):
    if StyleName != None and BoxChars != None:
        Decor.init_box_style(StyleName, BoxChars)
    else:
        pass


def init_lineStyle(StyleName: str, LineChar: tuple):
    if StyleName != None and LineChar != None:
        Decor.init_line_style(StyleName, LineChar)
    else:
        pass    



# ---------------------------------------------Tests-----------------------------------------------------



# @CliUtils()
# def greet(name):
#     print("hello", name)
