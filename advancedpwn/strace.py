from pwn import *
from pwnlib import util

def strace_cmd(pid):
    return ["strace", "-p", str(pid)]

def attach(target):
    from advancedpwn import create_ssh_cmd
    if isinstance(target, tubes.ssh.ssh_channel):
        if not target.pid:
            log.error("PID unknown for channel")

        shell = target.parent
        pid = target.pid
        
        cmd = create_ssh_cmd(shell)
        cmd += strace_cmd(pid)

        util.misc.run_in_new_terminal(' '.join(cmd))
    elif isinstance(target, tubes.process.process):
        pid = proc.pidof(target)[0]
        cmd = strace_cmd(pid)

        util.misc.run_in_new_terminal(' '.join(cmd))


def debug(args, exe=None, ssh=None, **kwargs):
    p = None
    if exe is None:
        exe = args[0]
    if ssh is not None:
        p = ssh.process(args, **kwargs)
    else:
        p = process(args, **kwargs)
    attach(p)
    return p