from typing import Tuple, List


def intersect(range_a: Tuple[int, int], range_b: Tuple[int, int]):
    left_boundary = max(range_a[0], range_b[0])
    right_boundary = min(range_a[1], range_b[1])
    if left_boundary < right_boundary:
        return (left_boundary, right_boundary)
    
    return None


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


def prepare_seed_ranges(seed_ranges):
    # convert (start, len) notation to (start, end)
    seed_positions = []

    for i in range(0, len(seed_ranges), 2):
        start = seed_ranges[i]
        length = seed_ranges[i+1]
        seed_positions.append((start, start+length))


    return seed_positions


def parse_input_data(lines):

    seed_ranges = None

    found_map = False
    map_category_index = 0
    map_index = -1

    mappings = {}

    # parse input data
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



def apply_mapping(range, mappings, results, direction="up"):
                
    # termination/ base case
    # if we don't have any more mappings to try
    # then return identity
    if len(mappings) == 0:
        results.append({
            "destination_range": range,
            "source_range": range,
            "shift": 0,
        })
        return

    # test if the range is in the first mapping
    mapping = mappings[0]

    destination_range = mapping["destination_range"] if direction == "up" else mapping["source_range"]
    shift = mapping["shift"]

    if direction == "down":
        shift = shift * -1

    overlap = intersect(range, destination_range)

    # this range has a mapping -> apply it
    if overlap: 
        # calculate new range with the shift

        if direction == "down":
            results.append({
                    "source_range": overlap,
                    "destination_range": (overlap[0]+shift, overlap[1]+shift),
                    "shift": shift,
                })
        else:
            results.append({
                "destination_range": overlap,
                "source_range": (overlap[0]+shift, overlap[1]+shift),
                "shift": shift,
            })

        remainings = subtract(range, overlap)

        # some parts are outside of the range, this mapping does not apply, but maybe another?
        if remainings:
            # recusively check if this range is included in another mapping
            # remove first mapping from mappings list since we already applied it
            rest_mappings = mappings[1:]
            for rem in remainings:
                apply_mapping(rem, rest_mappings, results)
    else:
        # no overlap, try another mapping
        rest_mappings = mappings[1:]
        apply_mapping(range, rest_mappings, results, direction=direction)


if __name__ == '__main__':
    lines = """##""".split("\n")
    
    print("Parsing input data")
    mappings, seeds = parse_input_data(lines)

    # initialize with the range where we know already it must be the lowest 
    destination_ranges = [{
        "source_range": (0,213274662)
    }]

    all_results = {}

    # now go back up the different levels any apply each mapping upwards
    for i, level in reversed(mappings.items()):

        result_ranges = []

        for destination_range in destination_ranges:

            # for each level, the source_range of the previous level now becomes the destination_range
            destination_range = destination_range["source_range"]
                    
            # for each level we have multiple mappings
            level_mappings = sorted(level.values(), key=lambda m: m["destination_start"])

            apply_mapping(destination_range, level_mappings, result_ranges)

        # use the output of this level for input of next level
        destination_ranges = result_ranges

        all_results[i] = result_ranges
                
    print("Build up tree from bottom to top")

    # all the source_ranges from the last level have a path down the the initial destination_range

    # find the overlap between those source_ranges and the source_ranges given by the puzzle
    # to further reduce the options we need to brute force

    print("Convert sources to list of ints")

    # we now the input must be from this list
    source_ranges = [r["source_range"] for r in all_results[0]]

    print(f"Total possible sources {len(source_ranges)}")

    puzzle_input_ranges = [s for s in seeds]

    print("Filter sources according to puzzle input")

    #reduced_source = [s for s in source if any(s in r for r in puzzle_input_ranges)]
    reduced_source = [intersect(source_range, puzzle_range) for source_range in source_ranges for puzzle_range in puzzle_input_ranges]

    source_ranges = [{
        "destination_range": s
        } for s in reduced_source if s is not None
        ]


    print(f"Calculate result for len of inputs {len(reduced_source)}")

    all_results = {}

    # now go down
    for i, level in mappings.items():

        result_ranges = []

        for source_range in source_ranges:

            # for each level, the source_range of the previous level now becomes the destination_range
            destination_range = source_range["destination_range"]
                    
            # for each level we have multiple mappings
            level_mappings = sorted(level.values(), key=lambda m: m["source_range"])

            apply_mapping(destination_range, level_mappings, result_ranges, direction="down")

        # use the output of this level for input of next level
        source_ranges = result_ranges

        all_results[i] = result_ranges


    min = sorted(all_results[len(all_results)-1], key=lambda r: r["destination_range"][0])
    print("Result", min[0]["destination_range"])

