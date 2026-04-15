from services.constraint_service import check_hard_constraints, check_exam_hard_constraints

def fitness(individual):
    penalty = 0

    # HARD constraints
    penalty += check_hard_constraints(individual)

    # SOFT constraints
    for gene in individual:
        _, _, _, timeslot, _, _, _ = gene

        # Avoid late classes
        if timeslot > 30:
            penalty += 2

    return penalty

def exam_fitness(individual):
    penalty = 0

    # HARD constraints for exams
    penalty += check_exam_hard_constraints(individual)

    # SOFT constraints for exams
    for gene in individual:
        _, _, _, exam_period, _, _ = gene

        # Prefer earlier exam periods
        if exam_period > 10:
            penalty += 1

    return penalty