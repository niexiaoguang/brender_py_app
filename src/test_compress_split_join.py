import myutils

# myutils.split('./data/zoom.pkg','./data/split/')

# myutils.join('./data/split','./data/result.pkg')

# myutils.compress('./data/zoom.pkg')
# myutils.decompress('./data/zoom.pkg.gz','./data')


# p = myutils.compress('./data/zoom.pkg')
# myutils.split(p,'./data/split/')

p = myutils.join('./data/split','./data/result.pkg.gz')
myutils.decompress(p,'./data')