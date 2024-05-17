from datetime import datetime, timedelta

# Rate from start to end. Any 2 timepoints would work though since the rate is fixed.
# 25-5-2023 9:37:01 # 2892757385733.60
# 25-5-2023 9:51:02 # 2590206837120.00
start = datetime.strptime("25-5-2023 9:37:01", "%d-%m-%Y %H:%M:%S")
end = datetime.strptime("25-5-2023 9:51:02", "%d-%m-%Y %H:%M:%S")
distance = 2892757385733.60 - 2590206837120.00
rate = distance / (end-start).total_seconds()
print(rate)
# The distance is decreasing with 359750949.6 "distance" per second.

# Duration is distance/speed.
seconds_left = 2590206837120.00/rate
print(end + timedelta(seconds=seconds_left))

# 2023-05-25 11:51:02
# Someone else solved this - so Im not sure if this is correct.