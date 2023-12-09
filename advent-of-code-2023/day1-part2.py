import regex

input = """1five7396484
sevenasdf4"""

"""
Get the first and last digit of each line
but now, in contrast to part 1, words can also be "digits"
concatenate the digits and sum them up

For example:
1five7396484 => 14
onejfa12nfz3 => 13

sum => 27
"""

values = []

word_to_number = {
    "zero": 0,
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

valid_digit = [str(d) for d in word_to_number.values()]

valid_word = list(word_to_number.keys())

for line in input.split("\n"):
    # use regex instead of re, so that we get "overlappings", e.g. oneight => [1, 8]
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