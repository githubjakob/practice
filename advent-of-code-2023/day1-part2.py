import regex

input = """1five7396484"""

values = []

valid_digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

word_to_number = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

valid_word = list(word_to_number.keys())

for line in input.split("\n"):
    # zero?
    parts = regex.findall(r'one|two|three|four|five|six|seven|eight|nine|ten|\d|[a-zA-Z]', line, overlapped=True)
    line = [word_to_number[c] if c in valid_word else c for c in parts]
    line = [int(c) if c in valid_digit else c for c in line]
    line = [c for c in line if isinstance(c, int)]
    first = next(iter(line), None)
    last = next(iter(reversed(line)), None)
    if first and last:
        values.append(int(str(first) + str(last)))

print(values)
print(sum(values))