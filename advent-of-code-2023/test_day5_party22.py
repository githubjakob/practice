from day5_part2 import intersect, mapping_func_curry, parse_input_data, rev_mapping_func_curry, reverse_apply_mapping_functions, apply_mapping_functions, backtrack, subtract, subtract_list_of_ranges, merge_ranges

def flatten(l):
    return [item for sublist in l for item in sublist]

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
            # use only the list from this item on wards
            rest_mappings = mappings[1:]
            for rem in remainings:
                apply_mapping(rem, rest_mappings, results)
    else:
        # no overlap, maybe try another mapping
        rest_mappings = mappings[1:]
        apply_mapping(range, rest_mappings, results)

#if __name__ == '__main__':
def test_foo():
    # if we don't have matching mapping rule then use identity
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


    min = sorted(all_results[0], key=lambda r: r["destination_range"][0])
    print("###", min[0])







def test_subtract():

    res = subtract((0,100), (0,100))

    assert res == []

 