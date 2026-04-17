import random
from services.fitness import fitness
from services.database_service import get_rooms_data, get_timeslots_data

# GA PARAMETERS - BALANCED FOR PERFORMANCE
POP_SIZE = 50  # Reduced from 200 for faster generation
GENERATIONS = 50  # Reduced from 300 for faster generation
ELITE_SIZE = 5  # Reduced proportionally
TOURNAMENT_SIZE = 4  # Reduced for performance
MUTATION_RATE = 0.15  # Reduced from 0.2 for stability

# TIMETABLE STRUCTURE
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def normalize_period_string(period_value):
    if period_value is None:
        return None
    text = str(period_value).strip()
    parts = [p.strip() for p in text.split("-")]
    if len(parts) != 2:
        return text

    def parse_comp(comp):
        cleaned = comp.replace(" ", "").replace(":00", "")
        time_parts = cleaned.split(":")
        try:
            if len(time_parts) == 1:
                hour = int(time_parts[0])
                minute = 0
            else:
                hour = int(time_parts[0])
                minute = int(time_parts[1])
        except ValueError:
            return None
        return hour * 60 + minute

    start = parse_comp(parts[0])
    end = parse_comp(parts[1])
    if start is None or end is None:
        return text

    return f"{start // 60:02d}:{start % 60:02d}-{end // 60:02d}:{end % 60:02d}"


# 🧬 CREATE ONE TIMETABLE (INDIVIDUAL)

def normalize_room(room_value):
    if room_value is None:
        return None
    room_str = str(room_value).strip()
    return room_str if room_str else None


def get_available_rooms(students, rooms):
    return [room for room in rooms if room['capacity'] >= students]


def get_room_choices(row, rooms):
    explicit_room = normalize_room(row.get("room"))
    if explicit_room:
        return [explicit_room]

    available_rooms = get_available_rooms(row.get("students", 0), rooms)
    return [room['id'] for room in available_rooms]


def create_individual(df, rooms, periods):
    individual = []

    for _, row in df.iterrows():
        room_choices = get_room_choices(row, rooms)
        room = random.choice(room_choices) if room_choices else None

        gene = {
            "course": row.get("course"),
            "lecturer": row.get("lecturer"),
            "room": room,
            "day": random.choice(DAYS),
            "period": random.choice(periods),
            "group": row.get("group", "default"),
            "capacity": row.get("capacity", 100),
            "students": row.get("students", 50)
        }
        individual.append(gene)

    return individual


# 👥 INITIAL POPULATION
def create_population(df, rooms, periods):
    return [create_individual(df, rooms, periods) for _ in range(POP_SIZE)]


# 🧬 CROSSOVER (COMBINE TWO TIMETABLES)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child


# 🔁 MUTATION (SMART VERSION)
def mutate(individual, rooms, periods):
    for i, gene in enumerate(individual):
        if random.random() < MUTATION_RATE:
            # 70% chance to mutate time, 30% chance to mutate both
            if random.random() < 0.7:
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(periods)
            else:
                # Full reassignment for stuck solutions
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(periods)
                available_rooms = get_room_choices(gene, rooms)
                if available_rooms:
                    gene["room"] = random.choice(available_rooms)
    return individual

# 🔄 ADAPTIVE MUTATION
def mutate_adaptive(individual, mutation_rate, rooms, periods):
    for i, gene in enumerate(individual):
        if random.random() < mutation_rate:
            # Intelligent mutation based on problem constraints
            if random.random() < 0.6:
                # Time slot mutation
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(periods)
            elif random.random() < 0.8:
                # Room mutation
                available_rooms = get_room_choices(gene, rooms)
                if available_rooms:
                    gene["room"] = random.choice(available_rooms)
            else:
                # Full mutation for diversity
                gene["day"] = random.choice(DAYS)
                gene["period"] = random.choice(periods)
                available_rooms = get_room_choices(gene, rooms)
                if available_rooms:
                    gene["room"] = random.choice(available_rooms)
    return individual


# 🏆 TOURNAMENT SELECTION (BETTER THAN RANDOM)
def select(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    return min(tournament, key=lambda x: fitness(x))


# 🚀 MAIN GA LOOP - ENHANCED
def run_ga(df):
    # Load data within app context
    try:
        rooms = get_rooms_data()
        timeslots = get_timeslots_data()
        
        if not rooms:
            raise ValueError("No rooms found in database. Please add rooms in Data Management.")
        if not timeslots:
            raise ValueError("No timeslots found in database. Please add timeslots in Data Management.")
        
        periods = sorted({
            normalize_period_string(slot["time"])
            for slot in timeslots
            if normalize_period_string(slot["time"])
        })
        
        if not periods:
            raise ValueError("No valid periods could be extracted from timeslots. Check timeslot format.")
        
    except Exception as e:
        raise Exception(f"Failed to load essential data: {str(e)}")

    population = create_population(df, rooms, periods)
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
            child = mutate_adaptive(child, current_mutation_rate, rooms, periods)

            next_gen.append(child)

        population = next_gen

        # Progress reporting
        progress_percent = int((generation + 1) / GENERATIONS * 100)
        if generation % 5 == 0 or generation == GENERATIONS - 1:
            print(f"PROGRESS:{progress_percent}% | Gen {generation + 1}/{GENERATIONS} | Fitness: {current_best:.2f}")

    # Return best solution
    best = min(population, key=lambda x: fitness(x))
    print(f"\nGA completed. Final best fitness: {fitness(best)}")
    return best