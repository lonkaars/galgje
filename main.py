import re, os, random, sys, character, color

def wordFilter(word): # laat alleen woorden toe zonder leestekens, en die langer dan 2 letters zijn
    if len(word) <= 2: return False
    if len(word) >= 8: return False
    filtered = re.search(r"[0-9\'\".\-\s]", word)
    return filtered == None

def loadWords(): # laad woorden uit de ./words map, filter en voeg ze toe aan een dictionary
    out = dict()
    for filename in os.listdir("./words"):
        if filename.endswith(".txt"):
            out[filename[:-4]] = list()
            unfiltered = open(f"./words/{filename}", "r").read().split("\n")
            for word in unfiltered:
                if wordFilter(word):
                    out[filename[:-4]].append(word)
    return out

def endSequence(word, won):
    print(f"Het woord was {word}")
    if not won:
        print(character.death)
    else:
        print("Dat was hem weer jongens")

def formatWord(word, guessed): # maak van een woord en geraden letters een woord met streepjes
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

def wordFromArgs():
    for arg in sys.argv:
        if not arg.endswith('.py'):
            if len(arg) != 0: clear() # leeg scherm bij aangepast woord
            return arg

def createWordList():
    print("Op het moment worden alle woorden in words/ geladen:", end="\n"*2)
    wordLists = loadWords()
    print(f"{color.stylize(len(wordLists), [color.blue, color.bold])} woordenlijst(en) gevonden!", end="\n"*2)
    allWords = list()
    for wordList in wordLists:
        print(f"Lijst {color.stylize(wordList, [color.blue])} met {color.stylize(len(wordLists[wordList]), [color.blue, color.bold])} woorden")
        allWords += wordLists[wordList]
    print(f"Er zijn in totaal {len(allWords)} woorden", end="\n"*2)
    return allWords

def guessWord(guess, word, moves):
    if not wordFilter(guess) or len(word) != len(guess):
        print(color.stylize("Je invoer is ongeldig!", [color.yellow]))
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

def guessHandler(guess, word, moves, guessed): # stuurt terug hoeveel beurten er af getrokken moeten worden (want continue werkt niet hier)
    if len(guess) > 1:
        return guessWord(guess, word, moves)
    elif len(guess) == 1:
        return guessChar(guess, word, guessed)
    else:
        print(color.stylize("Je moet wel een letter of woord gokken", [color.yellow]))
        return 0

def main():
    argsWord = wordFromArgs()
    print(color.stylize("Welkom bij galgje!", [color.magenta]))
    if sys.platform == "win32": print("Dit programma gebruikt ANSI codes om gekleurde tekst te laten zien, gebruik Git Bash of Cygwin op Windows als je kleuren wilt zien")
    allWords = list()
    if not argsWord: allWords = createWordList()

    # hoofdgedeelte
    word = argsWord or random.choice(allWords).lower()
    moves = len(character.character)
    guessed = set()
    print(f"Ik heb een woord in gedachten van {color.stylize(len(word), [color.magenta, color.bold])} letters", end="\n"*2)

    while moves > 0:
        if checkIfWon(word, guessed):
            endSequence(word, True)
            break

        print(f"\t{formatWord(word, guessed)}\nJe kunt nog {color.stylize(moves, [color.green, color.bold])} keer raden")
        # print alleen je geraden letters als je meer dan 0 letters geraden hebt
        if len(guessed) > 0: print(f"De dingen die je al geraden hebt zijn: {', '.join(guessed)}")
        print(color.stylize(character.character[::-1][moves - 1], [color.bold])) # print het juiste poppetje uit character.py
        guess = input(color.stylize("Raad een letter of woord: ", [color.green, color.bold])).lower()
        print("\n"*2) # witregels
        moves += guessHandler(guess, word, moves, guessed)
        if len(guess) > 0: guessed.add(guess)
    if not checkIfWon(word, guessed):
        endSequence(word, False)

if __name__ == "__main__":
    main()
