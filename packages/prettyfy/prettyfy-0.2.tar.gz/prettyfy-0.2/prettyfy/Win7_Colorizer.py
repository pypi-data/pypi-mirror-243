import ctypes as ct
from .ColorSet import ColorSet
from .Decor import Decor

import os


class Win7_Colorizer():
    # ct.windll.kernel32.SetConsoleTextAttribute(stdout,0x0080 | 0x0008 |0x0070 | 0x0004)
    # bgIntensity|fgIntensity|BgColor|FgColor
    DefaultFg: str = "white"
    DefaultBg: str = "black"
    intensify: bool = False
    def Print(*text, sep: str = " ", end: str = "\n"):
        width = os.get_terminal_size().columns - 1
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

    def __init__(self, string="", FgColor: str = None, BgColor: str = None) -> None:

        FgColor = self.DefaultFg if FgColor == None else FgColor
        BgColor = self.DefaultBg if BgColor == None else BgColor

        self.STDHANDLE = -11

        self.COLORS = ColorSet.WIN7_COLOR_SET
        self.stdout = ct.windll.kernel32.GetStdHandle(self.STDHANDLE)
        self.colorInitiator = ct.windll.kernel32.SetConsoleTextAttribute

        self.default_fg = self.COLORS["FOREGROUND"][self.DefaultFg]
        self.default_bg = self.COLORS["BACKGROUND"][self.DefaultBg]

        self.BgColor = BgColor
        self.FgColor = FgColor
        self.string = string

        
    def eval_(self, exp):
        try:
            val = eval(exp)
            return val
        except:
            return str(exp)

    def CPrint(self, text : str = None, JustTextBG : bool= False):
        width = os.get_terminal_size().columns - 1
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
                    print(line[1] + " " * (width - line[0]))
                else:

                    print(line[1], end = "", flush = True)
                    self.SetDefaultTheme()
                    print(" " * (width - line[0]))
                    self.colorInitiation()

    def colorInitiation(self):
        self.colorInitiator(
                self.stdout, self.COLORS["BACKGROUND"][self.BgColor] | self.COLORS["FOREGROUND"][self.FgColor])

            

    def Colorize(self, JustTextBG : bool = False):
        
        self.colorInitiation()
        onlyText = JustTextBG
        
        self.CPrint(self.string, JustTextBG = onlyText)
        self.SetDefaultTheme()


    def Input(self, prompt: str = ""):
        self.colorInitiation()
        prompt = prompt.splitlines()
        width = os.get_terminal_size().columns 
        for i, txt in enumerate(prompt):
            if i != len(prompt) - 1:
                print(txt, " " * ((width-1) - len(txt)))
            else:
                value = input(txt)
        self.SetDefaultTheme()
        return value


    def SetDefaultTheme(self):
        self.colorInitiator(self.stdout, self.default_bg | self.default_fg)

    def Reset(self):
        self.colorInitiator(
            self.stdout, self.COLORS["BACKGROUND"]["black"] | self.COLORS["FOREGROUND"]["white"])


# -----------------------------------Tests---------------------------------------------------- #


# Win7_Colorizer(string="Hope this works", DefaultBg="RED",
#             DefaultFg="BLUE").Colorize()
# print("")
# Win7_Colorizer(FgColor="BLACK", BgColor="CYAN", string="Hope this works",
#             DefaultBg="RED", DefaultFg="BLUE").Colorize()
# print("")

# Win7_Colorizer(string="Hope this works", DefaultBg="RED",
#             DefaultFg="BLUE").Colorize()

# Win7_Colorizer().Reset()


# colorize = Win7_Colorizer

# colorize.DefaultBg = "CYAN"
# colorize.DefaultFg = "BLACK"

# colorize().SetDefaultTheme()
# colorize(FgColor="BLACK", BgColor="CYAN", string="Hope this works...").Colorize()

# colorize.intensify = True

# colorize(FgColor="WHITE", BgColor="RED", string="This must be bright").Colorize()

# colorize.intensify = False

# colorize(FgColor="WHITE", BgColor="RED", string="This must be normal").Colorize()


# colorize().Reset()
