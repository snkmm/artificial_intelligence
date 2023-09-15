############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math

############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.w = {}
        for iteration in range(iterations):
            for x, y in examples:
                y_hat = self.predict(x)
                if (y_hat != y):
                    for i in x:
                        if (y):
                            self.w[i] = self.w.get(i, 0) + x[i]
                        else:
                            self.w[i] = self.w.get(i, 0) - x[i]

    def predict(self, x):
        return sum([self.w.get(i, 0) * x[i] for i in x]) > 0

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.ys = set(y for _, y in examples)
        self.ws = {l: {} for l in self.ys}
        for iteration in range(iterations):
            for x, y in examples:
                y_hat = self.predict(x)
                if (y_hat != y):
                    for i in x:
                        self.ws[y][i] = self.ws[y].get(i, 0) + x[i]
                        self.ws[y_hat][i] = self.ws[y_hat].get(i, 0) - x[i]

    def predict(self, x):
        argmax = (None, -math.inf)
        for i, ws in self.ws.items():
            temp = sum([ws.get(j, 0) * xj for j, xj in x.items()])
            if (argmax[1] < temp):
                argmax = (i, temp)
        return argmax[0]

############################################################
# Section 2: Applications
############################################################

class IrisClassifier(object):

    def __init__(self, data):
        train = [({i: z for i, z in enumerate(x)}, y) for x, y in data]
        self.c = MulticlassPerceptron(train, 20)

    def classify(self, instance):
        test = {i: z for i, z in enumerate(instance)}
        return self.c.predict(test)

class DigitClassifier(object):

    def __init__(self, data):
        train = [({i: z for i, z in enumerate(x)}, y) for x, y in data]
        self.c = MulticlassPerceptron(train, 10)

    def classify(self, instance):
        test = {i: z for i, z in enumerate(instance)}
        return self.c.predict(test)

class BiasClassifier(object):

    def __init__(self, data):
        train = [({0: x, 1: 1}, y) for x, y in data]
        self.c = BinaryPerceptron(train, 10)

    def classify(self, instance):
        test = {0: instance, 1: 1}
        return self.c.predict(test)

class MysteryClassifier1(object):

    def __init__(self, data):
        train = [({0: pow(x[0], 2) + pow(x[1], 2), 1: 1}, y) for x, y in data]
        self.c = BinaryPerceptron(train, 10)

    def classify(self, instance):
        test = {0: pow(instance[0], 2) + pow(instance[1], 2), 1: 1}
        return self.c.predict(test)

class MysteryClassifier2(object):

    def __init__(self, data):
        train = [({0: x[0] * x[1] * x[2]}, y) for x, y in data]
        self.c = BinaryPerceptron(train, 10)

    def classify(self, instance):
        test = {0: instance[0] * instance[1] * instance[2]}
        return self.c.predict(test)