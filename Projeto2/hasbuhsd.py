import struct
def float_to_binary32(value):
    bits, = struct.unpack('!I', struct.pack('!f', value))
    return f'{bits:032b}'

print(float_to_binary32(2.000024))