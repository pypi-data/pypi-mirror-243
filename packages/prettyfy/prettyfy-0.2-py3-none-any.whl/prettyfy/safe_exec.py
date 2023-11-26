# -------------------------------------Under development-------------------------------------------------

from .Decor import Decor
from .Win7_Colorizer import Win7_Colorizer
from .ANSI_Colorizer import ANSI_Colorizer


import sys
import platform
import os

TextColorizer = Win7_Colorizer if "Windows" in platform.platform() and int(platform.release()) < 10 else ANSI_Colorizer

def safe_exec():
    args = sys.argv
    filePath = args[-1]
    if "safe_exec" in args:
        if os.path.exists(filePath):
            with open(filePath) as f:
                contents = f.read()
                try:
                    exec(contents, globals())
                except Exception as e:
                    TextColorizer.DefaultBg = "bright_red"
                    TextColorizer.DefaultFg = "black"
                    TextColorizer().SetDefaultTheme()
                    TextColorizer.Print(f"Error: {e}")
                    TextColorizer.Print(f"Error type: {type(e).__name__}")

                    tb = e.__traceback__
                    while tb.tb_next:
                        tb = tb.tb_next
                        # TextColorizer.Print(f"Error raised at module: {tb.tb_frame.f_globals.get('__name__')}")

                    TextColorizer.Print(f"Error at line(in your file): {tb.tb_lineno}")
    elif ("safe_exec" in args and args[-1] == "--help") or ("safe_exec" in args and args[-1] == "-h"):
        TextColorizer.DefaultBg = "Black"
        TextColorizer.DefaultFg = "bright_cyan"
        TextColorizer().SetDefaultTheme()

        TextColorizer.Print(Decor.boxstr(string = """usage: prettyfy safe_exec <file-path>

Executes file vritually to find errors""",style = "simple"))
    elif ("prettyfy" in args and args[-1] == "--help") or("prettyfy" in args and args[-1] == "-h"):
        TextColorizer.DefaultBg = "Black"
        TextColorizer.DefaultFg = "bright_cyan"
        TextColorizer().SetDefaultTheme()
        TextColorizer.Print(Decor.boxstr(srting = 
"""usage: 
    
    prettyfy <command>

    Commands:

    safe_exec <file-path> : Executes file vritually to find errors"""
        ,style = "simple"))

    
    else:
        pass