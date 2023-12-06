from collections import defaultdict

games = []
with open("02", "r", encoding="utf-8") as inp:
    for game in inp:
        game = game.split(":")[1]
        game_result = defaultdict(list)
        for hand in game.split(";"):
            for num_color in hand.strip().split(","):
                num, color = num_color.strip().split(" ")
                game_result[color].append(int(num))
        games.append(game_result)

RED_LIM = 12
GREEN_LIM = 13
BLUE_LIM = 14

possible_game_inds = []
for i, game in enumerate(games):
    if any(blue_count > BLUE_LIM for blue_count in game["blue"]) or \
        any(green_count > GREEN_LIM for green_count in game["green"]) or \
        any(red_count > RED_LIM for red_count in game["red"]):
        continue
    else:
        possible_game_inds.append(i)

print(sum(i + 1 for i in possible_game_inds))

games_power = []
for game in games:
    power = 1
    power *= max(game["red"])
    power *= max(game["green"])
    power *= max(game["blue"])
    games_power.append(power)

print(sum(games_power))