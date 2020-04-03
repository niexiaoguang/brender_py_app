import requests
import os
from pathlib import Path
import gzip
import time
def download_steam(url,savepath,chunk=2048):
    r = requests.get(url, stream=True)
    with open(savepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk):
            if chunk:
                f.write(chunk)
                # time.sleep(0.1) # speed limit TODO

 


def compress(filepath):
    p = Path(filepath)
    if not p.is_file():
        return

    # f_in = open(filepath, 'rb')
    # f_out = gzip.open(filepath + '.gz', 'wb')
    # f_out.writelines(f_in)
    # f_out.close()
    # f_in.close()
    input = open(p, 'rb')
    s = input.read()
    input.close()
    
    outputPath = Path(str(p) + '.gz')
    output = gzip.GzipFile(outputPath, 'wb')
    output.write(s)
    output.close()
    return str(outputPath)


def decompress(filepath,dest_folder,overwrite=True):
    p = Path(filepath)
    if not p.is_file() or p.suffix != '.gz':
        return

    input = gzip.GzipFile(p, 'rb')
    s = input.read()
    input.close()

    outputPath = Path(str(p)[:-3])
    if overwrite and outputPath.is_file():
        os.remove(outputPath)
    else:
        print('not overwrite')
        outputPath = Path(dest_folder).joinpath(Path(outputPath.stem + '.' + str(time.time()) + outputPath.suffix))
        print(outputPath)
    output = open(outputPath, 'wb')
    output.write(s)
    output.close()

    return str(outputPath)

PartSize = 4096 * 1024 # 4MB parts file

def split(source, dest_folder, write_size=PartSize):
    # Make a destination folder if it doesn't exist yet
    # make sure source exist
    if not Path(source).is_file():
        return

    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)
    else:
        # Otherwise clean out all files in the destination folder
        for file in os.listdir(dest_folder):
            os.remove(os.path.join(dest_folder, file))
 
    partnum = 0
    source = Path(source)
    # Open the source file in binary mode
    input_file = open(source, 'rb')
 

    while True:
        # Read a portion of the input file
        chunk = input_file.read(write_size)
 
        # End the loop if we have hit EOF
        if not chunk:
            break
 
        # Increment partnum
        partnum += 1
 
        # Create a new file name
        filename = os.path.join(dest_folder, source.name + str(partnum).zfill(3))
 
        # Create a destination file
        dest_file = open(filename, 'wb')
 
        # Write to this portion of the destination file
        dest_file.write(chunk)
 
        # Explicitly close 
        dest_file.close()
     
    # Explicitly close
    input_file.close()
     
    # Return the number of files created by the split
    return partnum
 
 
def join(source_dir, dest_file, read_size=PartSize):
    # Create a new destination file
    dest_file = Path(dest_file)
    output_file = open(dest_file, 'wb')
     
    # Get a list of the file parts
    parts = os.listdir(source_dir)
     
    # Sort them by name (remember that the order num is part of the file name)
    parts.sort()
 
    # Go through each portion one by one
    for file in parts:
         
        # Assemble the full path to the file
        path = os.path.join(source_dir, file)
         
        # Open the part
        input_file = open(path, 'rb')
         
        while True:
            # Read all bytes of the part
            bytes = input_file.read(read_size)
             
            # Break out of loop if we are at end of file
            if not bytes:
                break
                 
            # Write the bytes to the output file
            output_file.write(bytes)
             
        # Close the input file
        input_file.close()
         
    # Close the output file
    output_file.close()
    return str(dest_file)


