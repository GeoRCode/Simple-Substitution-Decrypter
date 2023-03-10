import random
import math
from colored import fg, attr


# Función que calcula el fitness score de cada quadgram
def calcScore(text, quadgrams):
    text = "".join(text)
    score = 0
    quads = quadgrams.__getitem__
    for i in range(len(text) - 3):
        if text[i : i + 4] in quadgrams:
            score += quads(text[i : i + 4])
        else:
            score += floor
    return score

# Se crea diccionario con cada uno de los quadgrams en el inglés y su respectiva frecuencia
quadgrams = {}
for line in open("english_quadgrams.txt"):
    quad, num = line.split(" ")
    quadgrams[quad] = int(num)

# Se calcula la probabilidad logarítmica de cada quadgram
n = sum(quadgrams.values())
for quad in quadgrams.keys():
    quadgrams[quad] = math.log10(float(quadgrams[quad] / n))
floor = math.log10(0.01 / n)

# Se le pide al usuario la frase a desencriptar
OriginalText = input("Enter crypted text:\n")
text = OriginalText.upper()

# Se crea lista con el alfabeto en inglés y la primera clave
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
bestKey = alphabet[:]

# Se explora el texto para encontrar caracteres especiales, estos se extraen y
# se guardan en una lista con su respectivo index
specialChars = []
count = 0
for char in text:
    if char not in alphabet:
        specialChars.append((char, text.index(char) + count))
        text = text.replace(char, "", 1)
        count += 1

# Se asignan los valores iniciales del puntaje de la oración inicial, 
# el puntaje de validación y se le da un valor muy pequeño al
# valor final para hacer una validación adecuada con los puntajes
# obtenidos en cada iteración
initialScore = calcScore(list(text), quadgrams)
validScore = None
finalScore = -99e9

# Valores iniciales del padre para el algoritmo genético
random.shuffle(bestKey)
parentKey, parentScore, parentGuess = bestKey[:], finalScore, []

reset = fg(15) + attr(0)
noChanges = 0
currentGen = 0

# Inicializamos el algoritmo genético
while 1:
    currentGen += 1
    # Se obtiene la clave del padre y el fitness score de su predicción
    for char in text:
        idx = alphabet.index(char)
        parentGuess.append(parentKey[idx])
    parentScore = calcScore(parentGuess, quadgrams)

    count = 0
    # Inicializamos el ciclo para calcular los valores de los hijos
    while count < 100:
        a = random.randint(0, len(alphabet) - 1)
        b = random.randint(0, len(alphabet) - 1)

        childKey, childGuess = parentKey[:], []
        childKey[a], childKey[b] = childKey[b], childKey[a]

        # Se obtiene la clave del hijo y el fitness score de su predicción
        for char in text:
            idx = alphabet.index(char)
            childGuess.append(childKey[idx])
        childScore = calcScore(childGuess, quadgrams)

        # Se evalúa si el puntaje del hijo es mayor al del padre. En caso
        # de ser así, se establece el hijo como nuevo padre el cual empieza
        # de nuevo a generar hijos
        if childScore > parentScore:
            parentScore, parentKey, parentGuess = (
                childScore,
                childKey[:],
                childGuess[:],
            )
            count = 0
        count += 1


    # Se evalúa si el puntaje padre es mayor al valor final. Si esto se cumple, 
    # se establecen los valores del padre como los mejores valores
    if parentScore > finalScore:
        bestGen, finalScore, bestKey, bestGuess = (
            currentGen,
            parentScore,
            parentKey[:],
            parentGuess[:],
        )

    # Se evalúa si es puntaje final es igual al puntaje de validación. En caso 
    # de que se cumpla, se acumula la iteración ya que se define que cuando se
    # cumple esto 100 veces, el mensaje ya fue desencriptado y se rompe el ciclo
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

# Se agregan los caracteres especiales que fueron retirados del mensaje
for char in specialChars:
    sC, idx = char
    bestGuess.insert(idx, sC)

# Se agregan las mayúsculas en las posiciones adecuadas
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
