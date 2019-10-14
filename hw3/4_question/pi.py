import re
import hashlib

f = open('./pi1000000.txt','r')
pi= f.read()
f.close()

m = re.match(r'^(3\.\d*?12345)', pi)
# print('result:' + m.group(1))

x = hashlib.md5(m.group(1).encode('utf-8')).hexdigest()
print('md5 hash result:' + x)
