import random

import numpy
import pygame as pygame
from settings import *
from agent import Agent


def scan(x, y, z):

    if sc.get_at((int(cell[0]), int(cell[1]))) == BLUE:
        env[x] = 1
    if sc.get_at((int(cell[0]), int(cell[1]))) == RED:
        env[y] = 1
    if sc.get_at((int(cell[0]), int(cell[1]))) == GREEN:
        env[z] = 1


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
red = []
blue = []
grass = []
born_predators = 0
born_preys = 0
grass_count = 0
k = 10

for i in range(ANIMALS_COUNT):
    rand_x = random.randint(k * TILE, WIDTH - k * TILE)
    rand_y = random.randint(k * TILE, HEIGHT - k * TILE)
    rand_x = rand_x - rand_x % TILE
    rand_y = rand_y - rand_y % TILE
    red.append(Agent(rand_x, rand_y, RED))

for i in range(ANIMALS_COUNT*5):
    rand_x = random.randint(k * TILE, WIDTH - k * TILE)
    rand_y = random.randint(k * TILE, HEIGHT - k * TILE)
    rand_x = rand_x - rand_x % TILE
    rand_y = rand_y - rand_y % TILE
    blue.append(Agent(rand_x, rand_y, BLUE))
for i in range(GRASS_COUNT):
    rand_x = random.randint(k * TILE, WIDTH - k * TILE)
    rand_y = random.randint(k * TILE, HEIGHT - k * TILE)
    rand_x = rand_x - rand_x % TILE
    rand_y = rand_y - rand_y % TILE
    grass.append((rand_x, rand_y))

while True:
    grass_count += 1
    if grass_count == 1:
        rand_x = random.randint(k * TILE, WIDTH - k * TILE)
        rand_y = random.randint(k * TILE, HEIGHT - k * TILE)
        rand_x = rand_x - rand_x % TILE
        rand_y = rand_y - rand_y % TILE
        grass.append((rand_x, rand_y))
        grass_count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.fill(WHITE)
    for gr in grass:
        pygame.draw.rect(sc, GREEN, (gr[0], gr[1], TILE, TILE))
    for agent in red + blue:
        env = numpy.zeros(12)

        pygame.draw.rect(sc, agent.color, agent.pos)
        for cell in agent.front:
            # pygame.draw.rect(sc, YELLOW, (*cell, TILE, TILE))
            scan(0, 1, 2)
        for cell in agent.left:
            # pygame.draw.rect(sc, PURPLE, (*cell, TILE, TILE))
            scan(3, 4, 5)
        for cell in agent.right:
            # pygame.draw.rect(sc, PURPLE, (*cell, TILE, TILE))
            scan(6, 7, 8)
        for cell in agent.close:
            # pygame.draw.rect(sc, SANDY, (*cell, TILE, TILE))
            scan(9, 10, 11)
        agent.fit(env)

    for agent in red + blue:
        pred = agent.predict()
        action = pred.argmax()
        agent.movement(pred)
        if action == 3:
            if agent.color == BLUE:
                for cell in agent.all_cells:
                    coords = (int(cell[0]), int(cell[1]))
                    c = sc.get_at(coords)
                    if sc.get_at(coords) == GREEN and coords in grass:
                        grass.remove(coords)
                        agent.hp += 1
                if agent.hp == 5:
                    new_agent = Agent(agent.x + TILE, agent.y + TILE, agent.color)
                    new_agent.neurons = agent.neurons

                    for n in new_agent.neurons:
                        r = numpy.random.exponential(0.5)
                        if r < MUTATION_K:
                            idx = random.randint(0, len(n.w)-1)
                            p = random.randint(1, 2)
                            n.w[idx] += pow(-1, p) * n.w[idx] * 0.2

                    blue.append(new_agent)
                    agent.hp = 0
                    born_preys += 1

            if agent.color == RED:
                for cell in agent.all_cells:
                    coords = (int(cell[0]), int(cell[1]))
                    c = sc.get_at(coords)
                    if sc.get_at(coords) == BLUE:
                        for a in blue:
                            if (int(a.x), int(a.y)) == coords:
                                blue.remove(a)
                                agent.hp += 1

                if agent.hp == 1:
                    new_agent = Agent(agent.x + TILE, agent.y + TILE, agent.color)
                    new_agent.neurons = agent.neurons
                    for n in new_agent.neurons:
                        r = numpy.random.exponential(3)
                        if r < MUTATION_K:

                            idx = random.randint(0, len(n.w) - 1)
                            p = random.randint(1, 2)
                            n.w[idx] += pow(-1, p) * n.w[idx] * 0.2

                    red.append(new_agent)
                    agent.hp = 0
                    born_predators += 1

    font = pygame.font.SysFont('couriernew', 20)
    text = font.render("blue = " + str(len(blue)), True, BLACK)
    sc.blit(text, (10, 10))
    text = font.render("red = " + str(len(red)), True, BLACK)
    sc.blit(text, (150, 10))
    text = font.render("grass = " + str(len(grass)), True, BLACK)
    sc.blit(text, (280, 10))
    text = font.render("born red = " + str(born_predators), True, BLACK)
    sc.blit(text, (440, 10))
    text = font.render("born blue = " + str(born_preys), True, BLACK)
    sc.blit(text, (600, 10))
    pygame.display.flip()
    clock.tick(FPS)
