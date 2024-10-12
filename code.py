import numpy as np
import string
import random

# File paths --------------- Need to be fixed for user
bigramPath = "supp/bigram.txt"
encryptedPath = "supp/testInput.txt"

# Read in bigram frequency and populate a 26x26 matrix
alphabet = string.ascii_lowercase
with open(bigramPath, 'r') as file:
    bigramMatrix = np.full((26, 26), 1e-8)
    for line in file:
        bigram, frequency = line.strip().split(',')
        frequency = float(frequency.strip().replace('%', '')) / 100  # Convert percentage to fraction
        row = alphabet.index(bigram[0])
        column = alphabet.index(bigram[1])
        bigramMatrix[row][column] = frequency

# Read in encrypted data
def readEncryptedFile(encryptedPath):
    with open(encryptedPath, 'r') as file:
        return file.read().strip()
encryptedMessage = readEncryptedFile(encryptedPath)

# Filter out non-alphabet characters
def filterMessage(message, alphabet):
    return ''.join(char for char in message if char in alphabet)

# initialize mapping f as the identity
def function(alphabet):
    return {letter: letter for letter in alphabet}
f = function(alphabet)

# swaps two letters/maps the key to two different letters
def randomTransposition(f, alphabet):
    fStar = f.copy()
    a, b = random.sample(alphabet, 2)
    fStar[a], fStar[b] = fStar[b], fStar[a]
    return fStar

# Compute plausibility of a mapping
def computePlausibility(f, f_next,  encryptedMessage, bigramMatrix, alphabet):
    plausibility = 1
    filtered_message = filterMessage(encryptedMessage, alphabet)

    for i in range(len(filtered_message) - 1):
        si = filtered_message[i]
        next_si = filtered_message[i + 1]
        decryptedbigram1 = (f[si], f[next_si])
        decryptedbigram2=(f_next[si], f_next[next_si])
        row1 = alphabet.index(decryptedbigram1[0])
        column1 = alphabet.index(decryptedbigram1[1])
        row2 = alphabet.index(decryptedbigram2[0])
        column2 = alphabet.index(decryptedbigram2[1])
        associatedBigramFrequency1 = bigramMatrix[row1][column1]
        associatedBigramFrequency2 = bigramMatrix[row2][column2]
        ratio = associatedBigramFrequency2 / associatedBigramFrequency1
        plausibility *= ratio
        #print(plausibility)
    return plausibility


 # returns final mapping for decryption
def MCMC(f, encryptedMessage, bigramMatrix, alphabet):
    iterations = 10000 # max is 10,000?
    f_i = f
    counter = 0
    for i in range(iterations):
        fi_next = randomTransposition(f_i, alphabet)
        counter += 1
        pl_i = computePlausibility(f_i, fi_next, encryptedMessage, bigramMatrix, alphabet)
        if pl_i > 1:
            f_i = fi_next # accept new f

        else:
            coinFlipProb = pl_i
            if random.random() < coinFlipProb:
                f_i = fi_next

            else:
                f_i = f_i
                pl_i = pl_i

        print("Number of Iterations: ",counter)

    return f_i


key= MCMC(f, encryptedMessage, bigramMatrix, alphabet)

# Decrypts the message using the final mapping
def decryptMessage(key, encryptedMessage):
    decryptedMessage = ''.join(key.get(char, char) for char in encryptedMessage)
    return decryptedMessage

print(key)
decryptedMessage = decryptMessage(key, encryptedMessage)
print(decryptedMessage)
