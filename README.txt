This program is running on Python version 3.6.4 (could not use 3.5).

The program consists of two files, client.py and server.py.

To run each program, I specified their path and used the Python open(), exec(), and read() commands in the
interactive Python shell. The following command for example will run the programs-

>>> exec(open("C:\\Users\\client.py").read())

Alternatively, you can also use the command line and from the directory in which you Python installation is located, run-
 
>>> python [filename].py {function}

All necessary files were saved in their directories. It was recommended to use two
separate directories for the server and client files. You can simply add files to call wherever they are
needed.

When prompted, use the command line to input the arguments. *Note that during first run, there may be a hang after receiving input 
of IP Address. Simply run program again to get around this.