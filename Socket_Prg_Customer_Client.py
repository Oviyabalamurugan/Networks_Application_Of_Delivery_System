import socket

clientSocket = socket.socket()

try:
    clientSocket.connect((socket.gethostname(), 1024))
except socket.error as err:
    print(str(err))

print(clientSocket.recv(1000).decode('utf-8'))
print("Enter Name: ")
name = input()
clientSocket.send(name.encode('utf-8'))
print(clientSocket.recv(1000).decode('utf-8'))
mailID = input()
clientSocket.send(mailID.encode('utf-8'))

home = "Yes"
while (home == "yes" or home == "Yes"):
    print(clientSocket.recv(1000).decode('utf-8'))
    option = input()
    clientSocket.send(option.encode('utf-8'))
    option = int(option)
    if (option == 1):
        print(clientSocket.recv(1000).decode('utf-8'))
        orderID = input()
        clientSocket.send(orderID.encode('utf-8'))
        print(clientSocket.recv(1000).decode('utf-8'))
    elif (option == 2):
        continueprocess = 'Yes'
        while (continueprocess == 'Yes'):
            print(clientSocket.recv(1000).decode('utf-8'))
            print(clientSocket.recv(1000).decode('utf-8'))
            orderTaken = input()
            clientSocket.send(orderTaken.encode('utf-8'))
            print(clientSocket.recv(1000).decode('utf-8'))
            print(clientSocket.recv(1000).decode('utf-8'))
            print(clientSocket.recv(1000).decode('utf-8'))
            continueprocess = input()
            clientSocket.send(continueprocess.encode('utf-8'))
        print(clientSocket.recv(1000).decode('utf-8'))
    else:
        print(clientSocket.recv(1000).decode('utf-8'))
        break
    print('Do you want to go to home screen?')
    home = input()
    clientSocket.send(home.encode('utf-8'))
