#Rank System in game

RANKS = [
    ("FRESHMAN", 1, 5),
    ("SOPHOMORE", 6, 10),
    ("JUNIOR", 11, 15),
    ("SENIOR", 16, 20),
    ("GRADUATE", 21, 25) 
]

def get_academic_rank(level):
    for name, min_level, max_level in RANKS:
        if min_level <= level <= max_level:
            return name

    if level > 25:
        return RANKS[-1][0]

    return RANKS[0][0]

def get_unlocked_rank_count(level):
    return sum(
        1 for name, min_level, max_level in RANKS
        if level >= min_level
    )

def get_rank_status(level, min_level, max_level):
    if min_level <= level <= max_level:
        return "CURRENT"

    if level > max_level:
        return "UNLOCKED"

    return "LOCKED"