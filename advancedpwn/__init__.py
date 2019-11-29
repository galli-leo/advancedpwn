from pwn import *
import advancedpwn.ida
import advancedpwn.strace
import advancedpwn.std

def create_ssh_cmd(shell):
    cmd = ['ssh', '-C', '-t', '-p', str(shell.port), '-l', shell.user, shell.host]
    if shell.password:
        if not misc.which('sshpass'):
            log.error("sshpass must be installed to debug ssh processes")
        cmd = ['sshpass', '-p', shell.password] + cmd
    if shell.keyfile:
        cmd += ['-i', shell.keyfile]
    return cmd