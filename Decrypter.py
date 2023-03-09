import random
import math
from colored import fg, attr


def calcScore(text, quadgrams):
    """Calculates the fitness of the given text"""
    text = "".join(text)
    score = 0
    quads = quadgrams.__getitem__
    for i in range(len(text) - 3):
        if text[i : i + 4] in quadgrams:
            score += quads(text[i : i + 4])
        else:
            score += floor
    return score


quadgrams = {}
for line in open("english_quadgrams.txt"):
    quad, num = line.split(" ")
    quadgrams[quad] = int(num)

n = sum(quadgrams.values())
for quad in quadgrams.keys():
    quadgrams[quad] = math.log10(float(quadgrams[quad] / n))
floor = math.log10(0.01 / n)

OriginalText = input("Enter crypted text:\n")
text = OriginalText.upper()

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
bestKey = alphabet[:]

specialChars = []
count = 0
for char in text:
    if char not in alphabet:
        specialChars.append((char, text.index(char) + count))
        text = text.replace(char, "", 1)
        count += 1

initialScore = calcScore(list(text), quadgrams)
validScore = None
finalScore = -99e9

random.shuffle(bestKey)
parentKey, parentScore, parentGuess = bestKey[:], finalScore, []

reset = fg(15) + attr(0)
noChanges = 0
currentGen = 0
while 1:
    currentGen += 1
    for char in text:
        idx = alphabet.index(char)
        parentGuess.append(parentKey[idx])
    parentScore = calcScore(parentGuess, quadgrams)

    count = 0
    while count < 100:
        a = random.randint(0, len(alphabet) - 1)
        b = random.randint(0, len(alphabet) - 1)

        childKey, childGuess = parentKey[:], []
        childKey[a], childKey[b] = childKey[b], childKey[a]

        for char in text:
            idx = alphabet.index(char)
            childGuess.append(childKey[idx])
        childScore = calcScore(childGuess, quadgrams)

        if childScore > parentScore:
            parentScore, parentKey, parentGuess = (
                childScore,
                childKey[:],
                childGuess[:],
            )
            count = 0
        count += 1

    if parentScore > finalScore:
        bestGen, finalScore, bestKey, bestGuess = (
            currentGen,
            parentScore,
            parentKey[:],
            parentGuess[:],
        )

    if finalScore == validScore:
        noChanges += 1
        if noChanges == 100:
            break
    else:
        noChanges = 0

    validScore = finalScore

    print(
        f"\nCurrent generation: {fg(4)}{attr(1)}{currentGen}{reset} - Score: {fg(1)}{attr(1)}{finalScore}{reset}"
    )
    print(f"Guessed text: {fg(243)}{attr(1)}{''.join(bestGuess)}{reset}")

for char in specialChars:
    sC, idx = char
    bestGuess.insert(idx, sC)

for i in range(len(OriginalText)):
    if not OriginalText[i].isupper():
        bestGuess[i] = bestGuess[i].lower()

bestGuess = "".join(bestGuess)
maxScore = finalScore - initialScore

print(
    f"\n\nDecrypted in Generation {fg(2)}{attr(1)}{bestGen}{reset} with a Fitness Score increase of {fg(2)}{attr(1)}{maxScore}{reset} points"
)
print(
    f"    Initial Score: {fg(208)}{initialScore}{reset} - Final Score: {fg(3)}{finalScore}{reset}"
)
print(
    f"    Key: {fg(4)}{''.join(alphabet)}{reset}\n         ˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅\n         {fg(6)}{attr(1)}{''.join(bestKey)}{reset}"
)
print(f"      Crypted text: {fg(1)}{OriginalText}{reset}")
print(f"    Decrypted text: {fg(2)}{bestGuess}{reset}")
