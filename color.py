colors = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,

    "blackBG": 40,
    "redBG": 41,
    "greenBG": 42,
    "yellowBG": 43,
    "blueBG": 44,
    "magentaBG": 45,
    "cyanBG": 46,
    "whiteBG": 47,

    "reset": 0
}

def colorize(word, userColors):
    return f"\033[{';'.join(list(map(lambda int: str(int), userColors)))}m{word}{colors['reset']}"


