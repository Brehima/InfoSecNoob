#! /usr/bin/python

#fuzz="A"*80+"B"*4
#print fuzz
#we can cotrol EIP at offset 80
#since we only have left a small place we need to use ret2libc
#after info proc mappings we found that libc start on address 0xb7ecffb0
#first we will need to find the right offset of ''/bin/sh''  11f3bf
