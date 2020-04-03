import sys
lib_path = './lib/avro-python3-1.9.2'
sys.path.append(lib_path)

import avro
import io
import avro.schema
import avro.io

# mayby installer need it ? TODO
# import json

# import logging
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class SchemaNameConst():
    Code = 'code'
    Data = 'data'
    Status = 'status'
    Sender = 'sender'


class Code():
    FileHash = 0
    Download = 1
    Upload = 2


class Status():
    success = 200
    error = 400

# schema will updating by dev and copy to client TODO
class Schema():
    file_handler_schema = '''
    {
    "namespace": "brender.avro",
    "type": "record",
    "name": "file_handler",
    "fields": [
        {"name": "code", "type": "int"},
        {"name": "data",  "type": "string"},
        {"name": "status", "type": "int"},
        {"name": "sender", "type": "string"}
        ]
    }
    '''


def encode_byte_body(data):
    schema = avro.schema.Parse(Schema.file_handler_schema)

    writer = avro.io.DatumWriter(schema)

    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)

    # writer.write({"sname": "Alyssa", "favorite_number": 256}, encoder)
    writer.write(data,encoder)

    raw_bytes = bytes_writer.getvalue()
    return raw_bytes



def decode_byte_body(raw_bytes):
    schema = avro.schema.Parse(Schema.file_handler_schema)
    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    res = reader.read(decoder)
    return res