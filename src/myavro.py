import sys
lib_path = './lib/avro-python3-1.9.2'
sys.path.append(lib_path)

import avro
import io
import avro.schema
import avro.io

# mayby installer need it ? TODO
# import json

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

import myprotocol

class Schema():
    file_handler_schema = '''
    {
    "namespace": "brender.avro",
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "sname", "type": "string"},
        {"name": "favorite_number",  "type": ["int", "null"]},
        {"name": "favorite_color", "type": ["string", "null"]}
        ]
    }
    '''

def encode_byte():
    schema = avro.schema.Parse(file_handler_schema)
    writer = avro.io.DatumWriter(schema)

    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"sname": "Alyssa", "favorite_number": 256}, encoder)
    writer.write({"sname": "Ben", "favorite_number": 7, "favorite_color": "red"}, encoder)

    raw_bytes = bytes_writer.getvalue()
    return raw_bytes


def encode(code,data):

def decode_byte_body(raw_bytes):

    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    res = reader.read(decoder)
    return res