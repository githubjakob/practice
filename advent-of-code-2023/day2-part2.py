import functools
import operator

def product(iterable):
    return functools.reduce(operator.mul, iterable, 1)


lines = """Game 1: 1 blue, 2 red, 3 green; 4 red, 5 blue, 7 green"""

max_num_color = {
    "green": 13,
    "red": 12,
    "blue": 14,
}

sum_of_powers = 0

for line in lines.split("\n"):
    game = line.split(":")[0]
    game_id = int(game.replace("Game ", ""))
    
    min = {
        "green": 0,
        "red": 0,
        "blue": 0,
    }

    game_content = line.split(":")[1]
    for draw in game_content.split(";"):

        for color_content in draw.split(","):
            
            num_color = int(color_content.strip().split(" ")[0])
            color = color_content.strip().split(" ")[1]
        
            if min[color] <= num_color:
                min[color] = num_color
            
    power = product(min.values())
    sum_of_powers += power



print("sum", sum_of_powers)