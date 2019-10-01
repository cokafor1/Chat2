import socket
import ipaddress
import sys
import argparse
import getopt
import os
import time



#Creating UDP socket-
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet is address family, UDP protocol


#defining functions to use in cases mapping. These functions do not do much, simply send string input file name to server.
def getFile(file_name): #ask for file, if file doesn't exist, print message and return to main()
    print(locals())
    if os.path.exists(args.file_name) == True: 
        fileHandle = open(args.file_name, 'rb').read()
        clientSocket.sendto(fileHandle, server) #note- if not for 'rb' mode, fileHandle would need to be fileHandle.encode() here to send as binary encoded message
        serverResponse, serverAddress = clientSocket.recvfrom(5000)
    else: 
        print("File does not exist in directory.")
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            getFile(file_name)
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            main()

def putFile(file_name):
    print(locals())
   # putFile = input("Enter the file with extension you would like to put- ")
    if os.path.exists(file_name) == True: 
        fileHandle = open("file_name", 'rb')
        clientSocket.sendto(fileHandle.encode(), server)
    else: 
        print('File does not exist in directory.')
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            getFile()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            main()

def renameFile(old_file_name, new_file_name): #rename the files using two arguments
    #this should simply be sending a message as inputs/strings
    while len(args) == 2:
            oldFile = old_file_name.encode()
            newFile = new_file_name.encode()
    #check argument numbers
    print(locals())
    clientSocket.sendto(oldFile.encode(), server)
    clientSocket.sendto(newFile.encode(), server)

def listFiles(): #implement list as a boolean function where presumed true. Send value to server to take proper action.
    message = "list"
    clientSocket.sendto(message.encode(), server) #send list command to server
    (replyFromServer, Address) = clientSocket.recvfrom(5000)
    print(replyFromServer, '\n', sep = '')


def exit(): #simply send 'exit' string to server and allow it to handle
    message = "exit"
    #clientSocket.sendto(message.encode(), server)
    clientSocket.close()
    print('Exit on user command.')
    time.sleep(3)
    sys.exit()


def action(): #how to retrieve arguments......there should be a better way.
    action = input('What would you like to do?').split()
    if len(action) >= 4:#use loop to append command line user inputs to action list. Make list no more than four values
       print('This program only supports one command and up to two arguments, but you can try again.')
       action()
    elif len(action) == 2:
        file_name = action[1]
    elif len(action) == 3:
        old_file_name = action[2]
        new_file_name = action[3]
    return

if __name__ == "__main__":
    #Server address and port information-
    parse = argparse.ArgumentParser(prog = 'client')
    parse.add_argument('Address', nargs = 1, type = ipaddress.ip_address, help = "Enter IP Address.")
    parse.add_argument('Port', nargs = 1, type = int, help = "Enter port number above 1024.")
        
    args = vars(parse.parse_args())

    #TO DO- this loop ensures that desired port number is not too popular and is integer. Also tests number of arguments.
    #while True: 
    #    if (('Port' <= 1024):
    #        print("Clearly","  ", args.get('Port'), "  ", "is not above 1024.", sep = "")
    #        Port = int(input("Enter port number above 1024- "))
    #        continue
    #    if len(sys.argv) > 3:
    #        print('Too many arguments! Did you not read that it said only TWO arguments? Minus 10%. Please try again.')
    #    else: break

    
    server = (args.get('Address'), args.get('Port'))

    #action()
 
    #a dictionary, using keys to execute desired function specified in action variable
    options = {
    'get': getFile,
    'put': putFile,
    'rename': renameFile,
    'list': listFiles,
    'exit': exit }.get()() #needs to have user inputs from the command line

    if command not in options: 
        message = "Not in options but I will give to server to handle."
        clientSocket.sendto(message.encode(), server)  
    
    clientSocket.close()
