import time
import sys

time_start = time.time()
seconds = 0
minutes = 0

while True:
        print("{minutes} Minutes {seconds} Seconds".format(minutes=minutes, seconds=seconds))
        time.sleep(1)
        seconds = int(time.time() - time_start) - minutes * 60
        if seconds >= 60:
            minutes += 1
            seconds = 0
   
