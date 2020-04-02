import avro

class Protocol():
    GetFileHash = 0
    Download = 1
    Upload = 2



Schema = avro.schema.Parse(open("brender.avsc", "rb").read())