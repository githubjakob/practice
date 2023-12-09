input = """one1five"""

values = []

"""
Get the first and last digit of each line
concatenate the digits
sum them up
"""

for line in input.split("\n"):
    line = [int(c) for c in line if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]
    first = next(iter(line), None)
    last = next(iter(reversed(line)), None)
    if first and last:
        values.append(int(str(first) + str(last)))

print(values)
print(sum(values))