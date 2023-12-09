lines = """Card 1: 33 48 83 21 17 | 83 86  6 31 17  9 48 53""".split("\n")


"""
Find all numbers that are that are in both sets (divided by |)
Sum up the "points" ( 2 ** len(numbers))
"""

sum = 0

for line in lines: 
    winning_numbers = set(line.split("|")[0].split(":")[1].strip().split(" "))
    winning_numbers = set([n for n in winning_numbers if not n == ""]) # clean empty strings

    my_numbers = set(line.split("|")[1].strip().split(" "))
    my_numbers = [n for n in my_numbers if not n == ""] # clean empty strings
    
    my_wining_numbers_count = len(winning_numbers.intersection(my_numbers))

    my_points = 2 ** (my_wining_numbers_count - 1) if my_wining_numbers_count else 0
    
    sum += my_points

print(sum)