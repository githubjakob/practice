lines = """Game 1: 5 blue, 1 red, 2 green; 11 red, 2 blue, 7 green"""

max_num_color = {
    "green": 13,
    "red": 12,
    "blue": 14,
}

sum_game_ids = 0

for line in lines.split("\n"):
    game = line.split(":")[0]
    game_id = int(game.replace("Game ", ""))
    possible = True

    game_content = line.split(":")[1]
    for draw in game_content.split(";"):

        for color_content in draw.split(","):
            #print("#", color_content.strip())
            num_color = int(color_content.strip().split(" ")[0])
            color = color_content.strip().split(" ")[1]
            #print(num_color, color)
            max_num = max_num_color[color]
            if num_color > max_num:
                possible = False

    if possible:
        sum_game_ids += game_id 

print("sum", sum_game_ids)