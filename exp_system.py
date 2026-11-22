#The EXP SystEXP_PER_LEVEL = 100

EXP_PER_LEVEL = 100

def award_exp(app, amount):
    old_level = app.level

    app.exp += amount

    while app.exp >= EXP_PER_LEVEL:
        app.exp -= EXP_PER_LEVEL
        app.level += 1

    return old_level, app.level
