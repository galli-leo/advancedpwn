# advancedpwn

Advanced `pwntools` stuff.

Currently includes:

* `ida` module:
    * `ida.debug()`: similarily to `gdb.debug` allows you to start a process and automatically attach ida to it
    * `ida.attach()`: similar to `gdb.attach` allows you to attach ida to a running process
* `strace` module:
    * `strace.debug()`: similar to `gdb.debug` allows you to start a process and automatically attach strace to it in a new terminal window
    * `strace.attach()`: similar to `gdb.attach` allows you to attach strace to a running process in a new terminal window
* `std` module: provides standard functions present in every pwntools script, such as `start`. This should help declutter your exploit script. It also automatically handles using SSH to run stuff. e.g. you can run your exploit script on your main os and using ssh pwntools will do everything in the VM.

## Installation

Probably can install using:
```bash
python3 -m pip install git+https://github.com/galli-leo/advancedpwn.git
```

## Usage of `std` module

Your exploit script should look like this:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from advancedpwn import *
from advancedpwn.std import *

import re
context.arch = "amd64"

exe = context.binary = ELF('./pwn')
context.terminal = ["my_script_to_launch_new_terminal"]
#libc = context.binary = ELF('/lib/i386-linux-gnu/libc.so.6')

print(args.HOST, args.PORT)
host = args.HOST or 'example.com'
port = int(args.PORT or 1337)

io, proxy = start(host=host, port=port)
io.interactive()
```

You should have the following file under `~/.advancedpwn.py`:
```python
from pwn import *
# Configuration for IDA
ida_host = "10.10.10.1" # IP to your machine as seen from ssh
ida_port = 31337 # Start port of IDA server

# Configuration for ssh to VM
shell = ssh("user", "hostname", 22, keyfile="/path/to/keyfile")
# needed to map paths between Host and VM
path_map = {
    "/Users/leonardogalli/Code/CTF/shared" : "/home/vagrant/shared"
}
```

Examples:

```bash
python exploit.py # run script against server
python exploit.py LOCAL # run script locally
python exploit.py LOCAL SSH # run script against binary launched via ssh
python exploit.py LOCAL SSH IDA # run script against binary launched via ssh and also attach ida
python exploit.py LOCAL IDA # run script locally and also attach ida
python exploit.py LOCAL SSH STRACE # run script against binary launched via ssh and also attach strace
```


## Usage of IDA module
Install `ida_server.py` inside IDA (just copy it to the plugins directory).
Then you can use the ida module. If you are using `std` module as well, it should be as easy as:

```bash
python3 exploit.py LOCAL IDA
```

**Note:** For this to work, you must have the correct debug_server running on the system where the script is executing the binary (e.g. if via SSH, then on the VM). Also you must have configured the IDA instance that has your binary open to be able to connect to that server (e.g. selected Linux Server, configured host and port correctly).