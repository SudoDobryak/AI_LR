import math
import random

import numpy
import numpy as np
import pygame

from settings import *


class Neuron:
    def __init__(self, environment):
        self.environment = environment
        self.w = np.random.randint(0,100,len(environment))

    def out(self):
        return sum(self.w * self.environment) + random.randint(1, 10)


class Agent:
    def __init__(self, x, y, color):
        self.hidden = []
        for i in range(12):
            self.hidden.append(Neuron(numpy.zeros(12)))
        self.neurons = []
        for i in range(4):
            self.neurons.append(Neuron(numpy.zeros(12)))
        self.x = x
        self.y = y
        self.hp = 0
        self.color = color
        self.angle = 270

        self.close = [
            [self.x + TILE, self.y],
            [self.x - TILE, self.y],
            [self.x, self.y - TILE],
            [self.x - TILE, self.y - TILE],
            [self.x + TILE, self.y - TILE]
        ]

        self.left = [
            [self.x - 2 * TILE, self.y],
            [self.x - 2 * TILE, self.y - TILE]
        ]

        self.right = [
            [self.x + 2 * TILE, self.y],
            [self.x + 2 * TILE, self.y - TILE],
        ]

        self.front = [
            [self.x - 2 * TILE, self.y - 2 * TILE],
            [self.x - 1 * TILE, self.y - 2 * TILE],
            [self.x, self.y - 2 * TILE],
            [self.x + 1 * TILE, self.y - 2 * TILE],
            [self.x + 2 * TILE, self.y - 2 * TILE],
        ]

    @property
    def pos(self):
        return self.x, self.y, TILE, TILE

    @property
    def ang(self):
        return self.angle % 360

    @property
    def all_cells(self):
        return self.close + self.left + self.right + self.front

    def movement(self, actions):
        action = actions.argmax()
        sin_a = math.sin(self.ang * math.pi / 180)
        cos_a = math.cos(self.ang * math.pi / 180)

        if action == 0:
            self.angle -= 90
            for cell in self.all_cells:
                self.rotate(cell, -90)

        if action == 1:
            self.angle += 90
            for cell in self.all_cells:
                self.rotate(cell, 90)

        if action == 2:
            self.x += TILE * cos_a
            self.y += TILE * sin_a
            self.x = round(self.x)
            self.y = round(self.y)
            for cell in self.all_cells:
                cell[0] += TILE * cos_a
                cell[1] += TILE * sin_a
            self.tor(cell)

    def tor(self, cell):
        over_border = False
        if cell[0] <= 0:
            self.x = WIDTH - 3 * TILE
            over_border = True
        if cell[0] >= WIDTH:
            self.x = + 3 * TILE
            over_border = True
        if cell[1] <= 0:
            self.y = HEIGHT - 3 * TILE
            over_border = True
        if cell[1] >= HEIGHT:
            self.y = + 3 * TILE
            over_border = True

        if over_border:
            self.angle = 270
            self.close = [
                [self.x + TILE, self.y],
                [self.x - TILE, self.y],
                [self.x, self.y - TILE],
                [self.x - TILE, self.y - TILE],
                [self.x + TILE, self.y - TILE]
            ]

            self.left = [
                [self.x - 2 * TILE, self.y],
                [self.x - 2 * TILE, self.y - TILE]
            ]

            self.right = [
                [self.x + 2 * TILE, self.y],
                [self.x + 2 * TILE, self.y - TILE],
            ]

            self.front = [
                [self.x - 2 * TILE, self.y - 2 * TILE],
                [self.x - 1 * TILE, self.y - 2 * TILE],
                [self.x, self.y - 2 * TILE],
                [self.x + 1 * TILE, self.y - 2 * TILE],
                [self.x + 2 * TILE, self.y - 2 * TILE],
            ]

    def rotate(self, point, angle):
        pos = self.pos
        old_x = point[0] - pos[0]
        old_y = point[1] - pos[1]
        point[0] = (old_x * math.cos(angle * math.pi / 180) - old_y * math.sin(angle * math.pi / 180)) + pos[0]
        point[1] = (old_x * math.sin(angle * math.pi / 180) + old_y * math.cos(angle * math.pi / 180)) + pos[1]
        self.tor(point)

    def fit(self, env):
        # for neuron in self.neurons:
        #     neuron.environment = env
        hidden_result = []
        for neuron in self.hidden:
            neuron.environment = env

    def predict(self):
        result = []
        hidden_result = []
        for neuron in self.hidden:
            hidden_result.append(neuron.out())

        for neuron in self.neurons:
            neuron.environment = hidden_result

        for neuron in self.neurons:
            result.append(neuron.out())

        return np.asarray(result)
