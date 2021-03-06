import numpy as np
from random import randint, choice, random
from tools import sigmoid

# объявляем переменные
TARGET = np.array([0, 0, 1, 1])
GENERATION_NUM = 1000
POPULATION_NUM = 200
MUTATION_RATE = 0.01
INPUTS = np.array([
    [0, 1, 0],
    [0, 1, 1],
    [1, 1, 0],
    [1, 1, 1]
])
matting_pool = []
population = []

# создаём первую популяцию
for _ in range(POPULATION_NUM):
    population.append({
        'genes': 2 * np.random.rand(3) - 1,
        'fitness': 0.0
    })

# оцениваем пригодность
for p in population:
    error = 0

    for x, y in zip(INPUTS, TARGET):
        predict_y = sigmoid(np.dot(x, p['genes']))
        error += abs(y - predict_y)
    p['fitness'] = 1 / (error / 4)

# тренируем популяции
for generation in range(GENERATION_NUM):
    # подготавливаем набор для скрещиванию
    for p in population:
        for _ in range(int(p['fitness'])):
            matting_pool.append(p)

    # скрещивание
    for idx in range(len(population)):
        # выбираем случайных родителей
        parent_a = choice(matting_pool)
        parent_b = None

        while not parent_b and parent_a != parent_b:
            parent_b = choice(matting_pool)

        # crossover
        midpoint = randint(0, len(parent_a['genes']))
        child = {
            'genes': 2 * np.random.rand(3) - 1,
            'fitness': 0.0
        }

        for i in range(len(parent_a['genes'])):
            if i > midpoint:
                child['genes'][i] = parent_a['genes'][i]
            else:
                child['genes'][i] = parent_b['genes'][i]

        # mutations
        for i in range(len(child['genes'])):
            if MUTATION_RATE > random():
                child['genes'][i] = 2 * np.random.rand(1) - 1

        # оцениваем пригодность новой особи
        error = 0
        for x, y in zip(INPUTS, TARGET):
            predict_y = sigmoid(np.dot(x, child['genes']))
            error += abs(y - predict_y)

        child['fitness'] = 1 / (error / 4)

        population[idx] = child

for p in population:

    for x, y in zip(INPUTS, TARGET):
        predict_y = sigmoid(np.dot(x, p['genes']))

        print(predict_y, y)

    print('-' * 25)
