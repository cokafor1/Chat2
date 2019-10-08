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
    fileHandle = open(file_name, 'rb')

    if os.path.exists(file_name) == True:  ##client needs to know about how much data to expect
        file_size = str(os.path.getsize(file_name))
        try:
            serverSocket.sendto(file_size.encode(), anywhere)
        except socket.error:
                print("I couldn't send the file size.")

        if os.path.getsize(file_name) < 2000:
            new_fileHandle = fileHandle.read()
            serverSocket.sendto(new_fileHandle, anywhere)
            print(new_fileHandle)
        else:
            new_fileHandle = fileHandle.read(2048)
            count = 0
            totalpackets = (int(file_size) / 2048) #number of packets to sent = size of the file / buffer size (size of packets)
            while count < totalpackets: 
                serverSocket.sendto(new_fileHandle, anywhere)
                count += 1
                print("%d packets sent (%d bytes)." % (count, (count * 2048)))
            new_fileHandle = fileHandle.read(2048)
            fileHandle.close()
    else: 
        print('File does not exist in directory.')
        serverSocket.sendto(("File is not found").encode(), anywhere) 
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            #main()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            #main()


#def put file: 
def putFile(file_name): #receive command, decode, check if file exists, open encode, send
    print(locals())
    try:
        if os.path.exists(file_name) == True: # check if file in directory already
            print("File already exists in directory. Maybe you should check before deciding to waste resources.")
        
        else:
            message = "Okay, I can receive %s" % (file_name)  
            serverSocket.sendto(message.encode(), anywhere) #send get command to server
            serverReceiveFile = open(file_name, 'wb')
        
            (incoming_file_size, backthere) = serverSocket.recvfrom(2048)
            file_size = int(incoming_file_size.decode()) #get incoming file size and serve as acknowledgment
            print("Receiving file of size %s bytes." % file_size)

            count = 0
            totalpackets = (int(file_size) / 2048) #number of packets to sent = size of the file / buffer size (size of packets)
            while count < totalpackets: #write to file
                (clientReply, backthere) = serverSocket.recvfrom(2048)
                count += 1
                serverReceiveFile.write(clientReply)
            serverReceiveFile.close()
            
        if os.path.getsize(serverReceiveFile.read()) != file_size: getFile(file_name)
        else: main()
    except socket.error:
        print ("Took too long or something....")
        #main()


#def rename file:
def renameFile(old_file_name, new_file_name): #receive, decode, and rename on server.
    try:
        message = "Okay, let me see what I can do for you...."
        serverSocket.sendto(message.encode(), anywhere) #send get command to server
    except:
        message = "File couldn't be renamed at this time."
        print(message)
        serverSocket.sendto(message.encode(), anywhere)
        #main()

    if os.path.exists(file_name) == True: # check if files are in directory
            os.rename(oldFile, newFile)
            serverSocket.sendto("Files were renamed successfully.".encode(), anywhere)
    else:
        print("These files arent here.")
        serverSocket.sendto(("These files arent here.").encode(), anywhere) 
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            #main()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            #main()
        
   

#def list:
def listFiles():
    listing = os.listdir()
    for x in listing:
        #time.sleep(1)
        serverSocket.sendto(x.encode(), anywhere)
        print(x)

#def exit:
def exit():
    sys.exit()

def main():
    print()
    print()

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
            print("Command not in options.")
            serverSocket.sendto(("Client is right, I haven't been told how to handle this %s command. Sorry." % message).encode(), anywhere) #how do I know this for client address?
        elif len(parse_msg) == 2:
            file_name = parse_msg[1]
            options.get(command)(file_name)
        elif len(parse_msg) == 3:
            old_file_name = parse_msg[1]
            new_file_name = parse_msg[2]
            options.get(command)(old_file_name, new_file_name)
        else: options.get(command)()

        
    
if __name__ == "__main__": 
    main()
    