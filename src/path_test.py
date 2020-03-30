import os
from pathlib import Path

# list all files under a folder except some sub folders and extension 
exceptDirs = ['data/f1']
exceptExts = ['.jpg','.txt']

# for root, dirs, files in os.walk("./data"):

#     for p in exceptDirs:
#         if Path(p) not in Path(root).parents and p != root:
#             # print(root)
#             # print(dirs)
#             for filename in files:
#                 ext = Path(filename).suffix
#                 if ext not in exceptExts:

#                     print(filename)



# # much cleaner version
# targetDir = './data'
# exceptDirs = ['f1/f2'] # sub dictory under targetDir 
# exceptExts = ['.jpg','.txt']
# p = Path(targetDir)
# for i in p.glob('**/*'):
#     for folder in exceptDirs:
#         if p.joinpath(folder) not in i.parents and i.is_file() and i.suffix not in exceptExts:
#             print(i)


print(Path.cwd())
cwd = Path.cwd()
cwd = str(cwd)
cwd = Path(cwd)
print(type(cwd))
maybepath = 'engijaepijf'
maybepath = './data/f1/3.blend'

print(Path(maybepath).is_file())

maybepath = './data/f1/'
print(Path(maybepath).is_dir())