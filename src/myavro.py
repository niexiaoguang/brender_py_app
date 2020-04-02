# import sys
# lib_path = './avro-python3-1.9.2'
# sys.path.append(lib_path)

import avro
import io

import avro.schema

test_schema = '''
{
"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "sname", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}
'''

Schema = avro.schema.Parse(open("./config/brender.avsc", "r").read())