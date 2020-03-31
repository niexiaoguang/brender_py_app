import requests
from pathlib import Path
import qiniu
url = 'http://data.brender.cn/de5ad6c91e73fc5e.jpg'
# To save to a relative path.
r = requests.get(url)  
path = './data/5.jpg'
print(Path(path))
print(Path(path).is_file())

path = Path(path)
with open(path, 'wb') as f:
    f.write(r.content)