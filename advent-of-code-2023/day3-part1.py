

lines = (
    """467..114..
    ...*......
    ..35..633.""".split("\n")
    )

numbers = {}

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


sum_numbers = 0

for number_dict in numbers.values():
    line_number = number_dict["line_number"]
    number = number_dict["number"]
    number_position = number_dict["number_position"]

    prev_line = lines[line_number-1] if line_number > 0 else None
    line = lines[line_number]
    next_line = lines[line_number+1] if line_number < len(lines)-1 else None


    def check_line(current_line):
        if current_line is None:
            return False
        
        start = max(0, number_position-1)
        end = min(len(current_line), number_position+len(number)+1)

        adjacent_chars = current_line[start:end]

        return any(c for c in adjacent_chars if not c.isnumeric() and not c == ".")
    
    has_adjacent_symbol = any(check_line(l) for l in [prev_line, line, next_line])

    if has_adjacent_symbol:
        sum_numbers += int(number)

    print("has_adjacent_symbol", number, has_adjacent_symbol)
        
 
print(sum_numbers)