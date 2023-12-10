

lines = """seeds: int1 int2 ...

map1 map:
<target-start> <source-start> <range>

map2 map:
<target-start> <source-start> <range>

""".split("\n")

seed_positions = None

found_map = False
map_category_index = -1
map_index = -1

mappings = {}

mapping_functions = []

# parse input data
# convert to [[func1, func2], [func3, func4]]
# apply one function for each "mapping group"
for line in lines:
    if line is None or line == "":
        found_map = False
        map_index += 1
        map_category_index += 1
        continue

    if line.startswith("seeds:"):
        line = line.strip()
        line = line.replace("seeds: ", "")
        seed_positions = line.split(" ")
        seed_positions = [int(s) for s in seed_positions]

    if "map" in line:
        found_map = True
        continue
    
    if found_map:
        if not mappings.get(map_index):
            mappings[map_index] = {}

        mapping = line.split(" ")

        source_start = int(mapping[1])
        target_start = int(mapping[0])
        length = int(mapping[2])

        # curry to make the source_start, target_start, and length vars available in mapping_func ??
        def mapping_func_curry(source_start, target_start, length):

            def mapping_func(input):
                if input >= source_start and input <= source_start + length:
                    res = input + target_start - source_start
                    print(f"Applied func {target_start} {source_start} {length} -> {res}")
                    return res
                
                # identity by default
                return input

            return mapping_func
        
        # not needed actually
        mappings[map_index][map_category_index] = {
            "source_start": mapping[1],  
            "target_start": mapping[0],
            "length": mapping[2],
            "func": mapping_func_curry(source_start, target_start, length),
        }

        if len(mapping_functions) <= map_index:
            mapping_functions.append([])

        mapping_functions[map_index].append( mapping_func_curry(source_start, target_start, length))



def apply_mapping_functions(input):
    res = input
    for func_group in mapping_functions:
        next_group = False
        i = 0
        while not next_group and i < len(func_group):
            tmp_res = func_group[i](res)
            if tmp_res != res:
                res = tmp_res
                # break out of this group when we found a mapping
                next_group = True
            i += 1
                
    
    return res

print(min([apply_mapping_functions(s) for s in seed_positions]))