import keyboard
from datetime import datetime

raw_input("Press enter to start")
start_time = datetime.now()

raw_input("Press enter to stop")
finish_time = datetime.now()

total_time = finish_time - start_time

print(total_time.total_seconds())
"""
print('Enter your name:')
x = raw_input()
print('Hello, ' + x)"""
target_time = 1.0
for x in [1,2,3,4,5,6,7,8,9,10]:
    raw_input("Press enter to indicate completion of exercise")
    ex_time = datetime.now()
    # Get the time between start and key press
    rep_time = ex_time - start_time
    rep_time_delta = rep_time.total_seconds()
    # Compare time to target time and update performance
    diff_from_target = target_time - rep_time_delta
    performance = 0
    if 0.5 < diff_from_target:
        performance = 1
    elif diff_from_target > -0.5:
        performance = 2

    start_time = ex_time

    # Controller start_time will be reset when the action goal is created.

    print("Rep time = " + str(rep_time.total_seconds()))
    print("Diff from target = " + str(diff_from_target))
    print("Performance = " + str(performance))
