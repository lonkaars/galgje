black = 30
red = 31
green = 32
yellow = 33
blue = 34
magenta = 35
cyan = 36
white = 37

blackBG  = 40
redBG = 41
greenBG = 42
yellowBG = 43
blueBG = 44
magentaBG = 45
cyanBG = 46
whiteBG = 47

bold = 1
faint = 2
italic = 3
underline = 4

reset = 0

def setColorEnabled(color):
    global colorEnabled
    colorEnabled = color

def stylize(word, styles):
    return f"\033[{';'.join(list(map(lambda int: str(int), styles)))}m{word}\033[{reset}m" if colorEnabled else word

