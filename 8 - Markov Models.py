############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    for i in string.punctuation:
        text = text.replace(i, " " + i + " ")
    return text.split()

def ngrams(n, tokens):
    tokens.append("<END>")
    tokens = (n - 1) * ["<START>"] + tokens
    n_grams = []
    for i in range(n - 1, len(tokens)):
        j = i - (n - 1)
        n_grams.append((tuple(tokens[j:i]), tokens[i]))
    return n_grams

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.n_grams = []

    def update(self, sentence):
        self.n_grams += ngrams(self.n, tokenize(sentence))

    def prob(self, context, token):
        context_count = 0.0
        token_count = 0.0
        for i in self.n_grams:
            if (i[0] == context):
                context_count += 1
                if (i[1] == token):
                    token_count += 1
        if (context_count == 0):
            return 0.0
        return token_count / context_count

    def random_token(self, context):
        T = sorted(set(self.n_grams[i][1] for i in range(len(self.n_grams)) if self.n_grams[i][0] == context))
        P = 0.0
        r = random.random()
        for token in T:
            P += self.prob(context, token)
            if (r < P):
                return token

    def random_text(self, token_count):
        context_reset = tuple((self.n - 1) * ["<START>"])
        context = context_reset
        tokens = []
        for _ in range(token_count):
            token = self.random_token(context)
            if (self.n == 1):
                context = tuple()
            else:
                if (token == "<END>"):
                    context = context_reset
                else:
                    context = context[1:] + (token, )
            tokens.append(token)
        return " ".join(tokens)

    def perplexity(self, sentence):
        n_grams = ngrams(self.n, tokenize(sentence))
        perp_temp = 0.0
        for i in n_grams:
            perp_temp -= math.log(self.prob(i[0], i[1]))
        return math.pow(math.exp(perp_temp), 1.0 / len(n_grams))

def create_ngram_model(n, path):
    m = NgramModel(n)
    f = open(path)
    lines = f.readlines()
    for line in lines:
        m.update(line)
    return m