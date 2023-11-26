import platform

from .Decor import Decor
from .Win7_Colorizer import Win7_Colorizer
from .ANSI_Colorizer import ANSI_Colorizer
from .MenuDriver import MenuDriver
from .safe_exec import safe_exec


# TextColorizer = Win7_Colorizer
TextColorizer = Win7_Colorizer if "Windows" in platform.platform() and int(platform.release()) < 10 else ANSI_Colorizer


def colorizeText(string, FgColor : str = None, BgColor : str = None, JustTextBG: bool = False):

    only_text = JustTextBG

    TextColorizer(string = string, FgColor = FgColor, BgColor = BgColor).Colorize(JustTextBG = only_text)

def Input(prompt = "", FgColor : str = None, BgColor: str = None):
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