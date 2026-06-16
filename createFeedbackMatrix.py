import numpy as np
possibleGuesses = [w.strip() for w in open("data/Input/acceptedWords.txt")]
possibleAnswers = [w.strip() for w in open("data/Input/answers.txt")]
guess_idx = {w: i for i, w in enumerate(possibleGuesses)}   # row lookup
answer_idx = {w: i for i, w in enumerate(possibleAnswers)}  # column lookup
feedbackMatrix = np.zeros((len(possibleGuesses), len(possibleAnswers)), dtype=np.uint8)
for guess in possibleGuesses:
    for answer in possibleAnswers:
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


        encodedInt = result[0]+result[1]*3+result[2]*9+result[3]*27+result[4]*81
        feedbackMatrix[guess_idx[guess]][answer_idx[answer]] = encodedInt
np.save("data/feedbackMatrix.npy", feedbackMatrix)
print(f"Saved feedback matrix of shape {feedbackMatrix.shape}")
