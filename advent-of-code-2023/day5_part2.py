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
    lines = """seeds: 1848591090 462385043 2611025720 154883670 1508373603 11536371 3692308424 16905163 1203540561 280364121 3755585679 337861951 93589727 738327409 3421539474 257441906 3119409201 243224070 50985980 7961058

seed-to-soil map:
3305253869 1699909104 39566623
3344820492 1130725752 384459310
3244681427 1739475727 60572442
951517531 1800048169 868898709
1820416240 951517531 179208221
1999624461 2668946878 219310925
3729279802 1515185062 184724042
2218935386 2898481077 1015522767
3234458153 2888257803 10223274

soil-to-fertilizer map:
1569885498 220184682 161941102
3711640300 872157831 344226893
1934701528 0 25420995
3394438846 2543943059 181930710
2957858493 2070565336 135870012
1416178127 25420995 36071868
1030022714 2029369539 9317803
1039340517 1216384724 133685745
695011633 382125784 335011081
2317056551 1350070469 640801942
1731826600 2887680679 151926123
0 3039606802 695011633
2030497645 2257384153 286558906
1960122523 2038687342 31877994
3576369556 2840047597 42331426
1536338434 4027621785 33547064
1452249995 3964767856 62853929
1331718081 787697785 84460046
4055867193 2882379023 5301656
3093728505 3734618435 230149421
1173026262 61492863 158691819
1883752723 2206435348 50948805
3618700982 2725873769 92939318
1515103924 2818813087 21234510
1992000517 1990872411 38497128
3323877926 717136865 70560920

fertilizer-to-water map:
898769374 211542615 277361469
2901739042 2299030230 213178977
207924763 1114173904 26774777
3752402183 1968349402 71176470
1176130843 625299169 68863743
3114918019 3783121220 137843736
1244994586 488904084 103878858
3252761755 2915409726 98951129
2779748334 3652754391 121990708
3351712884 2593688676 245406043
0 1252990064 95883380
2007290234 3920964956 325008750
3823578653 2039525872 202532901
2443486939 2512209207 81479469
4231974038 3371954615 62993258
3698239076 2242058773 54163107
2340675105 3014360855 102811834
4219112930 4245973706 12861108
4026111554 2839094719 76315007
3597118927 3434947873 101120149
2332298984 3774745099 8376121
95883380 1140948681 112041383
4102426561 3536068022 116686369
1968349402 2296221880 2808350
1971157752 4258834814 36132482
866253147 592782942 32516227
446242155 694162912 420010992
2524966408 3117172689 254781926
234699540 0 211542615

water-to-light map:
3564276417 3073533986 256027539
540951899 3329561525 136112599
3123682450 3465674124 119685876
2479417373 4222809437 72157859
1957776831 2195006920 74795586
3089045940 3585360000 28951457
3820985109 2269802506 288781515
1285562478 1664965131 530041789
234319697 234026754 79806762
3243368326 1344057040 320908091
3117997397 541633052 5685053
2551575232 547318105 349893979
3820303956 540951899 681153
0 369583040 292943
314126459 313833516 55749524
4109766624 2888333314 185200672
292943 0 234026754
677064498 3614311457 608497980
2032572417 897212084 446844956
2901469211 2700756585 187576729
1815604267 2558584021 142172564

light-to-temperature map:
2658328410 4044901271 250066025
866264123 157899985 185676775
2062023507 343576760 307684950
1535723010 981670684 313982539
3292868240 2534053678 579746095
3905180794 3703329819 341571452
2908394435 3318856014 384473805
1194970869 1601263273 340752141
427693043 1299669198 158564104
748173107 651261710 118091016
1051940898 1458233302 143029971
586257147 0 157899985
4246752246 2485838628 48215050
1849705549 769352726 212317958
0 2368902754 805703
744157132 1295653223 4015975
805703 1942015414 426887340
3872614335 3113799773 32566459
2485838628 3146366232 172489782

temperature-to-humidity map:
2731357374 2535823037 72664015
2987243945 1266132780 17518070
3983567677 3876954134 113067367
1669770178 435765631 9597802
192217183 2087059527 132586479
324803662 1449340061 36910958
82239523 1283650850 47718149
4251710314 3400860374 43256982
788691045 2012848120 74211407
139712452 383260900 52504731
1679367980 1064470362 18439862
3627675589 3649605531 101947626
1761484189 1024489895 39980467
3964889474 4132263773 7628253
469056934 1486251019 222779936
3808503415 3992550600 118386133
4096635044 4139892026 155075270
0 328658745 54602155
3929418647 3751553157 35470827
3729623215 3787023984 78880200
129957672 2003093340 9754780
3926889548 3990021501 2529099
2130123401 3260061108 28438224
1154320063 445363433 515450115
2331952939 1331368999 72869773
2804021389 1082910224 183222556
1140184340 2219646006 14135723
3606348549 4110936733 21327040
3004762015 1709030955 50302777
1801464656 0 328658745
691836870 1759333732 96854175
447785309 2608487052 21271625
3400860374 3444117356 205488175
3055064792 2233781729 261071908
2185047506 1856187907 146905433
1697807842 960813548 63676347
361714620 2494853637 40969400
2404822712 2933526446 326534662
402684020 1404238772 45101289
3972517727 3865904184 11049950
2158561625 2907040565 26485881
862902452 2629758677 277281888
54602155 3288499332 27637368

humidity-to-location map:
1368371614 3063096196 39876417
2318920763 3734391855 138926764
2980019498 3984955289 310012007
3732521234 1430493364 562446062
213274662 484132485 78936678
0 892307918 213274662
1023610211 575518293 214768297
2807160244 2776517513 21582263
2457847527 2833630022 176634966
3619027057 2663023336 113494177
2926107621 1368371614 53911877
1784866635 3524616139 209775716
2695523574 3873318619 111636670
1250827638 790286590 102021328
3290031505 1992939426 224427328
954760770 415283044 68849441
1408248031 2286404732 376618604
292211340 0 415283044
1994642351 3102972613 324278412
2642692366 3034347120 28749076
3514458833 2798099776 35530246
1238378508 563069163 12449130
2828742507 3427251025 97365114
3549989079 2217366754 69037978
2671441442 3010264988 24082132
707494384 1105582580 247266386
2634482493 1422283491 8209873
""".split("\n")
    
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

