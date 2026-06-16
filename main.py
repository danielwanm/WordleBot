from wordleCalculator import WordleCalculator

if __name__ == "__main__":
    possibleWords = []
    with open("data/Input/answers.txt") as f:
        for word in f:
            word = word.strip()
            possibleWords.append(word)

    calc = WordleCalculator()

    print("Guess: tares")
    currentGuess = "tares"
    print("Write the colors that we got with grey = 0, yellow = 1 and green = 2, ie for 🟩⬜️🟨⬜️🟨 type: 20101")
    x = input("Answer: ")
    possibleWords = calc.getListOfWordsSatisfyingX(x, currentGuess, possibleWords)
    print(f"The following words are still possible: {possibleWords}")

    while len(possibleWords) > 0:
        if len(possibleWords) == 1:
            print(f"This should be correct!: {possibleWords[0]}")
            break
        currentGuess = calc.calculateOptimalWord(possibleWords)
        print(f"Guess: {currentGuess}")
        x = input("Answer: ")    
        possibleWords = calc.getListOfWordsSatisfyingX(x, currentGuess, possibleWords)
        print(f"The following words are still possible: {possibleWords}")


        
        
