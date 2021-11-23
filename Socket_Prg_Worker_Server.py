import socket
import pandas as pd
from _thread import start_new_thread

serverSocket = socket.socket()
noOfClients = 0
try:
    serverSocket.bind((socket.gethostname(), 1025))
except socket.error as err:
    print(str(err))

print("Waiting for connection...")
serverSocket.listen(8)


def servicesProvided(client):
    df = pd.read_excel('WorkersSheet.xlsx')
    client.send("Enter MAIL ID".encode('utf-8'))
    mail = client.recv(1000).decode('utf-8')
    client.send("Enter Password".encode('utf-8'))
    WorkerPwd = client.recv(1000).decode('utf-8')
    ans = df[(df['Gmail'] == mail) & (df['WorkerPwd'] == WorkerPwd)]
    if (ans.empty):
        client.send("Entered Gmail/Password is Invalid".encode('utf-8'))
        client.close()
    else:
        order = pd.read_csv('Order.csv')
        client.send("Access Granted...".encode('utf-8'))
        cont = "Yes"
        while (cont == "Yes" or cont == "yes"):
            client.send('Enter the Order number:'.encode('utf-8'))
            orderID = int(client.recv(1000).decode('utf-8'))
            client.send('Enter the delivery Status:'.encode('utf-8'))
            DeliveryStatus = client.recv(1000).decode('utf-8')
            order.set_index('orderID', inplace=True)
            order.loc[orderID, 'DeliveryStatus'] = DeliveryStatus
            order.reset_index(inplace=True)
            order.to_csv("Order.csv", index=False)
            client.send("Successful!\nDo you want to edit status of any more order? Yes/No?".encode('utf-8'))
            cont = client.recv(1000).decode('utf-8')
    client.close()


while True:
    client, adrs = serverSocket.accept()
    client.send("Connecting to server...".encode('utf-8'))
    start_new_thread(servicesProvided, (client,))
    noOfClients += 1