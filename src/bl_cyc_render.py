bl_exec_path = '/usr/app/blender-2.82a-linux64/blender'

print('hello blender py')


import subprocess
import sys

# create two files to hold the output and errors, respectively

output = ''
errors = ''
with open('/tmp/blender/out.txt','w+') as fout:
    with open('/tmp/blender/err.txt','w+') as ferr:
        out=subprocess.call([bl_exec_path,
        	'-b',
        	'/tmp/blender/eve.blend',
        	'-P',
        	'/tmp/blender/cyc.py'],

        	stdout=fout,stderr=ferr)
        # reset file to read from it
        fout.seek(0)
        # save output (if any) in variable
        output=fout.read()

        # reset file to read from it
        ferr.seek(0) 
        # save errors (if any) in variable
        errors = ferr.read()

# output

print(output)
# errors

print(errors)