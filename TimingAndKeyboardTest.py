'''import keyboard
from datetime import datetime

raw_input("Press enter to start")
start_time = datetime.now()

raw_input("Press enter to stop")
finish_time = datetime.now()

total_time = finish_time - start_time

print(total_time.total_seconds())'''
"""
print('Enter your name:')
x = raw_input()
print('Hello, ' + x)"""

import operator
x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1))
sorted_x.reverse()
sorted_x_keys = []
for i in sorted_x:
    sorted_x_keys.append(i[0])

print(sorted_x)
print(sorted_x_keys)
