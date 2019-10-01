import socket
import ipaddress
import sys
import getopt
import os

#Client address and port information-
Address = ipaddress.ip_address(input("Enter IP Address-"))

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True: #this loop ensures that desired port number is not too popular and is integer.
    Trop = int(input("Enter port number above 1024- "))
    if (Trop <= 1024):
        print("Clearly","  ", Trop, "  ", "is not above 1024.", sep = "")
        continue
    elif (isinstance(Trop, int)) == False: 
        print("Assume number is integer.")
        continue
    else:
        serverSocket.bind(("",Trop)) 
        (data, Address) = serverSocket.recvfrom(5000)
        print(data)

#def get file
def getFile(file_name): #receive command, decode, check if file exists, open encode, send
    (file_name, (Address,Trop)) = serverSocket.recvfrom(6000)
    sFile = file_name.decode()
    if os.path.exits(sFile) == True: 
        fileHandle = open(sFile, 'rb')
        serverSocket.sendto(fileHandle.encode(), Address)
    else: print('File does not exist in directory.')


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
    (data, (Address,Trop)) = serverSocket.recvfrom(6000)
    command = data.decode()
    if command == ascii("list"): listing = os.listdir()
    serverSocket.sendto(listing.encode(), Address)

#def exit:
def exit():
    (data, (Address,Trop)) = serverSocket.recvfrom(6000)
    command = data.decode()
    if command == ascii("exit"): serverSocket.close() 
    sys.exit()