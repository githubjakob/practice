from day5_part2 import intersect, parse_input_data


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
