############################################################
# Section 1: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [i for j in seqs for i in j]

def transpose(matrix):
    result = []
    for j in range(len(matrix[0])):
        result.append([matrix[i][j] for i in range(len(matrix))])
    return result

############################################################
# Section 2: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 3: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]

def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]

def slices(seq):
    for j in range(len(seq)):
        for i in range(j, len(seq)):
            yield seq[j:i + 1]

############################################################
# Section 4: Text Processing
############################################################

def normalize(text):
    return " ".join(text.lower().split())

def no_vowels(text):
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    for i in vowels:
        text = text.replace(i, "")
    return text

def digits_to_words(text):
    digits = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine"
    }
    result = [digits[i] for i in text if i in digits]
    return " ".join(result)

def to_mixed_case(name):
    result = [i.lower().capitalize() for i in name.split("_")]
    result = "".join(result)
    if (len(result) > 0):
        return result[0].lower() + result[1:]
    return ""

############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = polynomial

    def get_polynomial(self):
        return tuple(self.polynomial)

    def __neg__(self):
        return Polynomial([(-i, j) for i, j in self.get_polynomial()])

    def __add__(self, other):
        return Polynomial(self.get_polynomial() + other.get_polynomial())

    def __sub__(self, other):
        other = -other
        return Polynomial(self.get_polynomial() + other.get_polynomial())

    def __mul__(self, other):
        return Polynomial([(i * k, j + l) for i, j in self.get_polynomial() for k, l in other.get_polynomial()])

    def __call__(self, x):
        return sum([i * (x ** j) for i, j in self.get_polynomial()])

    def simplify(self):
        list_len = 0
        for _, j in self.get_polynomial():
            if (list_len < j):
                list_len = j
        poly = [0 for i in range(list_len + 1)]
        for k in range(len(poly)):
            for i, j in self.get_polynomial():
                if (k == j):
                    poly[k] += i
        result = [(poly[i], i) for i in range(len(poly)) if poly[i] != 0][::-1]
        if (len(result) == 0):
            result = [(0, 0)]
        self.polynomial = result

    def __str__(self):
        if (len(self.polynomial) == 0):
            return ""
        result = ""
        for i, j in self.polynomial:
            if (i >= 0):
                if (i == 1 and j != 0):
                    i = ""
                if (j > 1):
                    result += " + " + str(i) + "x^" + str(j)
                elif (j == 1):
                    result += " + " + str(i) + "x"
                else:
                    result += " + " + str(i) + ""
            else:
                if (i == -1 and j != 0):
                    i = ""
                if (j > 1):
                    result += " - " + str(i)[1:] + "x^" + str(j)
                elif (j == 1):
                    result += " - " + str(i)[1:] + "x"
                else:
                    result += " - " + str(i)[1:] + ""
        if (result[1] == "+"):
            return  result[3:]
        return  result[1] + result[3:]

############################################################
# Section 6: Python Packages
############################################################
import numpy as np
def sort_array(list_of_matrices):
    list_of_matrices = np.concatenate((list_of_matrices), axis=None)
    result = []
    for j in list_of_matrices:
        if (type(j) == np.ndarray or type(j) == list):
            j == j.flatten()
            for i in j:
                result.append(i)
        else:
            result.append(j)
    return np.sort(result)[::-1]

import nltk
def POS_tag(sentence):
    sentence = sentence.lower()
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(sentence)
    stop_words = nltk.corpus.stopwords.words("english")
    result = [i for i in new_words if i not in stop_words]
    result = " ".join(result)
    return nltk.pos_tag(nltk.tokenize.word_tokenize(result))