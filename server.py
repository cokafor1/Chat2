import socket
import ipaddress
import sys
import argparse
import getopt
import os
import time

#Client address and port information-
Address = '127.0.0.1'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#def get file
def getFile(file_name): #receive command, decode, check if file exists, open encode, send
    print(file_name) #to remove
    #serverSocket.sendto(("get %s" % file_name).encode(), anywhere)
    fileHandle = open(file_name, 'rb')

    if os.path.exists(file_name) == True:  ##client needs to know about how much data to expect
        file_size = str(os.path.getsize(file_name))
        try:
            serverSocket.sendto(file_size.encode(), anywhere)
        except OSError:
                pass

        if os.path.getsize(file_name) < 2000:
            new_fileHandle = fileHandle.read()
            serverSocket.sendto(fileHandle, anywhere)
            print(new_fileHandle)
        else:
            new_fileHandle = fileHandle.read(2048)
            count = 0
            totalpackets = (file_size / 2048) #number of packets to sent = size of the file / buffer size (size of packets)
            while count < totalpackets: 
                serverSocket.sendto(new_fileHandle, anywhere)
                count += 2048
                print("%d packets sent (%d bytes)." % ((count/2048), (count/2048) * 2048))
            new_fileHandle = fileHandle.read(2048)
            fileHandle.close()
    else: 
        print('File does not exist in directory.')
        serverSocket.sendto(("File is not found").encode(), anywhere) 
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            main()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            main()


#def put file: 
def putFile(file_name): #receive command, decode, check if file exists, open encode, send
    (file_name, (Address,Trop)) = serverSocket.recvfrom(6000)
    sFile = file_name.decode()
    if os.path.exits(sFile) == False: 
        fileHandle = open(sFile, 'rb')
        fileHandle.write(sFile, 'wb')
        fileHandle.close()
        serverSocket.sendto(fileHandle.encode(), Address)
    else: 
        reply = "File already exists in directory."
        serverSocket.sendto(reply.encode(), Address)

#def rename file:
def renameFile(old_file_name, new_file_name): #receive, decode, and rename on server.
    (old_file_name, (Address,Trop)) = serverSocket.recvfrom(6000)
    (new_file_name, (Address,Trop)) = serverSocket.recvfrom(6000)
    oldFile = old_file_name.decode()
    newFile = new_file_name.decode()
    os.rename(oldFile, newFile)
    serverSocket.sendto(newFile.encode(), Address)

#def list:
def listFiles():
    listing = os.listdir()
    for x in listing:
        serverSocket.sendto(x.encode(), anywhere)
        time.sleep(1)

#def exit:
def exit():
    print('POOP')
    sys.exit()

def main():

    parse = argparse.ArgumentParser(prog = 'server')
    parse.add_argument('Port', nargs = 1, type = int, help = "Enter port number above 1024.")
    
    args = parse.parse_args()

    Port = args.Port[0]

    serverSocket.bind(("", Port))

    #a dictionary, using keys to execute desired function specified in action variable #if message received is x, jump to function
    options = {
    'get': getFile,
    'put': putFile,
    'rename': renameFile,
    'list': listFiles,
    'exit': exit } #needs to have user inputs from the command line
    
    
    while True:
        print("Ready!")

        global anywhere
        (message, anywhere) = serverSocket.recvfrom(2048)

        parse_msg = message.decode().split()
        command = parse_msg[0]

        if command not in options: 
            serverSocket.sendto(("Client is right, I haven't been told how to handle this command. Sorry." % command).encode(), anywhere) #how do I know this for client address?
            break
        elif len(parse_msg) == 2:
            file_name = parse_msg[1]
            options.get(command)(file_name)
        elif len(parse_msg) == 3:
            old_file_name = parse_msg[1].encode()
            new_file_name = parse_msg[2].encode()
            options.get(command)(old_file_name, new_file_name)
        else: options.get(command)()

        
    
if __name__ == "__main__": 
    main()
    
