import os
import sys

scriptpath = "./src/"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

print('hello world')

args = sys.argv[1:]

print(args)

name = args[0]

