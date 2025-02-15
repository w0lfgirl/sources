# -*- coding:utf8 -*-

# Supports python2 & python3
# Name   : PyObfuscate - Simple Python Code Obfuscator
# Author : HTR-TECH
# Date   : Sun Jul 19 00:19:27 2021

# Import Modules
import os
import sys
import zlib
import time
import base64
import marshal
import py_compile
from pystyle import *
m = Colors.StaticMIX((Col.purple, Col.white))
w = Col.white
s = m + '[' + w
k = m + ']' + w
# Select raw_input() or input()
if sys.version_info[0]==2:
    _input = "raw_input('%s')"
elif sys.version_info[0]==3:
    _input = "input('%s')"
else:
    sys.exit("\n Your Python Version is not Supported!")

# Encoding
zlb = lambda in_ : zlib.compress(in_)
b16 = lambda in_ : base64.b16encode(in_)
b32 = lambda in_ : base64.b32encode(in_)
b64 = lambda in_ : base64.b64encode(in_)
mar = lambda in_ : marshal.dumps(compile(in_,'<x>','exec'))
note = "# encoded by //antisofters.\n# -------------------------\n"

def menu(): # Program Menu
    print(f"""
{s}01{k} Encode Marshal
{s}02{k} Encode Zlib
{s}03{k} Encode Base16
{s}04{k} Encode Base32
{s}05{k} Encode Base64
{s}06{k} Encode Zlib,Base16
{s}07{k} Encode Zlib,Base32
{s}08{k} Encode Zlib,Base64
{s}09{k} Encode Marshal,Zlib
{s}10{k} Encode Marshal,Base16
{s}11{k} Encode Marshal,Base32
{s}12{k} Encode Marshal,Base64
{s}13{k} Encode Marshal,Zlib,B16
{s}14{k} Encode Marshal,Zlib,B32
{s}15{k} Encode Marshal,Zlib,B64
{s}16{k} Simple Encode
{s}17{k} Exit
""")

class FileSize: # Gets the File Size
    def datas(self,z):
        for x in ['Byte','KB','MB','GB']:
            if z < 1024.0:
                return "%3.1f %s" % (z,x)
            z /= 1024.0
    def __init__(self,path):
        if os.path.isfile(path):
            dts = os.stat(path).st_size
            print(f"{s}Encoded File Size{k} >  %s\n" % self.datas(dts))
# FileSize('rec.py')

# Encode Menu
def Encode(option,data,output):
    s = m + '[' + w
    k = m + ']' + w
    loop = int(eval(_input % f"{s}Encode Count{k} > "))
    if option == 1:
        xx = "mar(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__[::-1]);"
    elif option == 2:
        xx = "zlb(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__[::-1]);"
    elif option == 3:
        xx = "b16(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b16decode(__[::-1]);"
    elif option == 4:
        xx = "b32(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b32decode(__[::-1]);"
    elif option == 5:
        xx = "b64(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b64decode(__[::-1]);"
    elif option == 6:
        xx = "b16(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 7:
        xx = "b32(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));"
    elif option == 8:
        xx = "b64(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));"
    elif option == 9:
        xx = "zlb(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));"
    elif option == 10:
        xx = "b16(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));"
    elif option == 11:
        xx = "b32(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));"
    elif option == 12:
        xx = "b64(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));"
    elif option == 13:
        xx = "b16(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));"
    elif option == 14:
        xx = "b32(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));"
    elif option == 15:
        xx = "b64(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));"
    else:
        sys.exit("\n Invalid Option!")
    
    for x in range(loop):
        try:
            data = "exec((_)(%s))" % repr(eval(xx))
        except TypeError as s:
            sys.exit(" TypeError : " + str(s))
    with open(output, 'w') as f:
        f.write(note + heading + data)
        f.close()

# Special Encode
def SEncode(data,output):
    for x in range(5):
        method = repr(b64(zlb(mar(data.encode('utf8'))))[::-1])
        data = "exec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(%s[::-1]))))" % method
    z = []
    for i in data:
        z.append(ord(i))
    sata = "_ = %s\nexec(''.join(chr(__) for __ in _))" % z
    with open(output, 'w') as f:
        f.write(note + "exec(str(chr(35)%s));" % '+chr(1)'*10000)
        f.write(sata)
        f.close()
    py_compile.compile(output,output)

# Main Menu
def MainMenu():
    try:
        menu()
        try:
            option = int(eval(_input % f"{s}Option{k} > "))
        except ValueError:
            sys.exit("\n Invalid Option !")
        
        if option > 0 and option <= 17:
            if option == 17:
                sys.exit("\n Thanks For Using this Tool")
        else:
            sys.exit('\n Invalid Option !')
        try:
            file = eval(_input % f"{s}File Name{k} > ")
            data = open(file).read()
        except IOError:
            sys.exit("\n File Not Found!")
        
        output = input(f"{s}output{k} > ")
        if option == 16:
            SEncode(data,output)
        else:
            Encode(option,data,output)
        print(f"{s}Saved as{k} > %s" % output)
        FileSize(output)
    except KeyboardInterrupt:
        time.sleep(1)
        sys.exit()

if __name__ == "__main__":
    MainMenu()
