import socket
import ipaddress
import sys
import argparse
import getopt
import os
import time

#Creating UDP socket-
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet is address family, UDP protocol
clientSocket.setblocking(0)

#defining functions to use in cases mapping. These functions do not do much, simply send string input file name to server.

def getFile(file_name): #ask for file, if file doesn't exist, print message and always return to main()
    print(locals())

    if os.path.exists(file_name) == True: # check if file in directory already
        print("File already exists in directory. Maybe you should check before deciding to waste resources.")
    else:
        message = "get %s" % (file_name)  
        clientSocket.sendto(message.encode(), server) #send get command to server
        clientReceiveFile = open(file_name, 'wb')
        time.sleep(1)
        try:
            (incoming_file_size, somewhere) = clientSocket.recvfrom(2048)
            file_size = incoming_file_size.decode() #get incoming file size and serve as acknowledgment
            print("Receiving file of size %s bytes." % file_size)
        except:
            print("Information not received by server side.")

        try:
            (serverReply, somewhere) = clientSocket.recvfrom(2048)
            print(serverReply.decode())
        except:
            pass

       # while (serverReply): #write to file
              #  clientReceiveFile.write(serverReply)
             #   clientReceiveFile.close()
            #    main()
                #except socket.error:
                 #    print ("Took too long or something....")
                 #    print()
                 #    main()

def putFile(file_name): #send the file to server
    print(locals())
    size = 2048
    sent = 0
    if os.path.exists(file_name) == True: 
        fileHandle = open(file_name, 'rb').read(size)
        print(fileHandle)
        while sent < os.path.getsize(file_name):
            clientSocket.sendto(fileHandle, server)
            sent += size
            print('Sent %s' % sent)
    else: 
        print('File does not exist in directory.')
        try:
            newdir = input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-")
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            main()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            main()
    try:
        clientSocket.settimeout(8)
        (serverReply, Address) = clientSocket.recvfrom(5000)
        print(serverReply, '\n', sep = '')
    except socket.error:
        print ("Took too long....")
        main()

def renameFile(old_file_name, new_file_name): #rename the files using two arguments
    while len(args) == 2:
            oldFile = old_file_name.encode()
            newFile = new_file_name.encode()
    clientSocket.sendto(oldFile.encode(), server)
    clientSocket.sendto(newFile.encode(), server)
    try:
        clientSocket.settimeout(8)
        (serverReply, Address) = clientSocket.recvfrom(5000)
        print(serverReply, '\n', sep = '')
    except socket.error:
        print ("Took too long....")
        main()

def listFiles(): 
    message = "list"
    clientSocket.sendto(message.encode(), server)
    time.sleep(1)
    (serverReply, somewhere) = clientSocket.recvfrom(2048)
    print(serverReply.decode(), '\n', sep = '')
    main()
    

def exit(): #simply send 'exit' string to server and allow it to handle
    message = "exit"
    clientSocket.sendto(message.encode(), server)
    clientSocket.close()
    print('Exit on user command.')
    time.sleep(3)
    sys.exit()


def action(): #how to retrieve arguments......there should be a better way.
    
    print("Your options are the following-")
    print("get [file_name]")
    print("put [file_name]")
    print("rename [old_file_name] [new_file_name]")
    print("list")
    print("exit")

    action = input('What would you like to do?').split()

    if len(action) >= 4:#use loop to append command line user inputs to action list. Make list no more than four values
       print('This program only supports one command and up to two arguments, but you can try again.')
       action()
    return action

def main():
    print("")
    #Server address and port information-
    parse = argparse.ArgumentParser(prog = 'client')
    parse.add_argument('Address', nargs = 1, type = ipaddress.ip_address, help = "Enter IP Address.")
    parse.add_argument('Port', nargs = 1, type = int, help = "Enter port number above 1024.")
        
    args = parse.parse_args()

 

    global server
    server = (args.Address[0]._explode_shorthand_ip_string(), args.Port[0])

    choice = action()
    command = str(choice[0])

    #a dictionary, using keys to execute desired function specified in action variable
    options = {
    'get': getFile,
    'put': putFile,
    'rename': renameFile,
    'list': listFiles,
    'exit': exit } #needs to have user inputs from the command line

    if command not in options: 
        print("Not in options but I will give to server to handle. Trust me......")
        #clientSocket.sendto(command.encode(), server)
        #time.sleep(2)
        #(error, server) = clientSocket.recvfrom(2048)
        #print(error.decode())
        #print(1)
        main()
    elif len(choice) == 2:
        file_name = choice[1]
        options.get(command)(file_name)
    elif len(choice) == 3:
        old_file_name = choice[1]
        new_file_name = choice[2]
        options.get(command)(old_file_name, new_file_name )
    else: options.get(command)()

    #clientSocket.close()

if __name__ == "__main__": 
    main()
