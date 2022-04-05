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
