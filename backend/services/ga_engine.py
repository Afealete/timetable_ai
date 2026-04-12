import random
import json
import os
from services.fitness_service import fitness
from services.database_service import get_lecturers_data, get_rooms_data, get_timeslots_data

POP_SIZE = 100
GENERATIONS = 200
MUTATION_RATE = 0.1

# Load data from database
ROOMS = get_rooms_data()
TIMESLOTS = get_timeslots_data()
LECTURERS = get_lecturers_data()

NUM_TIMESLOTS = len(TIMESLOTS)

def get_available_rooms(students):
    return [room for room in ROOMS if room['capacity'] >= students]

def create_individual(df):
    individual = []
    for _, row in df.iterrows():
        available_rooms = get_available_rooms(row["students"])
        if available_rooms:
            room = random.choice(available_rooms)['id']
        else:
            room = None  # No suitable room available
        gene = (
            row["course"],
            row["lecturer"],
            room,
            random.randint(0, NUM_TIMESLOTS - 1),  # Timeslot index
            row["group"],
            row["capacity"],
            row["students"]
        )
        individual.append(gene)
    return individual

def create_population(df):
    return [create_individual(df) for _ in range(POP_SIZE)]

def select(population):
    population.sort(key=lambda x: fitness(x))
    return population[:20]

def crossover(p1, p2):
    point = random.randint(0, len(p1)-1)
    return p1[:point] + p2[point:]

def mutate(individual):
    if random.random() < MUTATION_RATE:
        i = random.randint(0, len(individual)-1)
        gene = list(individual[i])
        # Mutate timeslot
        gene[3] = random.randint(0, NUM_TIMESLOTS - 1)
        # Mutate room
        available_rooms = get_available_rooms(gene[6])  # students
        if available_rooms:
            gene[2] = random.choice(available_rooms)['id']
        individual[i] = tuple(gene)
    return individual

def run_ga(df):
    population = create_population(df)

    for _ in range(GENERATIONS):
        selected = select(population)

        new_pop = []
        for _ in range(POP_SIZE):
            p1, p2 = random.sample(selected, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)

        population = new_pop

    best = min(population, key=lambda x: fitness(x))
    return best