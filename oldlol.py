import re
import hashlib

from base64 import b85decode as b85
from pystyle import Center, Colors, Colorate, System, Write
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from pystyle import *
p = Colors.StaticMIX((Col.purple, Col.white))
s = p + "[" + Col.white
k = p + "]" + Col.white 
file = input(f"{s}input{k} > ")

def decrypt_string(value):
    try:
        try:
            def IIlIIIIIllIlllIIII(IIllIlllIllIllIIlI):
                return unpad(AES.new(hashlib.sha256(str(list(value)[0][0] + list(value)[1][0]).encode()).digest()[:24], AES.MODE_CBC, IIllIlllIllIllIIlI[:AES.block_size]).decrypt(IIllIlllIllIllIIlI[AES.block_size:]), AES.block_size).decode()
            return (IIlIIIIIllIlllIIII(value[1][2]))
        except:
            def IIlIIIIIllIlllIIII(IIllIlllIllIllIIlI):
                return unpad(AES.new(hashlib.sha256(str(list(value)[0][0] + list(value)[1][0][:-1]).encode()).digest()[:24], AES.MODE_CBC, IIllIlllIllIllIIlI[:AES.block_size]).decrypt(IIllIlllIllIllIIlI[AES.block_size:]), AES.block_size).decode()
            return (IIlIIIIIllIlllIIII(value[1][2]))
    except:
        def lIIIIIIllIlIIlIlIl(IIllIlllIllIllIIlI, IlllIlllIIIIlIIIll):
            IIllIlllIllIllIIlI = b85(IIllIlllIllIllIIlI)
            (IlllIlllIIIIlIIIll, IlIlllllllIIlIIlII) = llIIIIllIIIllIllIl(IlllIlllIIIIlIIIll, IIllIlllIllIllIIlI[:8])
            return AES.new(IlllIlllIIIIlIIIll, AES.MODE_CFB, IlIlllllllIIlIIlII).decrypt(IIllIlllIllIllIIlI[8:]).decode()

        def llIIIIllIIIllIllIl(lIllIIlIlIlIlIlIll, IlIIlIIIIIIIlIIllI):
            IllIllIllIIllllllI = hashlib.pbkdf2_hmac('sha256', lIllIIlIlIlIlIlIll.encode(), IlIIlIIIIIIIlIIllI, 100000)
            return (IllIllIllIIllllllI[:16], IllIllIllIIllllllI[16:])
        return (lIIIIIIllIlIIlIlIl(list(value.values())[0], list(value.keys())[0][1:-1]))
    
def find_multiline_value(lines, key):
    value_lines = []
    value_found = False
    
    for line in lines:
        if value_found:
            if line.strip() == '' or re.match(r'\w+\s*=', line):
                break
            value_lines.append(line.strip())
        else:
            match = re.search(rf'{key}\s*=\s*(.*)', line)
            if match:
                value_lines.append(match.group(1).strip())
                value_found = True

    if value_lines:
        return ' '.join(value_lines)
    return None

with open(file, "r", encoding="utf-8") as f:
    lines = f.readlines()

    value_str = find_multiline_value(lines, 'pyobfuscate')
    if not value_str:
        value_str = find_multiline_value(lines, 'obfuscate')

    content_deobfuscated = decrypt_string(eval(value_str))
    oute = input(f"{s}output{k} > ")
    with open(oute, "w", encoding="utf-8") as f:
        f.write(content_deobfuscated)
print(f"{s}done{k}")
