import re, os, random, sys, character

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
        out += f"{char if char in guessed else '_'} "
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
    print(f"{len(wordLists)} woordenlijst(en) gevonden!", end="\n"*2)
    allWords = list()
    for wordList in wordLists:
        print(f"Lijst {wordList} met {len(wordLists[wordList])} woorden")
        allWords += wordLists[wordList]
    print(f"Er zijn in totaal {len(allWords)} woorden", end="\n"*2)
    return allWords

def guessWord(guess, word, moves):
    if not wordFilter(guess):
        print("Je invoer is ongeldig!")
        return 0
    if word == guess:
        endSequence(word, True)
        return len(moves) * -1 # trek alle beurten af
    else:
        print("Dat is niet mijn woord!")
        return -1

def guessChar(guess, word, guessedCharacters):
    if guess in guessedCharacters:
        print(f"De letter {guess} heb je al geraden")
        return 0
    else:
        print(f"De letter {guess} zit{' niet' if not guess in word else ''} in mijn woord")
        return int(guess in word) - 1

def guessHandler(guess, word, moves, guessedCharacters): # stuurt terug hoeveel beurten er af getrokken moeten worden (want continue werkt niet hier)
    if len(guess) > 1:
        return guessWord(guess, word, moves)
    elif len(guess) == 1:
        return guessChar(guess, word, guessedCharacters)
    else:
        print("Je moet wel een letter of woord gokken")
        return 0

def main():
    argsWord = wordFromArgs()
    print("Welkom bij galgje!")
    allWords = list()
    if not argsWord:
        allWords = createWordList()

    # hoofdgedeelte
    word = argsWord or random.choice(allWords).lower()
    moves = len(character.character)
    guessedCharacters = set()
    print(f"Ik heb een woord in gedachten van {len(word)} letters", end="\n"*2)
    print(word)

    while moves > 0:
        if checkIfWon(word, guessedCharacters):
            endSequence(word, True)
            break

        print(f"\t{formatWord(word, guessedCharacters)}\nJe kunt nog {moves} keer raden")
        # print alleen je geraden letters als je meer dan 0 letters geraden hebt
        if len(guessedCharacters) > 0: print(f"De dingen die je al geraden hebt zijn: {', '.join(guessedCharacters)}")
        print(character.character[::-1][moves - 1]) # print het juiste poppetje uit character.py
        guess = input("Raad een letter of woord: ").lower()
        print("\n"*2) # witregels
        moves += guessHandler(guess, word, moves, guessedCharacters)
        guessedCharacters.add(guess)
    if not checkIfWon(word, guessedCharacters):
        endSequence(word, False)

if __name__ == "__main__":
    main()
