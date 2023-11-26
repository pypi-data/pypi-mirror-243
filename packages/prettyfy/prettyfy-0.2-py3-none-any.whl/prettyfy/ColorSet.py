import curses

class ColorSet():
    WIN7_COLOR_SET = {
        "FOREGROUND": {
            "black": 0x0000,
            "blue": 0x0001,
            "green": 0x0002,
            "cyan": 0x0003,
            "red": 0x0004,
            "magenta": 0x0005,
            "yellow": 0x0006,
            "white": 0x0007,
            
            '''intensity = 0x0008   foreground color is intensified.'''

            "bright_black": 0x0000 | 0x0008,
            "bright_blue": 0x0001 | 0x0008,
            "bright_green": 0x0002 | 0x0008,
            "bright_cyan": 0x0003 | 0x0008,
            "bright_red": 0x0004 | 0x0008,
            "bright_magenta": 0x0005 | 0x0008,
            "bright_yellow": 0x0006,
            "bright_white": 0x0007 | 0x0008,
        },

        "BACKGROUND": {
            "black": 0x0000,
            "blue": 0x0010,
            "green": 0x0020,
            "cyan": 0x0030,
            "red": 0x0040,
            "magenta": 0x0050,
            "yellow": 0x0060,
            "white": 0x0070,

            '''intensity = 0x0080  background color is intensified.'''

            "bright_black": 0x0000 | 0x0080,
            "bright_blue": 0x0010 | 0x0080,
            "bright_green": 0x0020 | 0x0080,
            "bright_cyan": 0x0030 | 0x0080,
            "bright_red": 0x0040 | 0x0080,
            "bright_magenta": 0x0050 | 0x0080,
            "bright_yellow": 0x0060 | 0x0080,
            "bright_white": 0x0070 | 0x0080,
        }

    }

    ANSI_COLOR_SET = {
        "FOREGROUND": {
            "black": "30",
            "red": "31",
            "green": "32",
            "yellow": "33",
            "blue": "34",
            "magenta": "35",
            "cyan": "36",
            "white": "37",
            
            "bright_black": "90",
            "bright_red": "91",
            "bright_green": "92",
            "bright_yellow": "93",
            "bright_blue": "94",
            "bright_magenta": "95",
            "bright_cyan": "96",
            "bright_white": "97",
        },

        "BACKGROUND": {
            "black": "40",
            "red": "41",
            "green": "42",
            "yellow": "43",
            "blue": "44",
            "magenta": "45",
            "cyan": "46",
            "white": "47",

            "bright_black": "100",
            "bright_red": "101",
            "bright_green": "102",
            "bright_yellow": "103",
            "bright_blue": "104",
            "bright_magenta": "105",
            "bright_cyan": "106",
            "bright_white": "107",
        }


    }
    MENU_COLOR_SET = {
        
        "black": curses.COLOR_BLACK,
        "red": curses.COLOR_RED,
        "green": curses.COLOR_GREEN,
        "yellow": curses.COLOR_YELLOW,
        "blue": curses.COLOR_BLUE,
        "magenta": curses.COLOR_MAGENTA,
        "cyan": curses.COLOR_CYAN,
        "white": curses.COLOR_WHITE,

        "bright_black": curses.COLOR_BLACK | 0x0008,
        "bright_red": curses.COLOR_RED | 0x0008,
        "bright_green": curses.COLOR_GREEN | 0x0008,
        "bright_yellow": curses.COLOR_YELLOW | 0x0008,
        "bright_blue": curses.COLOR_BLUE | 0x0008,
        "bright_magenta": curses.COLOR_MAGENTA | 0x0008,
        "bright_cyan": curses.COLOR_CYAN | 0x0008,
        "bright_white": curses.COLOR_WHITE | 0x0008,


    }
