#! python3
import os
import sys
import yaml
import docopt
import os.path
import telnetlib

tn= telnetlib.Telnet('192.168.1.98')

# --------------- Application Entrypoint ---------------

tn.set_debuglevel(9)

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
    #prog = __file__
    #directory = os.path.dirname(os.path.abspath(prog))
    #print(os.path.join(directory, 'devconfig.yml'))
    #args = docopt.docopt(__doc__)
    #print(args) # TODO: remove this line - initial debug ONLY
    #config = ConfigFile(args['--config'])
    #error = run_command(args, config)
    #sys.exit(error)
