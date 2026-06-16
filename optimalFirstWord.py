from optimalWord import WordleCalculator

if __name__ == "__main__":
    possibleWords = []
    with open("data/answers.txt") as f:
        for word in f:
            possibleWords.append(word.strip())

    calc = WordleCalculator()

    expectedInformation = {}
    with open("acceptedWords.txt") as f:
        for word in f:
            word = word.strip()
            expectedInformation[word] = calc.calculateEV(possibleWords, word)

    with open("expectedValue.txt", "w") as f:
        for word, ev in sorted(expectedInformation.items(), key=lambda p: p[1], reverse=True):
            print(f"{word} {ev:.4f}", file=f)
