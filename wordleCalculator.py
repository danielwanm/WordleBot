import math
import numpy as np
from collections import Counter
class WordleCalculator:
    def __init__(self):
        self.possibleGuesses = [w.strip() for w in open("data/Input/acceptedWords.txt")]
        self.possibleAnswers = [w.strip() for w in open("data/Input/answers.txt")]
        self.guess_idx = {w: i for i, w in enumerate(self.possibleGuesses)}   # row lookup
        self.answer_idx = {w: i for i, w in enumerate(self.possibleAnswers)}  # column lookup
        self.feedBackMatrix = np.load("data/feedbackMatrix.npy")



    # Returns the guess which gives the most expected information
    def calculateOptimalWord(self, possibleWords):
        if (len(possibleWords) <= 2):
            return possibleWords[0]
        expectedInformation = {}
        for word in self.possibleGuesses:
            word = word.strip()
            expectedInformation[word] = self.calculateEV(possibleWords, word)
        return max(expectedInformation, key=expectedInformation.get)




    # calculates the expected number of bits revealed for a potential guess given the set of possible words
    def calculateEV(self, possibleWords, word):
        buckets = Counter(self.feedback(word, answer) for answer in possibleWords)
        n = len(possibleWords)
        return sum((count / n) * math.log2(n / count) for count in buckets.values())




    # returns the 5 color long feedback for a  potential guess based on what the answer is
    def feedback(self, guess, answer):
        code = self.feedBackMatrix[self.guess_idx[guess], self.answer_idx[answer]]
        return code
    
    @staticmethod
    def decode(code):
        return "".join(str((int(code) // 3 ** i) % 3) for i in range(5))
    
    # returns the new set of possible words after a real guess
    def getListOfWordsSatisfyingX(self, x, word, possibleWords):
        x = [int(c) for c in x]
        greens = {}                 # position -> required letter
        not_at = []                 # (position, letter) forbidden at that spot
        min_count = Counter()       # letter -> minimum occurrences in answer
        exact_cap = {}              # letter -> max occurrences (set when a grey appears)


        # set up filter based on x (feedback)
        for i in range(5):
            letter, color = word[i], x[i]
            if color == 2:          
                greens[i] = letter
                min_count[letter] += 1
            elif color == 1:        
                not_at.append((i, letter))
                min_count[letter] += 1
            else:                   
                not_at.append((i, letter))

        for i in range(5):          
            if x[i] == 0:
                exact_cap[word[i]] = min_count[word[i]]

        # run through filter
        adheredToX = []
        for line in possibleWords:
            candidate = line.strip()
            if any(candidate[i] != l for i, l in greens.items()):
                continue
            if any(candidate[i] == l for i, l in not_at):
                continue
            counts = Counter(candidate)
            if any(counts[l] < c for l, c in min_count.items()):
                continue
            if any(counts[l] > cap for l, cap in exact_cap.items()):
                continue
            adheredToX.append(candidate)
        return adheredToX