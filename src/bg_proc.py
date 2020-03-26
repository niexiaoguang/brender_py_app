# import thread_subprocess
import time
import os
import subprocess
import sys

# thread_subprocess.test()

pyExecPath = 'python'


p = subprocess.Popen([pyExecPath,'bg_script.py'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,universal_newlines=True
                        )

returncode = p.poll()
while returncode is None:
        time.sleep(1)
        print('read from proc')
        line = p.stdout.readline()
        returncode = p.poll()
        line = str(line)
        line = line.strip()
        if(line):
            print(line)
print("result with : " ,returncode)

