import json

LINE_CHARACTERS = {
    "single": "─",
    "double": "═",
    "simple_dash": "-",
    "squigle": "~",
    "bold": "▬"
}
BOX_CHARACTERS = {
    "rounded": (("╭", "─", "╮"), ("╰", "─", "╯"), "│"),
    "sharp": (("┌", "─", "┐"), ("└", "─", "┘"), "│"),
    "tech": (("/", "─", "\\"), ("\\", "─", "/"), "│"),
    "simple": (("+", "-", "+"), ("+", "-", "+"), "|"),
    "double_box": (("╔", "═", "╗"), ("╚", "═", "╝"), "║"),
    "squigle": (("╭", "~", "╮"), ("╰", "~", "╯"), "│"),
    "bold": (("▄", "▀", "▄"), ("▀", "▄", "▀"), "█"),
}


class Decor():

    
    def init_box_style(StyleName: str, BoxChars: tuple):
        BOX_CHARACTERS[StyleName] = BoxChars

    def init_line_style(StyleName: str, LineChar: tuple):
        LINE_CHARACTERS[StyleName] = LineChar

    def drawLine(style, length):
        char = LINE_CHARACTERS[style]
        return char*length

        
    def boxstr(style, string):
        boxed_str = ""
        lines = string.splitlines()
        box_elements = BOX_CHARACTERS[style]
        width = max([len(i) for i in lines])
        boxed_str += f"{box_elements[0][0] + box_elements[0][1] * ((width // len(box_elements[0][1])) + 2) + box_elements[0][2]}\n"
        for i, line in enumerate(lines):
            boxed_str += f"{box_elements[2] + ' ' + lines[i] + ' ' + ' '  * (width-len(lines[i])) + box_elements[2]}\n"

        boxed_str += f"{box_elements[1][0] + box_elements[1][1] * (width // len(box_elements[1][1]) + 2) + box_elements[1][2]}"
        return boxed_str
    
    def prettyprint(seq, indent = 2):
        return json.dumps(seq, indent = indent)




# -----------------------------------Tests---------------------------------------------------- #


# Decor.drawLine("single", 40)
# Decor.drawLine("double", 40)
# Decor.drawLine("simple_dash", 40)
# Decor.drawLine("squigle", 40)
# Decor.drawLine("bold", 40)

#box("rounded", 10, 10)
#box("sharp", 10, 10)
#box("simple", 10, 10)
#box("double_box", 10, 10)
#box("tech", 10, 10)

# Decor.boxstr("rounded", """Hi this is great
# if this works"""
# )
# Decor.boxstr("sharp", """Hi this is great
# if this works"""
# )
# Decor.boxstr("simple", """Hi this is great
# if this works"""
# )
# Decor.boxstr("double_box", """Hi this is great
# if this works"""
# )
# Decor.boxstr("tech", """Hi this is great
# if this works"""
# )
# Decor.boxstr("squigle", """Hi this is great
# if this works"""
# )
# Decor.boxstr("bold", """Hi this is great
# if this works"""
# )
