#!/usr/bin/env python3
"""apc.py - Control APC network power strip

Usage:
  apc.py [options] (on [<port>] | off [<port>] | reset [<port>] | list)
  apc.py [options] set-alias <name> <num>
  apc.py [options] rm-alias <name>
  apc.py [options] set-host <hostname>
  apc.py --help

Commands:
  on                     Turn port on [defaults to last port if empty]
  off                    Turn port off [default to last port if empty]
  reset                  Reset port [default to last port if empty]
  list                   List all ports, their aliases, and their status
  set-alias              Set an alias for a port number
  rm-alias               Remove alias for a port
  set-host               Set host of APC device via IP address or hostname
  --help                 Print this usage screen

Options:
  --config <filename>    Point to custom config file [default: ~/.config/apc/config.yaml]

"""
import re
import os
import sys
import yaml
import docopt
import os.path
import telnetlib
import json

# --------------- Application Entrypoint ---------------

def main():
    args = docopt.docopt(__doc__)
    config = ConfigFile(args['--config'])
    error = run_command(args, config)
    sys.exit(error)

# --------------- Command Handlers ---------------

def clear():
    os.system("clear")

def on_command(args, config):
    print("on command")
    config.read()
    port = args.get("<port>") or config.last_port
    port = int(port)
    if port is None:
        sys.stderr.write('Error: Please specify a port number.\n')
        return -1
    if not port == config.last_port:
        config.last_port = port
        config.write()
    print("I'm going to telnet to", config.hostname)
    print(" to instantly power on port", port)
    tn = telnetlib.Telnet('192.168.1.98')
    tn.set_debuglevel(9)
    tn.read_until(b'User Name : ', 5)
    tn.write(b'cor\r')
    tn.read_until(b'Password  : ', 5)
    tn.write(b'dev2020\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'2\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'%d\r' % port)
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'cancel :', 5)
    tn.write(b'YES\r')
    tn.read_until(b'continue...', 5)
    tn.write(b'\r')
    print('Power on upon outlet port', port, 'successful.')
    return 0

def off_command(args, config):
    print("off command")
    config.read()
    #port = args.get("<port>") or config.last_port
    port = None
    if port is None:
        # TODO: Send to stderror
        #sys.stderr.write(json.dumps(config.__init__, ensure_ascii=False, sort_keys=True, indent=4).encode('utf-8', 'replace'))
        sys.stderr.write('Error: %s\n' % 'Please specify a port number.')
        return -1
    #if not port == config.last_port:
    #    config.last_port = port
    #    config.write()
    print("I'm going to telnet to", config.hostname)
    print(" to instantly power off port", port)
    tn = telnetlib.Telnet('192.168.1.98')
    tn.set_debuglevel(9)
    tn.read_until(b'User Name : ', 5)
    tn.write(b'cor\r')
    tn.read_until(b'Password  : ', 5)
    tn.write(b'dev2020\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'2\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'%d\r' % port)
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'2\r')
    tn.read_until(b'cancel :', 5)
    tn.write(b'YES\r')
    tn.read_until(b'continue...', 5)
    tn.write(b'\r')
    print("Power off upon outlet port", port, "successful.")
    return 0

def reset_command(args, config):
    print("reset command")
    config.read()
    port = args.get("<port>") or config.last_port
    port = int(port)
    if port is None:
        sys.stderr.write('Error: %s\n' % 'Please specify a port number.')
        return -1
    if not port == config.last_port:
        config.last_port = port
        config.write()
    print("I'm going to telnet to", config.hostname)
    print(" to instantly reset", port)
    tn = telnetlib.Telnet('192.168.1.98')
    tn.set_debuglevel(9)
    tn.read_until(b'User Name : ', 5)
    tn.write(b'cor\r')
    tn.read_until(b'Password  : ', 5)
    tn.write(b'dev2020\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'2\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'%d\r' % port)
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>', 5)
    tn.write(b'3\r')
    tn.read_until(b'cancel :', 5)
    tn.write(b'YES\r')
    tn.read_until(b'continue...', 5)
    tn.write(b'\r')
    print("Power reset upon outlet port", port, "successful.")
    return 0


def list_command(args, config):
    print("list command")
    config.read()
    print("I'm listing current outlet status at", config.hostname)
    tn = telnetlib.Telnet('192.168.1.98')
    tn.set_debuglevel(9)
    tn.read_until(b'User Name : ') 
    tn.write(b'cor\r')
    tn.read_until(b'Password  : ')
    tn.write(b'dev2020\r')
    tn.read_until(b'<CTRL-L>')
    tn.write(b'1\r')
    tn.read_until(b'<CTRL-L>')
    tn.write(b'2\r')
    tn.read_until(b'<CTRL-L>')
    tn.write(b'1\r')
    data = tn.read_until(b'<ESC>') 
    matches = re.search(r'Device 1 +(ON|OFF)\r\n.*?Device 2 +(ON|OFF)\r\n.*?Device 3 +(ON|OFF)\r\n.*?Device 4 +(ON|OFF)\r\n.*?Device 5 +(ON|OFF)\r\n.*?Device 6 +(ON|OFF)\r\n.*?Device 7 +(ON|OFF)\r\n.*?Device 8 +(ON|OFF)', data.decode('utf-8'), re.MULTILINE)
    print(data.decode('utf-8'))
    print(matches.group(1,2,3,4,5,6,7,8))

def set_alias_command(args, config):
    print("set alias command")
    config.read()
    num = args.get("<port>")
    name = args.get("<name>")
    if name is None:
        sys.stderr.write('Error: %s\n' % 'Please specify a new alias name for this port.')
        return -1
        config.write()
    if num is None:
        sys.stderr.write('Error: %s\n' % 'Please specify a port for the alias name change.')
        return -1
        config.write()
    print("I'm going to telnet to", config.hostname)
    print(" to instantly reset", port)
    tn = telnetlib.Telnet('192.168.1.98')
    tn.set_debuglevel(9)
    tn.read_until(b'User Name : ')
    tn.write(b'cor\r')
    tn.read_until(b'Password  : ')
    tn.write(b'1\r')
    tn.write(b'2\r')
    tn.write(b'1\r')
    tn.write(b'1\r')
    tn.write(b'%d\r' % num)
    tn.write(b'2\r')
    tn.write(b'1\r')
    tn.read_until(b'Outlet Name : ')
    input('New Outlet Name :')

def rm_alias_command(args, config):
    print("rm alias command")

def set_host_command(args, config):
    print("set host command")

def run_command(args, config):
    """Find function pointer for command name and call it with args and
    config file object.  Return error code from the function, or -1 if the

    """
    commands = { 'on': on_command,
                 'off': off_command,
                 'reset': reset_command,
                 'list': list_command,
                 'set-alias': set_alias_command,
                 'rm-alias': rm_alias_command,
                 'set-host': set_host_command,
    }
    for command in commands:
        if not command in args:
            raise ValueError('Invalid command key %s' % command)
        if args[command]:
            return commands[command](args, config)
    raise ValueError('Must pass in at least one True command')


# --------------- Classes ---------------

class ConfigFile(object):
    """POD (Plain Old Data) class + a little bit of smarts"""
    def __init__(self, filename):
        """Must have a filename. All other fields start off as None except
        aliases, which starts as an empty dictionary

        """
        self.filename = os.path.expanduser(filename)
        self.hostname = None
        self.user = None
        self.password = None
        self.last_port = None
        self.description = None
        self.aliases = {}
        self.descriptions = {}
        self.__data = None

    def read(self):
        "Read config file from disk, decode yaml and populate fields"
        with open(self.filename, 'r') as handle:
            data = yaml.safe_load(handle)
            self.hostname = data.get('hostname')
            self.user = data.get('user')
            self.password = data.get('password')
            self.last_port = data.get('last_port')
            self.description = data.get('description')
            self.aliases = self._create_aliases(data.get('aliases'))
            self.descriptions = self._create_descriptions(data.get('aliases'))

    def write(self):
        "Write POD to config file in yaml format"
        file = open(self.filename, 'w')
        aliases = []
        for port in self.aliases:
            entry = { 'port' : port, 'name' : self.aliases[port], 'description' : self.descriptions[port]}
            aliases.append(entry)
        data = {'hostname' : self.hostname , 'user' : self.user ,
                'password' : self.password ,'last_port' : self.last_port ,
                'description' : self.description , 'aliases' : aliases }
        yaml.dump(data, file)

    def set_alias(self, num, name):
        "Add or overwrite a port alias"
        pass

    def rm_alias(self, name):
        """Remove a port alias.  Return True if we removed an existing alias,
        or False if nothing by that name was found.

        """
        for num in self.aliases:
            if self.aliases[num] == name:
                del self.aliases[num]
                return True
        return False

    def _create_aliases(self, yaml_list):
        """Turn list of dictionaries into a dictionary with the port number and alias
        """
        alias_dict = {}
        num = {}
        name = {}
        for entry in yaml_list:
            print(entry)
            num = entry.get('port')
            name = entry.get('name')
            if num is not None and name is not None:
                alias_dict[num] = name
        return alias_dict

    def _create_descriptions(self, yaml_list):
        """Turn list of dictionaries into a dictionary with the port number and description
        """
        description_dict = {}
        for entry in yaml_list:
            num = entry.get('port')
            description = entry.get('description')
            if num is not None and description is not None:
                description_dict[num] = description
        return description_dict

    def __str__(self):
        descr = f"""{{filename: '{self.filename}', \
hostname: '{self.hostname}', \
user: '{self.user}', \
password: '{self.password}', \
last_port: '{self.last_port}', \
description: '{self.description}', \
aliases: {{"""

        secondary_port = False
        for port in self.aliases:
            if secondary_port:
                descr += ", "
            secondary_port = True
            descr += f"{port}: '{self.aliases[port]}'"

        descr += "}, descriptions: {"
        secondary_port = False
        for port in self.descriptions:
            if secondary_port:
                descr += ", "
            secondary_port = True
            descr += f"{port}: '{self.descriptions[port]}'"
        descr += "}}"
        return descr

class Apc(object):
    def __init__(self, host=None, user=None, password=None, map=None):
        self.host = host or "apc"
        self.user = user or "apc"
        self.password = password or "apc"
        self.port_map = map or {}
        self.last_port = None

    def set_map(self, map):
        """Set port alias map by passing in a dictionary with number is key,
        and alias as value.

        """
        self.port_map = map

    def port_name(num):
        """Return port name/alias associated with port number.  Return
        'Unknown' if not found.

        """
        return self.port_map.get(num, 'Unknown')

    def port_num(name):
        """Return port number associated with port alias 'name'.  Return -1 if
        not found.

        """
        for num in self.port_map:
            if self.port_map[num] == name:
                return num
        return -1

    def on(self, port):
        pass

    def off(self, port):
        pass

    def reset(self, port):
        pass


if __name__ == "__main__":
    main()

