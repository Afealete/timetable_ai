def fitness(individual):
    penalty = 0

    lecturer_time = {}
    room_time = {}
    group_time = {}

    for g in individual:
        key1 = (g["lecturer"], g["day"], g["period"])
        key2 = (g["room"], g["day"], g["period"])
        key3 = (g["group"], g["day"], g["period"])

        if key1 in lecturer_time:
            penalty += 100

        if key2 in room_time:
            penalty += 100

        if key3 in group_time:
            penalty += 100

        if g["students"] > g["capacity"]:
            penalty += 100

        lecturer_time[key1] = True
        room_time[key2] = True
        group_time[key3] = True

    return penalty