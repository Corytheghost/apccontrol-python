import os
import telnetlib

tn= telnetlib.Telnet('192.168.1.98')

#tn.set_debuglevel(9)

tn.read_until(b'Username : \r', 5)
tn.write(b'cor\r')

tn.read_until(b'Password  : \r', 5)
tn.write(b'dev2020\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'1\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'2\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'1\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'1\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'1\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'1\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'YES\r')

tn.read_until(b'<CTRL-L>\r', 5)
tn.write(b'\r')

#print("read"),tn.read_until(b'<CTRL-L>', 5)