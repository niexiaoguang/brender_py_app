# import sys
# lib_path = './avro-python3-1.9.2'
# sys.path.append(lib_path)

import avro
import io


Schema = avro.schema.Parse(open("./config/brender.avsc", "rb").read())