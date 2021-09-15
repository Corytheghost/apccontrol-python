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
import os
import sys
import yaml
import docopt
import os.path
import telnetlib

# --------------- Application Entrypoint ---------------

def main():
    args = docopt.docopt(__doc__)
    config = ConfigFile(args['--config'])
    error = run_command(args, config)
    sys.exit(error)

# --------------- Command Handlers ---------------

def on_command(args, config):
    print("on command")
    config.read()
    port = args.get("<port>") or config.last_port
    if port is None:
        # TODO: Send to stderror
        print('Please specify a port number.')
        return -1
    if not port == config.last_port:
        config.last_port = port
    print("I'm going to telnet to", config.hostname)
    print(" to port", port)
    port = int(port)
    print("I'm going to telnet to", config.hostname)
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
    print(config)
    config.write()

def clear():
    os.system("clear")

def off_command(args, config):
    print("off command")
    config.read()

def reset_command(args, config):
    print("reset command")
    config.read()
    #config.read()
    #port = args.get("<port>") or config.last_port
    #if port is None:
    #    print('Please specify a port number')
    #    return -1
    #if not port == config.last_port:
    #    config.last_port = port
    #print("I'm going to telnet to", config.hostname)
    #tn = telnetlib.Telnet('192.168.1.98')
    #tn.read_until(b'User Name : ', 5)
    #time.sleep(2)
    #tn.write(b'cor\n')
    #print(config)

def reset_command(args, config):
    print("reset command")
    #config.read()
    #port = args.get("<port>") or config.last_port
    #if port is None:
    #    print('Please specify a port number')
    #    return -1
    #if not port == config.last_port:
    #    config.last_port = port
    #print("I'm going to telnet to", config.hostname)
    #tn = telnetlib.Telnet('192.168.1.98')
    #tn.read_until(b'User Name : ', 5)
    #time.sleep(2)
    #tn.write(b'cor\n')
    #print(config)

def list_command(args, config):
    print("list command")
    config.read()

def set_alias_command(args, config):
    print("set alias command")

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

