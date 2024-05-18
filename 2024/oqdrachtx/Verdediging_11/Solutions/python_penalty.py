base = "2024/oqdrachtx/Verdediging_11/Noodweer in de Stad/"

with open(base + "gebouwhoogtes.txt", "r") as f:
    buildings = f.readlines()[0]

buildings = eval(buildings)

# buildings = [4, 5, 1, 3, 3, 5, 1, 5]


def get_water(building_heights, stop_at_height=None):
    total_water = 0
    passed = 0
    penalty = 0
    curr_highest = 0

    for building_height in building_heights:
        if building_height >= curr_highest:

            total_water += (curr_highest * passed) - penalty
            passed = 0
            penalty = 0
            curr_highest = building_height

            if stop_at_height is not None and building_height >= stop_at_height:
                return total_water
            continue

        penalty += building_height
        passed += 1

    if passed != 0:
        # if we get here we've hit the end of the array but still passed buildings along the way here; we can store potential magical wbbsu here!
        # to get this missed amount flip the array and walk through it until we've hit the last known highest building (we know the result from there) and add that to our current total.
        total_water += get_water(
            reversed(building_heights), stop_at_height=curr_highest
        )

    return total_water


print(
    f"The water that can be stored between the buildings is: {get_water(buildings)} wbbsu (water between building store units)."
)
