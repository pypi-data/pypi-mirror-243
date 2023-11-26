from .ColorSet import ColorSet
from .Decor import Decor

import os
import sys


class ANSI_Colorizer:
    DefaultFg : str = "white"
    DefaultBg : str = "black"

    

    def Print(*text, sep: str = " ", end: str = "\n"):

        width = os.get_terminal_size().columns 
        text = (" ",) if text == () else text
        print_contents = " "

        if len(text) == 1:
            if type(text[0]).__name__ == "list" or type(text[0]).__name__ == "set" or type(text[0]).__name__ == "tuple" or type(text[0]).__name__ == "dict":
                print_contents = Decor.prettyprint(text[0])
            else:
                string_list = map(str, text)
                print_contents = sep.join(string_list)
        else:        
            string_list = map(str, text)
            print_contents = sep.join(string_list)

        lines = print_contents.splitlines()
        length = [(len(line), line) for line in lines]
        for line in length:
            
            print(line[1] + " " * (width - line[0]), sep = sep, end = end)


    def __init__(self, string = "", FgColor : str = None, BgColor : str = None) -> None:
        if sys.platform == 'win32': os.system("")

        self.COLORS = ColorSet.ANSI_COLOR_SET

        FgColor = self.DefaultFg if FgColor == None else FgColor
        BgColor = self.DefaultBg if BgColor == None else BgColor


        self.default_fg = self.COLORS["FOREGROUND"][self.DefaultFg]
        self.default_bg = self.COLORS["BACKGROUND"][self.DefaultBg]

        self.FgColor = self.COLORS["FOREGROUND"][FgColor]
        self.BgColor = self.COLORS["BACKGROUND"][BgColor]
        self.string = string

        self.ColorEscape = f"\x1b[{self.FgColor};{self.BgColor}m"
        self.DefaultColorEscape = f"\x1b[{self.default_fg};{self.default_bg}m"
        self.ResetEscape = "\x1b[37;40m"

    def eval_(self, exp):
        try:
            val = eval(exp)
            return val
        except:
            return str(exp)

    def CPrint(self, text = None, JustTextBG : bool = False):
        width = os.get_terminal_size().columns 
        text = self.eval_(text)

        if text != None:
            if type(text).__name__ == "list" or type(text).__name__ == "set" or type(text).__name__ == "tuple" or type(text).__name__ == "dict":
                text = Decor.prettyprint(text)
            else:
                text = str(text)

            lines = text.splitlines()
            
            length_lines = [(len(line), line) for line in lines]

            
            for i, line in enumerate(length_lines):
                if not JustTextBG:
                    print(line[1] + " " * (width - line[0]), end="")
                else:
                    print(line[1] , end="")
                    print(self.DefaultColorEscape, end="")
                    if i == len(length_lines) - 1:
                        print(" " * (width - line[0]), end= "")
                        print(self.DefaultColorEscape, end="")

                    else:
    
                        print(" " * (width - line[0]))
                        print(self.ColorEscape, end="")

    def Colorize(self, JustTextBG : bool = False):
        print(self.ColorEscape, end="")

        text = self.string
        self.CPrint(text = str(text), JustTextBG = JustTextBG)

        print(self.DefaultColorEscape, end="\n")

    def Input(self, prompt: str = ""):
        print(self.ColorEscape, end="")
        prompt = prompt.splitlines()
        width = os.get_terminal_size().columns 
        for i, txt in enumerate(prompt):
            if i != len(prompt) - 1:
                print(txt, " " * ((width-1) - len(txt)))
            else:
                value = input(txt)
        print(self.DefaultColorEscape, end="")
        return value

    def Reset(self):
        print(self.ResetEscape)

    def SetDefaultTheme(self):
        print(self.DefaultColorEscape + "")



# -----------------------------------Tests---------------------------------------------------- #


# colorize = ANSI_Colorizer


# colorize.DefaultBg = "BRIGHT_CYAN"
# colorize.DefaultFg = "BLACK"

# colorize().SetDefaultTheme()

# colorize(FgColor="BLACK", BgColor="BRIGHT_CYAN", string="Hope this works...").Colorize()

# colorize().Reset()
