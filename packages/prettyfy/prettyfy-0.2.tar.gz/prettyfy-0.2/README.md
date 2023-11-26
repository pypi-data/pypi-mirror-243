# Prettyfy
 A package of the everyone to beautify their console applicaions and CLI's(Command Line Interfaces).

## Installation
```cmd
pip install prettyfy
```
## github page:
[Click here](https://github.com/Shanmukh-dev/Prettyfy-Package)
## Usage
```python
import prettyfy
from prettyfy import *
import os


colorize = TextColorizer
colorize.DefaultBg = "bright_cyan"
colorize.DefaultFg = "black"


colorize().SetDefaultTheme()
init_boxStyle("Shanti-style", (("<->", "<->", "<->"), ("<->", "<->", "<->"), "<+>"))


def Option1():
    Print("This is option 1")
def Option2():
    Print("This is option 2")
def Option3():
    Print("This is option 3")
def Option4():
    Print("This is option 3")


menuList = ["Option1", "Option2", "Option3", "Option4"]



choice = MenuDriver(TextColorizer=colorize, MenuList=menuList, header = "Shanti-style", header_border_style = "Shanti-style", SelectionStyle = "INVERT", BgColor = "bright_cyan", FgColor = "black" ).GetChoice()

exec(f"{choice}()")



ColorizeText = colorizeText


colorizeText(FgColor="black", BgColor="cyan", string="Hope this works...")


colorizeText(FgColor="bright_white", BgColor="bright_red", string="This must be bright")


colorizeText(FgColor="white", BgColor="red", string="This must be normal JustTextBG", JustTextBG = True)


colorizeText(FgColor="white", BgColor="red", string="""This must be normal
...I think""")

Print("This is another print")


colorizeText(FgColor="white", BgColor="red", string="""This must be normal
...I think JustTextBG""", JustTextBG = True)

colorizeText(FgColor="white", BgColor="red", string={1:"one", 2:"two", 3:"three"}, JustTextBG = True)



Print(45654)
Print({1:"one", 2:"two", 3:"three"})
Print("This is another print")
Print("This is another print")
Print("This is another print", "This is continued", "Sep test", sep="///////////")

boxed = Decor.boxstr("bold", """Love
Coding""")

Print(boxed)
Print()

colorize(FgColor="white", BgColor="red", string=boxed).Colorize(JustTextBG = True)
Print()
colorize(FgColor="white", BgColor="red", string=boxed).Colorize()

val = Input("\nGetting colored input: ")
Print(val)

boxed1 = Decor.boxstr(string="""Love
Coding...""", style="Shanti-style")

Print(boxed1)

input()


colorize().Reset()

```

## Examples
### Menu
![menu example](images/image1.png)

### Text colorization
![text colorization exaple](images/image2.png)

## Building CLI
```python
# ---------------------------Under development--------------------------------
from prettyfy.CliUtils import *
import hashlib


TextColorizer.DefaultBg = 'black'
TextColorizer.DefaultFg = 'bright_green'
TextColorizer().SetDefaultTheme()
header = decor.boxstr(style = 'simple', string = "Hash-gen")

Print(header)

@CliUtils()
def gen_hash(name):
    txt = name.encode()
    print(hashlib.md5(txt).hexdigest())
TextColorizer().Reset()
```