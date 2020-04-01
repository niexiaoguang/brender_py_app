import avro
import io
import avro.schema
import avro.io


test_schema = '''
{
"namespace": "example.avro",
 "type": "record",
 "name": "User",
 "fields": [
     {"name": "name", "type": "string"},
     {"name": "favorite_number",  "type": ["int", "null"]},
     {"name": "favorite_color", "type": ["string", "null"]}
 ]
}
'''

schema = avro.schema.parse(test_schema)
writer = avro.io.DatumWriter(schema)

bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write({"name": "Alyssa", "favorite_number": 256}, encoder)
writer.write({"name": "Ben", "favorite_number": 7, "favorite_color": "red"}, encoder)

raw_bytes = bytes_writer.getvalue()
print(len(raw_bytes))
print(type(raw_bytes))

bytes_reader = io.BytesIO(raw_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
reader = avro.io.DatumReader(schema)
user1 = reader.read(decoder)
user2 = reader.read(decoder)

print(user1)
print(user2)