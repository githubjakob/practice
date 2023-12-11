

from typing import Tuple, List


lines = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".split("\n")

seed_ranges = None

found_map = False
map_category_index = -1
map_index = -1

mappings = {}

mapping_functions = []
rev_mapping_functions = []


def intersect(range_a: Tuple[int, int], range_b: Tuple[int, int]):
    left_boundary = max(range_a[0], range_b[0])
    right_boundary = min(range_a[1], range_b[1])
    if left_boundary < right_boundary:
        return (left_boundary, right_boundary)
    
    return None


def flatten(l):
    return [item for sublist in l for item in sublist]


def subtract(range_a, range_b):
    if range_b is None:
        return range_a
    
    start_a, end_a = range_a
    start_b, end_b = range_b

    if end_b <= start_a or start_b >= end_a:
        return [(start_a, end_a)]

    if start_b > start_a and end_b < end_a:
        return [(start_a, start_b), (end_b, end_a)]

    if start_b <= start_a < end_b < end_a:
        return [(end_b, end_a)]

    if start_a < start_b < end_a <= end_b:
        return [(start_a, start_b)]

    return []


def subtract_list_of_ranges(original_range, ranges_to_subtract):
    ranges_to_subtract.sort(key=lambda x: x[0])

    result = [original_range]

    for r in ranges_to_subtract:
        temp_result = []
        for original in result:
            if r[1] <= original[0] or r[0] >= original[1]:
                temp_result.append(original)
                continue

            if original[0] < r[0] < original[1]:
                temp_result.append((original[0], r[0]))

            if original[0] < r[1] < original[1]:
                temp_result.append((r[1], original[1]))

        result = temp_result

    return result

def merge_ranges(ranges):
    if not ranges:
        return []

    # Sort the ranges based on the start of each range
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    merged = [sorted_ranges[0]]
    for current in sorted_ranges[1:]:
        last_merged = merged[-1]

        # Check if the current range overlaps or is adjacent to the last merged range
        if current[0] <= last_merged[1]:
            # Merge the two ranges
            merged[-1] = (last_merged[0], max(last_merged[1], current[1]))
        else:
            # No overlap, add the current range to the list
            merged.append(current)

    return merged



# curry to make the source_start, target_start, and length vars available in mapping_func ??
def mapping_func_curry(target_start, source_start, length):

    def mapping_func(input):
        if input >= source_start and input <= source_start + length:
            res = input + target_start - source_start
            #print(f"Applied func {target_start} {source_start} {length} -> {res}")
            return res
        
        # identity by default
        return input

    return mapping_func

def rev_mapping_func_curry(target_start, source_start, length):

    def rev_mapping_func(output_range: Tuple[int, int]):
        intersection = intersect(output_range, (target_start, target_start+length))
        if intersection:
            shift = source_start - target_start
            left_res = intersection[0] + shift
            right_res = intersection[1] + shift
            return (left_res, right_res), intersection, shift

        return None, output_range, None
    
    return rev_mapping_func


def parse_input_data(lines):

    seed_ranges = None

    found_map = False
    map_category_index = 0
    map_index = -1

    mappings = {}

    mapping_functions = []
    rev_mapping_functions = []

    # parse input data
    # convert to [[func1, func2], [func3, func4]]
    # apply one function for each "mapping group"
    for line in lines:
        line = line.strip()
        if line is None or line == "":
            found_map = False
            map_index += 1
            map_category_index = 0
            continue

        if line.startswith("seeds:"):
            line = line.strip()
            line = line.replace("seeds: ", "")
            seed_ranges = line.split(" ")
            seed_ranges = [int(s) for s in seed_ranges]

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

            mappings[map_index][map_category_index] = {
                "source_start": source_start,  
                "source_range": (source_start, source_start + length),
                "destination_start": target_start,
                "destination_range": (target_start, target_start + length),
                "length": length,
                "shift": source_start - target_start,
            }

            map_category_index += 1

    return mappings, prepare_seed_ranges(seed_ranges)


def apply_mapping_functions(input, mapping_functions):
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

def prepare_seed_ranges(seed_ranges):
    # convert (start, len) notation to (start, end)
    seed_positions = []

    for i in range(0, len(seed_ranges), 2):
        start = seed_ranges[i]
        length = seed_ranges[i+1]
        seed_positions.append((start, start+length))


    return seed_positions



def reverse_apply_mapping_functions(output_range, rev_mapping_functions):
    results = [[{ "destination_range": output_range}]]
    for i, func_group in enumerate(reversed(rev_mapping_functions)):
        
        for result in results[i]:
        # result is in output_range

            destination_rage = result["destination_range"]

            group_results = []
            for func in func_group:
                source_range, destination_range, shift = func(destination_rage)
                if source_range is not None:
                    group_results.append({
                        "source_range": source_range,
                        "destination_range": destination_range,
                        "shift": shift * -1,
                    })
            
            if i == len(results) - 1:
                results.append([])

            results[i+1] += group_results

            # TODO
            # if there are no source_ranges for the destination_range -> add identity for whole destination_range
            # if parts of the destination_range don't have a explicit mapping, calculate the missing piece and add identify function

            remaining_output_range = subtract_list_of_ranges(result["destination_range"], [r["destination_range"] for r in group_results])

            if remaining_output_range:
                results[i+1] += [{
                    "source_range": r,
                    "destination_range": r,
                }  for r in remaining_output_range ]

    return results


def backtrack(output_range, rev_mapping_functions, seed_ranges):
    # go up the tree and get the input seed for a output range
    tree = reverse_apply_mapping_functions(output_range, rev_mapping_functions=rev_mapping_functions)

    top_level_ranges = tree[len(tree)-1]

    print("top-level", top)

    merged_ranges = merge_ranges([r["source_range"] for r in top_level_ranges])



    #possible_seed_ranges = [intersect(top_level_range, seed_range) for seed_range in seed_ranges for top_level_range in top_level_ranges]
    #possible_seed_ranges = [r for r in possible_seed_ranges if r is not None]

    return merged_ranges

if __name__ == '__main__':
    rev_mapping_functions = parse_input_data(lines)
    # prepare_seed_ranges()
    reverse_apply_mapping_functions((0,55), rev_mapping_functions=rev_mapping_functions)



    #print(min([apply_mapping_functions(s) for s in seed_positions]))