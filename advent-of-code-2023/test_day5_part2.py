
import numpy as np
from day5_part2 import intersect, mapping_func_curry, parse_input_data, rev_mapping_func_curry, reverse_apply_mapping_functions, apply_mapping_functions, backtrack, subtract_list_of_ranges, merge_ranges


def test_intersect():

    res = intersect((0,10), (20, 100))
    assert res is None

    res = intersect((10,20), (15, 100))
    assert res[0] == 15
    assert res[1] == 20

    res = intersect((10,20), (15, 17))
    assert res[0] == 15
    assert res[1] == 17

    res = intersect((10,20), (20, 30))
    assert res is None


def test_merge_ranges():

    res = merge_ranges([(0,10), (5, 20)])

    assert len(res) == 1
    assert res[0][0] == 0
    assert res[0][1] == 20

    res = merge_ranges([(0,10), (20, 30)])

    assert len(res) == 2
    assert res[0][0] == 0
    assert res[0][1] == 10

    assert res[1][0] == 20
    assert res[1][1] == 30

    res = merge_ranges([(0,10), (20, 30), (20, 35), (0,1), (0,11)])

    assert len(res) == 2
    assert res[0][0] == 0
    assert res[0][1] == 11

    assert res[1][0] == 20
    assert res[1][1] == 35

def test_rev_mapping_func():

    rev_mapping_func = rev_mapping_func_curry(1, 0, 69)
    mapping_func = mapping_func_curry(1, 0, 69)

    assert mapping_func(0) == 1
    assert mapping_func(1) == 2

    res = rev_mapping_func((1, 2))

    assert res[0] == 0
    assert res[1] == 1

    res = rev_mapping_func((100, 200))

    assert res is None


def test_parse_input_data():
    lines = """seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48""".split("\n")
    
    rev_mapping_functions, mapping_functions, _ = parse_input_data(lines)

    locations_rage = (0,55)

    results = reverse_apply_mapping_functions(locations_rage, rev_mapping_functions=rev_mapping_functions)

    assert len(results) == 2

    start_range = results[0]

    assert len(results[1]) == 2

    assert results[1][0][0] == 98
    assert results[1][0][1] == 100

    assert results[1][1][0] == 50
    assert results[1][1][1] == 53


def test_parse_input_data_reverse_identity():
    # if we don't have matching mapping rule then use identity
    lines = """seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48""".split("\n")
    
    rev_mapping_functions, mapping_functions, _ = parse_input_data(lines)

    output_range = (200,400)

    results = reverse_apply_mapping_functions(output_range, rev_mapping_functions=rev_mapping_functions)

    assert len(results) == 2

    start_range = results[0]

    assert len(results[1]) == 1

    assert results[1][0][0] == 200
    assert results[1][0][1] == 400


def test_parse_input_data_reverse_identity_2_levels():
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
    
    rev_mapping_functions, mapping_functions, _ = parse_input_data(lines)

    output_range = (0,56)

    results = backtrack(output_range, rev_mapping_functions, [(79,92)])
    

    assert len(results) == 3

    assert results[2][0]["source_range"][0] == 79
    assert results[2][0]["source_range"][1] == 81

    assert apply_mapping_functions(79, mapping_functions=mapping_functions) == 81
    assert apply_mapping_functions(80, mapping_functions=mapping_functions) == 82


def test_subtract_list():

    res = subtract_list_of_ranges((0,100), [(0,50)])

    assert len(res) == 1
    assert res[0][0] == 50
    assert res[0][1] == 100

    res = subtract_list_of_ranges((0,100), [(0,25), (50,100)])

    assert len(res) == 1
    assert res[0][0] == 25
    assert res[0][1] == 50

    res = subtract_list_of_ranges((0,100), [(10,20), (50,100)])

    assert len(res) == 2
    assert res[0][0] == 0
    assert res[0][1] == 10
    assert res[1][0] == 20
    assert res[1][1] == 50



def test_backtrack():

    lines = """seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15""".split("\n")
    
    rev_mapping_functions, mapping_functions, seed_ranges = parse_input_data(lines)

    backtrack((0,100), rev_mapping_functions, seed_ranges)