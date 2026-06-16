# Back tester for wordle solver
from wordleCalculator import WordleCalculator
FIRST_GUESS = "tares"
class BackTester:
    def __init__(self):
        self.calc = WordleCalculator()
    def runGame(self, answer, possibleWords):
        guess = FIRST_GUESS
        possibleWords = possibleWords
        numGuesses = 0
        while(True):

            numGuesses += 1
            if (guess == answer):
                return numGuesses 
            code = self.calc.feedback(guess, answer)
            x = self.calc.decode(code)
            possibleWords = self.calc.getListOfWordsSatisfyingX(x, guess, possibleWords)
            guess = self.calc.calculateOptimalWord(possibleWords)


    def runBacktester(self):
        possibleWords = []
        with open("data/Input/answers.txt") as f:
            for word in f:
                possibleWords.append(word.strip())

        with open("data/Input/answers.txt") as f:
            with open("data/Output/backTesterData.txt", "w", buffering=1) as f1:
                for line in f:
                    word = line.strip()
                    
                    print(f"testing answer: {word}")
                    print(f"{word}| {self.runGame(word, possibleWords)}", file = f1)
            


if __name__ == "__main__":
    BackTester().runBacktester()
    