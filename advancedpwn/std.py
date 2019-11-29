from pwn import *
from advancedpwn import ida, strace
import os

def import_file(full_name, path):
    """Import a python module from a path. 3.4+ only.

    Does not call sys.modules[full_name] = path
    """
    from importlib import util

    spec = util.spec_from_file_location(full_name, path)
    mod = util.module_from_spec(spec)

    spec.loader.exec_module(mod)
    return mod

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".advancedpwn.py")
config = import_file("config", CONFIG_PATH)

def map_path(local_path):
    global config
    for key, val in config.path_map.items():
        local_path = local_path.replace(key, val)
    return local_path

def local(argv=[], host=None, port=None, gdbscript=None, *a, **kw):
    '''Execute the target binary locally'''
    global config
    exe = context.binary
    ssh_conf = None
    exe_path = exe.path
    if args.SSH:
        ssh_conf = config.shell
        exe_path = map_path(exe_path)
        ida_host = "localhost"
    if args.GDB:
        return gdb.debug([exe_path] + argv, ssh=ssh_conf, *a, **kw), None
    if args.IDA:
        return ida.debug([exe_path] + argv, ida_host=config.ida_host, ida_start_port=config.ida_port, ssh=ssh_conf)
    if args.STRACE:
        return strace.debug([exe_path] + argv, ssh=ssh_conf), None
    else:
        if ssh_conf is not None:
            return ssh_conf.process([exe_path] + argv, *a, **kw), None
        else:
            return process([exe_path] + argv, *a, **kw), None

def remote(argv=[], host=None, port=None, gdbscript=None, *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)