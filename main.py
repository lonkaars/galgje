import re
import os
import random

def loadWords(): # laad woorden uit de ./words map en voeg ze toe aan een dictionary
    out = dict()
    for filename in os.listdir("./words"):
        if filename.endswith(".txt"):
            out[filename[:-4]] = open(f"./words/{filename}", "r").read().split("\n")
    return out

def wordFilter(word): # laat alleen woorden toe zonder leestekens, en die langer dan 2 letters zijn
    if(len(word) <= 1): return False
    filtered = re.search(r"[0-9\'\"\.\-\s]", word)
    return filtered == None

def getRandomWord(wordList):
    wordList = list(filter(wordFilter, wordList))
    return random.choice(wordList)

def endSequence():
    print("Dat was hem weer jongens")

def formatWord(word, guessed): # maak van een woord en geraden letters een woord met streepjes
    out = ""
    for char in word:
        out += f"{char} " if char in guessed else "_ "
    return out[:-1]


def main():
    print("Welkom bij galgje!\nOp het moment worden alle woorden in words/ geladen:", end="\n"*2)
    wordLists = loadWords()
    print(f"{len(wordLists)} woordenlijst(en) gevonden!", end="\n"*2)
    allWords = list()
    for wordList in wordLists:
        print(f"Lijst {wordList} met {len(wordLists[wordList])} woorden")
        allWords += wordLists[wordList]
    print(f"Er zijn in totaal {len(allWords)} woorden", end="\n"*2)

    # hoofdgedeelte
    word = getRandomWord(allWords).lower()
    moves = 8
    guessedCharacters = set()
    print(f"Ik heb een woord in gedachten van {len(word)} letters", end="\n"*2)
    while moves > 0:
        print(f"\n\t{formatWord(word, guessedCharacters)}\nJe kunt nog {moves} keer raden")
        guess = input("Raad een letter of woord: ").lower()
        if len(guess) > 1:
            # als de gok langer is dan 1 letter is het automatisch een gok voor een woord
            if word == guess:
                endSequence()
                break
            else:
                print("Dat is niet mijn woord!")
        else:
            # gok voor een letter
            if guess in guessedCharacters:
                print(f"De letter {guess} heb je al geraden")
                continue # ga naar de volgende ronde zonder een beurt af te trekken
            else:
                guessedCharacters.add(guess)
                print(f"De letter {guess} zit{' niet' if not guess in word else ''} in mijn woord")
        moves -= 1
    endSequence()

if __name__ == "__main__":
    main()
