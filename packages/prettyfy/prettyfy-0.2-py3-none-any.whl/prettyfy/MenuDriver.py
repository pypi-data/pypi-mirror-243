from .ColorSet import ColorSet
from .Decor import Decor

import curses
from curses import wrapper
import time
import os


class MenuDriver:

    SELECTION_STYLE = {
        "INVERT": curses.A_REVERSE,
        "LIGHT_HIGHLIGHT": curses.A_BLINK,
        "BOLD" : curses.A_BOLD,
        "STANDOUT": curses.A_STANDOUT
    }

    def __init__(self, TextColorizer, MenuList, FgColor : str = None, BgColor : str = None, header: str = " ", header_border_style = "simple", separatorStyle = "simple_dash", SelectionStyle: str = 0) -> None:
        
        self.MenuList = MenuList
        self.choice = 0
        self.width = os.get_terminal_size().columns
        self.SelectionStyle = ["INVERT"] if SelectionStyle == 0 else SelectionStyle.split()

        self.header = "---Menu header here---" if header == " " else header
        self.header_border_style = header_border_style
        self.separatorStyle = separatorStyle

        self.colors = ColorSet.MENU_COLOR_SET#

        self.default_fg = self.colors[TextColorizer.DefaultFg]#
        self.default_bg = self.colors[TextColorizer.DefaultBg]#

        self.FgColor = self.colors[TextColorizer.DefaultFg] if FgColor == None else self.colors[FgColor]#
        self.BgColor = self.colors[TextColorizer.DefaultBg] if FgColor == None else self.colors[BgColor]#

        wrapper(self.Menu)


    

    def Menu(self, stdscr):
       
        self.stdscr = stdscr

        def Cprint(string: str = " ", color_pair: int = 1):
            lines = string.splitlines()
            for line in lines:
                self.stdscr.addstr(f"{line}{' ' * (self.width - len(line))}", curses.color_pair(color_pair))

        self.maxWidth = max([len(i) for i in self.MenuList])
        curses.init_pair(1, self.FgColor, self.BgColor)


        
        self.stdscr.clear()
        
        

        while True:
            
            self.stdscr.clear()

            Cprint(f"{Decor.boxstr(style = self.header_border_style, string = self.header)}\n\n", 1)

            Cprint(f"+{Decor.drawLine(style = self.separatorStyle, length = self.maxWidth + 2)}+\n", 1)

            style = 0
            for i in self.SelectionStyle:
                style = style|self.SELECTION_STYLE[i]
            for i, option in enumerate(self.MenuList):
                if i == self.choice:
                    
                    selected_option = f">> {option}"
                    self.stdscr.addstr(f"{selected_option}{' ' * (self.width - len(selected_option))}", curses.color_pair(1) | style)
                    self.stdscr.refresh()
                else:
                    Cprint(option, 1)
                    self.stdscr.refresh()

            Cprint(f"+{Decor.drawLine(style = self.separatorStyle, length = self.maxWidth + 2)}+\n", 1)
            Cprint(string = "\n# Use arrow keys to navigate\n# Press Enter to select\n# Press Esc to cancell\n\n", color_pair = 1)
            try:
                self.key = self.stdscr.getkey()
            except:
                self.key = None
            
            
            if self.key == "KEY_RIGHT" or self.key == "KEY_DOWN":
                if self.choice >= len(self.MenuList) - 1:
                    self.choice = 0
                else:
                    self.choice += 1
            elif self.key == "KEY_LEFT" or self.key == "KEY_UP":
                if self.choice <= 0:
                    self.choice = len(self.MenuList) - 1
                else:
                    self.choice -= 1
            elif self.key == "\n":
                self.stdscr.addstr(f"Redirecting to {self.MenuList[self.choice]}", curses.color_pair(1) | style)
                self.stdscr.refresh()

                time.sleep(1.5)
                break
            elif self.key == "\x1b":

                self.stdscr.addstr("Cancelled. Press any key to continue.")
                self.stdscr.refresh()

                self.stdscr.getch()
                return None
                break

    def GetChoice(self):
        return self.MenuList[self.choice]
           



# choice = MenuDriver(MenuList = ["Option1", "Option2", "Option3", "Option4"]).GetChoice()

# print(choice)