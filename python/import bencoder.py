import bencoder

def convert(data):
    print(data)
    if isinstance(data,str):  return bytes(data, encoding = 'utf8')
    if isinstance(data,dict):   return dict(map(convert, data.items()))
    if isinstance(data,tuple):  return map(convert, data)
    if isinstance(data,list):  return [convert(i) for i in data]
    return data

tid = "1abc"
msg = dict(t=tid, y="e", e=[202, "Server Error"])

msg = convert(msg)
re = bencoder.encode(msg)
print(re)