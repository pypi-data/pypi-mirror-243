#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util import Counter
ivec_len = 16
data = b'foobarbaz'
print('message:     ',data)
key = bytes.fromhex('deadbeef' * 8)
c = AES.new(key,AES.MODE_CTR,counter=Counter.new(ivec_len*8,initial_value=1))
enc_data = c.encrypt(data)
print('\npycrypto enc:',enc_data)
c = AES.new(key,AES.MODE_CTR,counter=Counter.new(ivec_len*8,initial_value=1))
dec_data = c.encrypt(enc_data)
print('pycrypto dec:', dec_data)

from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend

ctr_init_val = b'\x00' * 15 + b'\x01'
print('\nhazmat ctr_init_val:',ctr_init_val)
cipher = Cipher(algorithms.AES(key),modes.CTR(ctr_init_val),backend=default_backend())
encryptor = cipher.encryptor()
ct = encryptor.update(data)
#ct = encryptor.update(data) + encryptor.finalize()
print('\nhazmat enc:  ', ct)
assert ct == enc_data
decryptor = cipher.decryptor()
res = decryptor.update(ct)
#res = decryptor.update(ct) + decryptor.finalize()
print('hazmat dec:  ',res)
