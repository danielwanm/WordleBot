import math
from collections import Counter

class OptimalWordCalc:
    def calculateOptimalWord(self, possibleWords):
        expectedInformation = {}
        with open("data/acceptedWords.txt") as f:
            for word in f:
                word = word.strip()
                expectedInformation[word] = self.calculateEV(possibleWords, word)
        return max(expectedInformation, key=expectedInformation.get)

    def calculateEV(self, possibleWords, word):
        buckets = Counter(self.feedback(word, answer) for answer in possibleWords)
        n = len(possibleWords)
        return sum((count / n) * math.log2(n / count) for count in buckets.values())

    def feedback(self, guess, answer):
        result = [0] * 5
        remaining = list(answer)
        for i in range(5):              # greens first
            if guess[i] == remaining[i]:
                result[i] = 2
                remaining[i] = None
        for i in range(5):              # then yellows, count-limited
            if result[i] == 0 and guess[i] in remaining:
                result[i] = 1
                remaining[remaining.index(guess[i])] = None
        return tuple(result)


    def getListOfWordsSatisfyingX(self, x, word, possibleWords):
        x = [int(c) for c in x]
        greens = {}                 # position -> required letter
        not_at = []                 # (position, letter) forbidden at that spot
        min_count = Counter()       # letter -> minimum occurrences in answer
        exact_cap = {}              # letter -> max occurrences (set when a grey appears)

        for i in range(5):
            letter, color = word[i], x[i]
            if color == 2:          # green
                greens[i] = letter
                min_count[letter] += 1
            elif color == 1:        # yellow
                not_at.append((i, letter))
                min_count[letter] += 1
            else:                   # grey
                not_at.append((i, letter))

        for i in range(5):          # a grey tile caps that letter at its green+yellow count
            if x[i] == 0:
                exact_cap[word[i]] = min_count[word[i]]

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