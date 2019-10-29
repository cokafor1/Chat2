import socket, ipaddress, sys, argparse, os, time, imghdr, base64

#Creating UDP socket-
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet is address family, UDP protocol
clientSocket.setblocking(0)

#defining functions to use in cases mapping. These functions do not do much, simply send string input file name to server.

def getFile(file_name): #ask for file, if file doesn't exist, print message and always return to main()
    print(locals())
    try:
        if os.path.exists(file_name) == True: # check if file in directory already
            print("File already exists in directory. Maybe you should check before deciding to waste resources.")
        else:
            message = "get %s" % (file_name)  
            clientSocket.sendto(message.encode(), server) #send get command to server
            clientReceiveFile = open(file_name, 'wb')
        
            (incoming_file_size, rightthere) = clientSocket.recvfrom(4096) #why use new address?
            file_size = int(incoming_file_size.decode()) #get incoming file size and serve as acknowledgment
            print("Receiving file of size %s bytes." % file_size)
            time.sleep(1)

            count = 0
            totalpackets = (int(file_size) / 2048) #number of packets to sent = size of the file / buffer size (size of packets)
            if 'jpg' in file_name:
                while count < totalpackets: #write to file
                    (serverReply, rightthere) = clientSocket.recvfrom(2048)
                    time.sleep(.5)
                    count += 1
                    print(count)
                    clientReceiveFile.write(base64.b64decode(serverReply.decode()))
                    type(clientReceiveFile.write(base64.b64decode(serverReply.decode())))
            else:
                while count < totalpackets: #write to file
                    (serverReply, rightthere) = clientSocket.recvfrom(1024)
                    count += 1
                    print(count)
                    clientReceiveFile.write(serverReply)
            print(1)
            clientReceiveFile.close()
            main()

        #if os.path.getsize(clientReceiveFile.read()) != file_size: getFile(file_name)
        #else: main()
    except socket.error:
            print ("Took too long or something....")
    
        

def putFile(file_name): #send the file to server
    fileHandle = open(file_name, 'rb')
    
    if os.path.exists(file_name) == True:  
        try:
            message = "put %s" % (file_name)  
            clientSocket.sendto(message.encode(), server) #send get command to server
            time.sleep(1)
        except socket.error:
                print("I couldn't send the message.")

        file_size = str(os.path.getsize(file_name)) ##client needs to know about how much data to expect
        try:
            clientSocket.sendto(file_size.encode(), server)
        except socket.error:
                print("I couldn't send the file size.")

        if os.path.getsize(file_name) < 2000: 
            new_fileHandle = fileHandle.read()
            clientSocket.sendto(new_fileHandle, server)
            main()
        else:
            new_fileHandle = fileHandle.read(1024)
            count = 0
            totalpackets = (int(file_size) / 1024) #number of packets to sent = size of the file / buffer size (size of packets)
            while count < totalpackets: 
                clientSocket.sendto(new_fileHandle, server)
                count += 1
                print("%d packets sent (%d bytes)." % (count, (count * 1024)))
            new_fileHandle = fileHandle.read(1024)
            fileHandle.close()
            main()
    else: 
        print('File does not exist in directory.')
        clientSocket.sendto(("File is not found").encode(), server) 
        try:
            newdir = print(input("You can specify the correct directory (Don't forget proper '\\' escape characters.)-"))
            os.chdir(newdir)
            print("Okay, let's go back to try get the file again.")
            main()
        except OSError:
            print("Sorry, there is an OSError and path couldn't be changed.")
            main()

def renameFile(old_file_name, new_file_name): #rename the files using two arguments
    message = "rename %s %s" % (old_file_name, new_file_name)  
    clientSocket.sendto(message.encode(), server)
    time.sleep(1)
    try:
        (serverReply, server) = clientSocket.recvfrom(2408)
        print(serverReply, '\n', sep = '')
    except socket.error:
        print ("Took too long....")
        main()
    main()

def listFiles(): 
    message = "list"
    clientSocket.sendto(message.encode(), server)
    while True:
        try:
            time.sleep(.1)
            (serverReply, rightthere) = clientSocket.recvfrom(1024)
            print(serverReply.decode())
        except BlockingIOError:
            main()
    

def exit(): #simply send 'exit' string to server and allow it to handle
    message = "exit"
    clientSocket.sendto(message.encode(), server)
    clientSocket.close()
    print('Gracefully exiting.....')
    time.sleep(.5)
    sys.exit()


def action(): #how to retrieve arguments......there should be a better way.
    
    print("""\
    Your options are-
    get [file_name]
    put [file_name]
    rename [old_file_name] [new_file_name]
    list
    exit""")

    action = input('What would you like to do?').split()

    if len(action) >= 4:#use loop to append command line user inputs to action list. Make list no more than four values
       print('This program only supports one command and up to two arguments, but you can try again.')
       action()
    return action

def main():
    print()
    print()

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
        options.get(command)(old_file_name, new_file_name)
    else: options.get(command)()

    #clientSocket.close()

if __name__ == "__main__": 
    main()