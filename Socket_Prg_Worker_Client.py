import socket

clientSocket = socket.socket()

try:
    clientSocket.connect((socket.gethostname(),1025))
except socket.error as err:
    print(str(err))

print(clientSocket.recv(1000).decode('utf-8'))

print(clientSocket.recv(1000).decode('utf-8'))
mailID = input() 
clientSocket.send(mailID.encode('utf-8'))

print(clientSocket.recv(1000).decode('utf-8'))
WokerPwd = input() 
clientSocket.send(WokerPwd.encode('utf-8'))
print(clientSocket.recv(1000).decode('utf-8'))


cont = "Yes"
while (cont == "Yes" or cont == "yes"):
    print(clientSocket.recv(1000).decode('utf-8'))
    OrderTaken = input()
    clientSocket.send(OrderTaken.encode('utf-8'))
    print(clientSocket.recv(1000).decode('utf-8'))
    DeliveryStatus = input()
    clientSocket.send(DeliveryStatus.encode('utf-8'))
    print(clientSocket.recv(1000).decode('utf-8'))
    cont = input()
    clientSocket.send(cont.encode('utf-8'))
