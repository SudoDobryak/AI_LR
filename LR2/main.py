import math
import os

import numpy as np
from PIL import Image

np.random.seed(404)


class Neuron:
    def __init__(self, img):
        self.img = img
        self.w = np.random.rand(900)

    def out(self):
        return self.activation(sum(self.img * self.w))

    def activation(self, out, threshold=0):
        if out > threshold:
            return 1
        else:
            return 0


class Layer:
    def __init__(self, n=33, l=0.1):
        self.neurons = []
        self.n = n
        self.l = l
        for i in range(n):
            self.neurons.append(Neuron(np.zeros(900)))

    def fit(self, img):
        for i in range(self.n):
            self.neurons[i].img = img

    def update_w(self, error):
        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[i].w)):
                self.neurons[i].w[j] += self.l * error[i] * self.neurons[i].img[j]

    def predict(self):
        result = []
        for n in self.neurons:
            result.append(n.out())
        return np.asarray(result)


network = Layer()
for epoch in range(10):
    print(epoch)
    for img in os.listdir("Name/"):
        image = np.array(Image.open("Name/" + img).convert("L"))
        image[image < 255] = 1
        image[image == 255] = 0
        network.fit(image.flatten())
        pred = network.predict()
        target = np.zeros(33)
        target[ord(img[0]) - 1040] = 1
        print()
        print("target= " + chr(target.argmax() + 1040))
        print(target)
        print(len(target))
        print("prediction= " + chr(pred.argmax() + 1040))
        print(pred)
        print(len(pred))
        error = target - pred
        network.update_w(error)

print()
image = np.array(Image.open("Test.png").convert("L"))
image[image < 255] = 1
image[image == 255] = 0
network.fit(image.flatten())
p = network.predict()
print("prediction= " + chr(p.argmax() + 1040))
