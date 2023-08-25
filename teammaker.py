import csv
import random
import math
import copy

# load data (from the csv file)
def get_player_data():
    PLAYER_DATA = []
    with open('player_soccer_database.csv', 'r') as player_data:
        reader = csv.DictReader(player_data)
        for row in reader:
            PLAYER_DATA.append(row)
    return PLAYER_DATA

# group player by position (a list of players)
def group_data(data):
    Gk, Def, Mid, For = [], [], [], []
    for player in data:
        pos = player['Position']
        if pos == 'Goalkeeper':
            Gk.append(player)
        elif pos == 'Defender':
            Def.append(player)
        elif pos == 'Midfielder':
            Mid.append(player)
        else:
            For.append(player)
    return Gk, Def, Mid, For

# team building function
def build_team(Gk, Def, Mid, For):
    new_team = [random.choice(Gk)]
    count = 0
    while count < 4:
        p = random.choice(Def)
        if p not in new_team:
            new_team.append(p)
            count += 1
    count = 0
    while count < 4:
        p = random.choice(Mid)
        if p not in new_team:
            new_team.append(p)
            count += 1
    count = 0
    while count < 2:
        p = random.choice(For)
        if p not in new_team:
            new_team.append(p)
            count += 1
    return new_team

# build n number of teams
def generate_teams(size, Gk, Def, Mid, For):
    teams = []
    while len(teams) < size:
        team = build_team(Gk, Def, Mid, For)
        teams.append(team)
    return teams

# evaluate the team
def eval_team(team):
    d_score, o_score, d_app, o_app, d_stats, o_stats = 0, 0, 0, 0, 0, 0

    # Goal Keeper Score
    gk = team[0]
    if int(gk['Appearances']) > 0:
        d_score += math.sqrt(int(gk['Appearances'])) * int(gk['Saves']) / int(gk['Appearances'])
    # Defender Score
    for i in range(1, 5):
        Def = team[i]
        d_stats += int(Def['Tackles']) * int(Def['Tackle success %'][:-1]) / 100
        d_app += int(Def['Appearances'])

    if d_app > 0:
        d_score += math.sqrt(d_app) * d_stats / d_app
    # Midfielder Score
    d_stats, d_app = 0, 0
    for i in range(5, 9):
        Mid = team[i]
        if Mid['Duels won'] != '':
            d_stats += int(Mid['Duels won'])
            d_app += int(Mid['Appearances'])
        o_stats += int(Mid['Passes'])
        o_app += int(Mid['Appearances'])
    if d_app > 0:
        d_score += math.sqrt(d_app) * d_stats / d_app
        o_score += math.sqrt(o_app) * o_stats / o_app
    # Forward Score
    o_stats, o_app = 0, 0
    for i in range(9, 11):
        For = team[i]
        o_stats += int(For['Goals'])
        o_app += int(For['Appearances'])
    if o_app > 0:
        o_score += math.sqrt(o_app) * o_stats / o_app
    return (d_score * o_score) ** (1 / 3)

# evaluate the team (intermediate)
def eval_team_int(team):
    d_score, o_score, d_app, o_app, d_stats, o_stats = 0, 0, 0, 0, 0, 0
    # At least 6 players from England
    # Average Age
    e_count = 0
    total_age, val_age = 0, 0
    for p in team:
        if p['Age'] != '':
            total_age += int(p['Age'])
            val_age += 1
        if p['Nationality'] == 'England':
            e_count += 1
    e_mul = 1 if e_count >= 6 else 0
    avg_age_mul = math.sqrt(30 * (1 / (total_age / val_age)))
    # Goal Keeper Score
    gk = team[0]
    if int(gk['Appearances']) > 0:
        d_score += math.sqrt(int(gk['Appearances'])) * int(gk['Saves']) / int(gk['Appearances'])
    # Defender Score
    for i in range(1, 5):
        Def = team[i]
        d_stats += int(Def['Tackles']) * int(Def['Tackle success %'][:-1]) / 100
        d_app += int(Def['Appearances'])

    if d_app > 0:
        d_score += math.sqrt(d_app) * d_stats / d_app
    # Midfielder Score
    d_stats, d_app = 0, 0
    for i in range(5, 9):
        Mid = team[i]
        if Mid['Duels won'] != '':
            d_stats += int(Mid['Duels won'])
            d_app += int(Mid['Appearances'])
        o_stats += int(Mid['Passes'])
        o_app += int(Mid['Appearances'])
    if d_app > 0:
        d_score += math.sqrt(d_app) * d_stats / d_app
        o_score += math.sqrt(o_app) * o_stats / o_app
    # Forward Score
    o_stats, o_app = 0, 0
    for i in range(9, 11):
        For = team[i]
        o_stats += int(For['Goals'])
        o_app += int(For['Appearances'])
    if o_app > 0:
        o_score += math.sqrt(o_app) * o_stats / o_app
    return e_mul * (avg_age_mul * d_score * o_score) ** (1 / 3)

def print_team(team):
    print(f'Score: {eval_team(team)}')
    for p in team:
        print(f'Name: {p["Name"]}\t Appearances: {p["Appearances"]}\t Saves: {p["Saves"]}\t Tackles: {p["Tackles"]}\t '
              f'Duels won: {p["Duels won"]}\t Passes: {p["Passes"]}\t Goals: {p["Goals"]}')
    print("")

def print_team_int(team):
    print(f'Score: {eval_team_int(team)}')
    for p in team:
        print(
            f'Name: {p["Name"]}\t Nationality: {p["Nationality"]}\t Age: {p["Age"]}\t  Appearances: {p["Appearances"]}\t Saves: {p["Saves"]}\t Tackles: {p["Tackles"]}\t '
            f'Duels won: {p["Duels won"]}\t Passes: {p["Passes"]}\t Goals: {p["Goals"]}')
    print("")

def has_conflict(t1, t2):
    for p in t1:
        if p in t2:
            return True
    return False

def same_members(t1, t2):
    for p in t1:
        if p not in t2:
            return False
    return True

def create_game_set(Gk, Def, Mid, For):
    tmp = build_team(Gk, Def, Mid, For)
    Teams = [copy.deepcopy(tmp)]
    while len(Teams) < 4:
        team = build_team(Gk, Def, Mid, For)
        clear = True
        for t in Teams:
            if has_conflict(t, team):
                clear = False
        if clear:
            Teams.append(copy.deepcopy(team))
    return Teams

def eval_game(t1, t2):
    all_players = t1 + t2
    # Shots on target per game
    total_shoots = 0
    total_app = 0
    s_score = 0
    for p in all_players:
        if p['Shots on target'] != '':
            total_app += int(p['Appearances'])
            total_shoots += int(p['Shots on target'])
    if total_app > 0:
        s_score = total_shoots/total_app

    total_saves = 0
    total_app = 0
    save_score = 0
    for p in all_players:
        if p['Saves'] != '':
            total_app += int(p['Appearances'])
            total_saves += int(p['Saves'])
    if total_app > 0:
        save_score = total_saves / total_app
    exp_g = s_score - save_score

    total_passes = 0
    total_app = 0
    pass_score = 0
    for p in all_players:
        if p['Passes'] != '':
            total_app += int(p['Appearances'])
            total_passes += int(p['Passes'])
    if total_app > 0:
        pass_score = total_passes / total_app

    total_inter = 0
    total_app = 0
    inter_score = 0
    for p in all_players:
        if p['Interceptions'] != '':
            total_app += int(p['Appearances'])
            total_inter += int(p['Interceptions'])
    if total_app > 0:
        inter_score = total_inter / total_app
    exp_p = pass_score - inter_score
    return exp_g + exp_p

def eval_game_set(game_set):
    set_score = 0
    for i in range(3):
        for j in range(i + 1, 4):
            set_score += eval_game(copy.deepcopy(game_set[i]), copy.deepcopy(game_set[j]))
    return set_score

def generate_games(size, Gk, Def, Mid, For):
    game_sets = []
    while len(game_sets) < size:
        new_game_set = create_game_set(Gk, Def, Mid, For)
        game_sets.append(copy.deepcopy(new_game_set))
    return game_sets

def print_game_set(game_set):
    print(f'Score: {eval_game_set(game_set)}')
    for t in range(len(game_set)):
        print(f'Team {t+1}:')
        for p in game_set[t]:
            print(f'Name: {p["Name"]}\t Appearances: {p["Appearances"]}\t Saves: {p["Saves"]}\t Tackles: {p["Tackles"]}\t '
                f'Duels won: {p["Duels won"]}\t Passes: {p["Passes"]}\t Goals: {p["Goals"]}')
        print("")

# Minimal Objective
def get_best_teams(size, num_gen, min_val):
    BEST_TEAMS = []
    GK, DEF, MID, FOR = group_data(get_player_data())
    GENERATION = generate_teams(size, GK, DEF, MID, FOR)
    for _ in range(num_gen):
        # rank the teams
        ranked_teams = []
        for t in GENERATION:
            ranked_teams.append((eval_team(t), t))
        ranked_teams = sorted(ranked_teams, key=lambda x: x[0], reverse=True)
        # get current best team
        if ranked_teams[0][0] > min_val:
            if ranked_teams[0][1] not in BEST_TEAMS:
                BEST_TEAMS.append(copy.deepcopy(ranked_teams[0][1]))
        # get top 10 percent teams for computing next gen
        top_10_percent = ranked_teams[:int(size * 0.1)]
        # new player and team samples
        new_player_samples = []
        new_team_samples = []
        for t in top_10_percent:
            new_team_samples.append(t[1])
            for p in t[1]:
                if p not in new_player_samples:
                    new_player_samples.append(p)
        Gk, Def, Mid, For = group_data(new_player_samples)
        # generate new gen
        GENERATION = []
        # random generation
        GENERATION += generate_teams(int(size * 0.2), Gk, Def, Mid, For)
        # Crossover
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            c = random.randint(1, 9)
            t1 = random.choice(new_team_samples)
            t2 = random.choice(new_team_samples)
            dup = False
            for p in t1[:c]:
                if p in t2[c:]:
                    dup = True
                    break
            if not dup:
                n_t = t1[:c] + t2[c:]
                GENERATION.append(n_t)
                count += 1
        # Mutation
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            t = random.choice(new_team_samples)
            c = random.randint(0, 3)
            mod = False
            if c == 0:
                t[0] = random.choice(GK)
                mod = True
            elif c == 1:
                p = random.choice(DEF)
                if p not in t:
                    t[random.randint(1, 4)] = p
                    mod = True
            elif c == 2:
                p = random.choice(MID)
                if p not in t:
                    t[random.randint(5, 8)] = p
                    mod = True
            elif c == 3:
                p = random.choice(FOR)
                if p not in t:
                    t[random.randint(9, 10)] = p
                    mod = True
            if mod:
                GENERATION.append(t)
                count += 1
    result = sorted(BEST_TEAMS, key=lambda x: eval_team(x), reverse=True)
    return result[0]

# Intermediate Objective
def get_best_teams_int(size, num_gen, min_val):
    BEST_TEAMS = []
    GK, DEF, MID, FOR = group_data(get_player_data())
    GENERATION = generate_teams(size, GK, DEF, MID, FOR)
    for _ in range(num_gen):
        # rank the teams
        ranked_teams = []
        for t in GENERATION:
            ranked_teams.append((eval_team_int(t), t))
        ranked_teams = sorted(ranked_teams, key=lambda x: x[0], reverse=True)
        # get current best team
        if ranked_teams[0][0] > min_val:
            if ranked_teams[0][1] not in BEST_TEAMS:
                BEST_TEAMS.append(copy.deepcopy(ranked_teams[0][1]))
        # get top 10 percent teams for computing next gen
        top_10_percent = ranked_teams[:int(size * 0.1)]
        # new player and team samples
        new_player_samples = []
        new_team_samples = []
        for t in top_10_percent:
            new_team_samples.append(t[1])
            for p in t[1]:
                if p not in new_player_samples:
                    new_player_samples.append(p)
        Gk, Def, Mid, For = group_data(new_player_samples)
        # generate new gen
        GENERATION = []
        # random generation
        GENERATION += generate_teams(int(size * 0.2), Gk, Def, Mid, For)
        # Crossover
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            c = random.randint(1, 9)
            t1 = random.choice(new_team_samples)
            t2 = random.choice(new_team_samples)
            dup = False
            for p in t1[:c]:
                if p in t2[c:]:
                    dup = True
                    break
            if not dup:
                n_t = t1[:c] + t2[c:]
                GENERATION.append(n_t)
                count += 1
        # Mutation
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            t = random.choice(new_team_samples)
            c = random.randint(0, 3)
            mod = False
            if c == 0:
                t[0] = random.choice(GK)
                mod = True
            elif c == 1:
                p = random.choice(DEF)
                if p not in t:
                    t[random.randint(1, 4)] = p
                    mod = True
            elif c == 2:
                p = random.choice(MID)
                if p not in t:
                    t[random.randint(5, 8)] = p
                    mod = True
            elif c == 3:
                p = random.choice(FOR)
                if p not in t:
                    t[random.randint(9, 10)] = p
                    mod = True
            if mod:
                GENERATION.append(t)
                count += 1
    result = sorted(BEST_TEAMS, key=lambda x: eval_team_int(x), reverse=True)
    return result[0]

# Advanced Objective
def get_best_game(size, num_gen, min_val):
    BEST_GAME_SETS = []
    GK, DEF, MID, FOR = group_data(get_player_data())
    GENERATION = copy.deepcopy(generate_games(size, GK, DEF, MID, FOR))
    for _ in range(num_gen):
        print(_)
        # rank the teams
        RANKED_GAMES = []
        for g in GENERATION:
            RANKED_GAMES.append((eval_game_set(g), g))
        RANKED_GAMES = sorted(RANKED_GAMES, key=lambda x: x[0], reverse=True)
        # get current best team
        if RANKED_GAMES[0][0] > min_val:
            if RANKED_GAMES[0][1] not in BEST_GAME_SETS:
                BEST_GAME_SETS.append(copy.deepcopy(RANKED_GAMES[0][1]))
        # get top 30 percent teams for computing next gen
        top_30_percent = RANKED_GAMES[:int(size * 0.3)]
        # new player and team samples
        NEW_PLAYER_SAMPLES = []
        NEW_GAME_SAMPLES = []
        for g in top_30_percent:
            NEW_GAME_SAMPLES.append(copy.deepcopy(g[1]))
            for t in g[1]:
                for p in t:
                    if p not in NEW_PLAYER_SAMPLES:
                        NEW_PLAYER_SAMPLES.append(p)
        Gk, Def, Mid, For = group_data(NEW_PLAYER_SAMPLES)
        # generate new gen
        GENERATION = []
        # random generation
        GENERATION += copy.deepcopy(generate_games(int(size * 0.2), Gk, Def, Mid, For))
        # Crossover
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            c = random.randint(1, 2)
            t1 = random.choice(NEW_GAME_SAMPLES)
            t2 = random.choice(NEW_GAME_SAMPLES)
            dup = False
            for x1 in t1[:c]:
                for x2 in t2[c:]:
                    a = copy.deepcopy(x1)
                    b = copy.deepcopy(x2)
                    if has_conflict(copy.deepcopy(a), copy.deepcopy(b)):
                        dup = True
            if not dup:
                n_t = t1[:c] + t2[c:]
                GENERATION.append(copy.deepcopy(n_t))
                count += 1
        # Mutation
        count = 0
        m_size = int(size * 0.4)
        while count < m_size:
            t = random.choice(NEW_GAME_SAMPLES)
            c = random.randint(0, 3)
            t[c] = []
            mod = False
            while not mod:
                tmp = build_team(GK, DEF, MID, FOR)
                no_c = True
                for ts in t:
                    if has_conflict(ts, tmp):
                        no_c = False
                if no_c:
                    t[c] = copy.deepcopy(tmp)
                    GENERATION.append(copy.deepcopy(t))
                    mod = True
            count += 1
    result = sorted(BEST_GAME_SETS, key=lambda x: eval_game_set(x), reverse=True)
    return result[0]

# print('Minimal Objective Result:')
# r = get_best_teams(1000, 100, 70)
# print_team(r)
#
# print('Intermediate Objective Result:')
# r = get_best_teams_int(1000, 100, 70)
# print_team_int(r)

print('Advanced Objective Result:')
r = get_best_game(1000, 10, 230)
print_game_set(r)