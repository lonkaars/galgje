import re, os, random, sys, character, color, argparse, messages

# character, color en messages zijn andere bestanden in dit project

def parseBool(string):
    return bool(string.lower() in ("true", "1")) # deze functie wordt gebruikt om te kijken of de --color vlag True moet zijn

def parseArgs():
    parser = argparse.ArgumentParser(description="Galje in python geschreven door Loek Le Blansch")
    parser.add_argument("--color", type=parseBool, help="Of kleuren aan staan (standaard uit op Windows)")
    parser.add_argument("--word", help="Een aangepast woord om galgje mee te spelen")
    return parser.parse_args()

# laat alleen woorden toe zonder leestekens, en die langer dan 2 letters zijn
def wordFilter(word):
    if len(word) <= 2: return "word_too_short"
    if len(word) >= 8: return "word_too_long"
    filtered = re.search(r"[0-9\'\".\-\s]", word) # regex met character set om te controleren op niet toegestane tekens in een woord (in dit geval leestekens)
    return "word_contains_invalid_characters" if filtered != None else True # stuur een string terug met de foutmelding, of True als de string toegestaan is

# laad woorden uit de ./words map, filter en voeg ze toe aan een dictionary
def loadWords():
    out = dict() # maak een dictionary voor de woorden
    for filename in os.listdir("./words"): # voor elk bestand in de words/ map
        if filename.endswith(".txt"): # negeer alle bestanden die niet eindigen met .txt
            out[filename[:-4]] = list() # voeg een key toe aan de out dictionary met de bestandsnaam zonder .txt er achter
            unfiltered = open(f"./words/{filename}", "r").read().split("\n") # lees de woordenlijst
            for word in unfiltered: # filter de woorden in de woordenlijst
                if wordFilter(word) == True:
                    out[filename[:-4]].append(word)
    return out

def endSequence(word, won):
    print(f"Het woord was {word}")
    if not won:
        print(character.death)
        print(messages.randomMessage("LOST_MESSAGE"))
    else:
        print(messages.randomMessage("GAME_END"))

# maak van een woord en geraden letters een woord met streepjes
def formatWord(word, guessed):
    out = ""
    for char in word:
        out += f"{char if char in guessed else color.stylize('_', [color.faint])} "
    return out[:-1] # haal laatste spatie weg

def checkIfWon(word, guessed):
    for letter in word:
        if not letter in guessed:
            return False
    return True

def clear():
    os.system("cls") # windows
    os.system("clear") # linux + unix

def createWordList():
    print(messages.randomMessage("LOADING_WORDS"), end="\n"*2)
    wordLists = loadWords()
    print(f"{color.stylize(len(wordLists), [color.blue, color.bold])} woordenlijst(en) gevonden!", end="\n"*2)
    allWords = list()
    for wordList in wordLists:
        print(f"Lijst {color.stylize(wordList, [color.blue])} met {color.stylize(len(wordLists[wordList]), [color.blue, color.bold])} woorden")
        allWords += wordLists[wordList]
    print(f"Er zijn in totaal {len(allWords)} woorden", end="\n"*2)
    return allWords

def guessWord(guess, word, moves):
    filteredWord = wordFilter(guess)
    if filteredWord != True or len(word) != len(guess):
        # Deze code zet de foutmeldingen van wordFilter() om naar strings die uitleggen wat je fout hebt gedaan
        error = filteredWord
        errorMessages = {
                "word_too_short": messages.randomMessage("ERR_WORD_TOO_SHORT"),
                "word_too_long": messages.randomMessage("ERR_WORD_TOO_LONG"),
                "word_contains_invalid_characters": messages.randomMessage("ERR_WORD_INVALID")
                }
        if len(guess) < len(word) and error == True: error = "word_too_short"
        elif len(guess) > len(word) and error == True: error = "word_too_long"

        print(color.stylize(errorMessages.get(error), [color.yellow]))
        return 0
    if word == guess:
        endSequence(word, True)
        return len(moves) * -1 # trek alle beurten af
    else:
        print(color.stylize("Dat is niet mijn woord!", [color.red]))
        return -1

def guessChar(guess, word, guessed):
    if guess in guessed:
        print(color.stylize(f"De letter {guess} heb je al geraden", [color.yellow]))
        return 0
    else:
        print(color.stylize(f"De letter {guess} zit{' niet' if not guess in word else ''} in mijn woord", [color.green if guess in word else color.red]))
        return int(guess in word) - 1

# stuurt terug hoeveel beurten er af getrokken moeten worden (want continue werkt niet hier)
def guessHandler(guess, word, moves, guessed):
    if len(guess) > 1:
        return guessWord(guess, word, moves)
    elif len(guess) == 1:
        return guessChar(guess, word, guessed)
    else:
        print(color.stylize(messages.randomMessage("ERR_NO_WORD_GUESSED"), [color.yellow]))
        return 0

def game(word):
    moves = len(character.character)
    guessed = set() # hier gebruik ik een set zodat ik zelf geen rekening hoef te houden met dubbele gokken
    print(f"Ik heb een woord in gedachten van {color.stylize(len(word), [color.magenta, color.bold])} letters", end="\n"*2)

    while moves > 0:
        if checkIfWon(word, guessed):
            endSequence(word, True)
            break # spring uit de while loop

        print(f"\t{formatWord(word, guessed)}\nJe kunt nog {color.stylize(moves, [color.green, color.bold])} keer raden")
        if len(guessed) > 0: print(f"De dingen die je al geraden hebt zijn: {', '.join(guessed)}") # print alleen je geraden letters als je meer dan 0 letters geraden hebt
        print(color.stylize(character.character[::-1][moves - 1], [color.bold])) # print het juiste poppetje uit character.py
        guess = input(color.stylize(messages.randomMessage("GUESS_PROMPT") + " ", [color.green, color.bold])).lower()
        print("\n"*2) # witregels
        moves += guessHandler(guess, word, moves, guessed)
        if len(guess) > 0: guessed.add(guess)
    if not checkIfWon(word, guessed):
        endSequence(word, False)

def main():
    args = parseArgs()
    if args.word: clear()
    color.setColorEnabled(args.color if args.color != None else sys.platform != "win32") # zet kleuren automatisch uit op Windows
    print(color.stylize(messages.randomMessage("GAME_START"), [color.magenta]))
    if sys.platform == "win32": print("Dit programma gebruikt ANSI codes om gekleurde tekst te laten zien, gebruik de --color true vlag om ze aan te forceren op een terminal die ze ondersteunt")
    allWords = list()
    if not args.word: allWords = createWordList() # laad alleen de woordenlijst als er geen aangepast woord is gegeven
    word = args.word or random.choice(allWords) # or zorgt er hier voor dat word niet overschreven wordt door random.choice als args.word geen lege string is
    word = word.lower() # zorg dat het woord geen hoofdletters bevat
    game(word)

if __name__ == "__main__":
    main()
