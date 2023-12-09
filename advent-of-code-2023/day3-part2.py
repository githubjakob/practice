
lines = """
421..412..
...*......
..35......
""".split("\n")


line_lenght = len(lines[1]) # just in case 0 is empty

numbers = {}

def flatten(l):
    return [item for sublist in l for item in sublist]

for line_number, line in enumerate(lines):

    number_position = 0
    last_char_number = False
    
    for char_pos, char in enumerate(line):

        if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            if last_char_number:
                key = f"{line_number}-{number_position}"
                numbers[key]["number"] = numbers[key]["number"] + char
            else:
                number_position = char_pos
                last_char_number = True
                key = f"{line_number}-{number_position}"
                numbers[key] = {
                    "number": char,
                    "number_position": number_position,
                    "line_number": line_number,
                }
                
        else: 
            last_char_number = False

print(numbers)

def get_overlapping_numbers(line_number, start_position):
    overlapping_numbers = []
    for i in range(0, line_lenght):
        number = numbers.get(f'{line_number}-{i}')
        if number:
            number_position = number["number_position"]
            number_length = len(str(number["number"]))
            # 463..114..
            # ...*......
            # star_position = 3
            # overlapping iff 
            # - number_position = 0 && number_length >= 3
            # - number_position = 1 && number_length >= 2
            # - number_position = 2 && number_length >= 1
            # - number_position = 3
            # - number_position = 4
            left_boundary = max(0, number_position - 1)
            right_boundary = min(line_lenght, number_position + number_length -1 + 1)
            overlapping = left_boundary <= start_position and start_position <= right_boundary
            if overlapping:
                overlapping_numbers.append(number)
    return overlapping_numbers


sum = 0

for line_number, line in enumerate(lines):
    for char_pos, char in enumerate(line):
        if char == "*":
            prev_line_overlapping = get_overlapping_numbers(line_number-1, char_pos) if line_number > 0 else None
            line_overlapping = get_overlapping_numbers(line_number, char_pos)
            next_line_overlapping = get_overlapping_numbers(line_number+1, char_pos) if line_number < len(lines)-1 else None

            overlappig_total = flatten([prev_line_overlapping, line_overlapping, next_line_overlapping])

            if len(overlappig_total) == 2:
                first = overlappig_total[0]
                second = overlappig_total[1]

                gear_ratio = int(first["number"]) * int(second["number"])

                print(f"found star with 2 adjecant in line {line_number} {char_pos} ")

                sum += gear_ratio

print("sum", sum)




