import time
import sys
print('running ' + __file__)
found = False
i = 0
while not found:
    time.sleep(2)
    sys.stdout.write(__file__ + ' ' + str(time.time()))
    sys.stdout.flush()

    i += 1
    if(i >= 10):
        found = True

sys.stdout.write(__file__ + 'finished')
sys.stdout.flush()
