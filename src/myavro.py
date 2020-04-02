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


# schema will updating by dev and copy to client TODO
class Schema():
    file_handler_schema_req = '''
    {
    "namespace": "brender.avro",
    "type": "record",
    "name": "fq",
    "fields": [
        {"name": "code", "type": "int"},
        {"name": "pa",  "type": "string"},
        {"name": "re", "type": "string"}
        ]
    }
    '''

    file_handler_schema_result = '''
    {
    "namespace": "brender.avro",
    "type": "record",
    "name": "fr",
    "fields": [
        {"name": "code", "type": "int"},
        {"name": "ha",  "type": "string"},
        {"name": "st", "type": "ini"}
        ]
    }

    '''
class SchemaNameConst():
    FilePath = 'pa'
    FileHash = 'ha'
    Code = 'code'
    ReQueueName = 're'
    Status = 'st'
    FileHandlerReq = 'fq'
    FileHanlderRes = 'fr'


def encode_byte(reqSchema):
    schema = avro.schema.Parse(reqSchema)
    writer = avro.io.DatumWriter(schema)

    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"sname": "Alyssa", "favorite_number": 256}, encoder)
    writer.write({"sname": "Ben", "favorite_number": 7, "favorite_color": "red"}, encoder)

    raw_bytes = bytes_writer.getvalue()
    return raw_bytes


def encode_byte_body(code,data):
    res = None
    return res


def decode_byte_body(raw_bytes):

    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    res = reader.read(decoder)
    return res