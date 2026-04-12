import random
from services.fitness import fitness

# GA PARAMETERS - OPTIMIZED
POP_SIZE = 200  # Increased from 50
GENERATIONS = 300  # Increased from 100
ELITE_SIZE = 20  # Increased from 10 (10% of population)
TOURNAMENT_SIZE = 7  # Increased from 5 for better selection
MUTATION_RATE = 0.15  # Reduced from 0.2 for stability

# TIMETABLE STRUCTURE
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

PERIODS = [
    "08:00-10:00",
    "10:00-12:00",
    "12:00-14:00",
    "14:00-16:00"
]


# 🧬 CREATE ONE TIMETABLE (INDIVIDUAL)
def create_individual(df):
    individual = []

    for _, row in df.iterrows():
        gene = {
            "course": row.get("course"),
            "lecturer": row.get("lecturer"),
            "room": row.get("room"),
            "day": random.choice(DAYS),
            "period": random.choice(PERIODS),
            "group": row.get("group", "default"),
            "capacity": row.get("capacity", 100),
            "students": row.get("students", 50)
        }
        individual.append(gene)

    return individual


# 👥 INITIAL POPULATION
def create_population(df):
    return [create_individual(df) for _ in range(POP_SIZE)]


# 🧬 CROSSOVER (COMBINE TWO TIMETABLES)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child


# 🔁 MUTATION (SMART VERSION)
def mutate(individual):
    for i, gene in enumerate(individual):
        if random.random() < MUTATION_RATE:
            # 70% chance to mutate time, 30% chance to mutate both
            if random.random() < 0.7:
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(PERIODS)
            else:
                # Full reassignment for stuck solutions
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(PERIODS)
                gene["room"] = f"Room{random.randint(1, 10)}"  # More room variety
    return individual

# 🔄 ADAPTIVE MUTATION
def mutate_adaptive(individual, mutation_rate):
    for i, gene in enumerate(individual):
        if random.random() < mutation_rate:
            # Intelligent mutation based on problem constraints
            if random.random() < 0.6:
                # Time slot mutation
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(PERIODS)
            elif random.random() < 0.8:
                # Room mutation
                gene["room"] = f"Room{random.randint(1, 10)}"
            else:
                # Full mutation for diversity
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(PERIODS)
                gene["room"] = f"Room{random.randint(1, 10)}"
    return individual


# 🏆 TOURNAMENT SELECTION (BETTER THAN RANDOM)
def select(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    return min(tournament, key=lambda x: fitness(x))


# 🚀 MAIN GA LOOP - ENHANCED
def run_ga(df):
    population = create_population(df)
    best_fitness_history = []
    stagnation_counter = 0
    last_best_fitness = float('inf')

    for generation in range(GENERATIONS):
        # Sort by fitness (lower is better)
        population = sorted(population, key=lambda x: fitness(x))
        current_best = fitness(population[0])
        best_fitness_history.append(current_best)

        # Adaptive mutation and stagnation detection
        if current_best == last_best_fitness:
            stagnation_counter += 1
        else:
            stagnation_counter = 0
            last_best_fitness = current_best

        # If stagnated for 20 generations, increase mutation rate temporarily
        current_mutation_rate = MUTATION_RATE
        if stagnation_counter > 20:
            current_mutation_rate = min(MUTATION_RATE * 2, 0.5)  # Cap at 50%

        # Elitism (keep best solutions)
        next_gen = population[:ELITE_SIZE]

        # Generate rest of population
        while len(next_gen) < POP_SIZE:
            parent1 = select(population)
            parent2 = select(population)

            child = crossover(parent1, parent2)
            child = mutate_adaptive(child, current_mutation_rate)

            next_gen.append(child)

        population = next_gen

        # Progress reporting
        if generation % 20 == 0:
            print(f"Generation {generation}, Best Fitness: {current_best}, Stagnation: {stagnation_counter}")

    # Return best solution
    best = min(population, key=lambda x: fitness(x))
    print(f"\nGA completed. Final best fitness: {fitness(best)}")
    return best