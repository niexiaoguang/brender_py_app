from qiniu import etag
from pathlib import Path

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')



def get_file_hash(filepath):
    if Path(filepath).is_file():
        return etag(filepath)
    else:
        return 'None'