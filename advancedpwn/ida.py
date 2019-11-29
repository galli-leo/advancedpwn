from pwn import *
import xmlrpc.client
import os


def create_client(host, port):
    return xmlrpc.client.ServerProxy("http://{}:{}/".format(host, port))


def find_server(host, start_port, binary_path):
    for port in range(start_port, start_port + 10):
        try:
            proxy = create_client(host, port)
            filepath = proxy.get_input_file_path()
            just_file = os.path.basename(filepath)
            if just_file == os.path.basename(binary_path) or os.path.samefile(filepath, binary_path):
                return proxy
            log.debug("File open in IDA instance does not match binary_path, trying others")
        except Exception as e:
            log.debug("Had error when trying to connect to ida instance: %s", e)
            pass


def attach(process, ida_host, ida_start_port, binary_path):
    proxy = find_server(ida_host, ida_start_port, binary_path)
    if proxy is None:
        log.error("Could not find running IDA instance with correct binary path!")
    print("PID: {process.pid}: ", process.pid)
    proxy.attach_process(process.pid, -1)
    return proxy


def debug(args, ida_host = "localhost", ida_start_port = 31337, exe=None, ssh=None, **kwargs):
    p = None
    if exe is None:
        exe = args[0]
    if ssh is not None:
        p = ssh.process(args, **kwargs)
    else:
        p = process(args, **kwargs)
    print(exe)
    proxy = attach(p, ida_host, ida_start_port, exe)
    return p, proxy
    