import socket
import pandas as pd
from _thread import start_new_thread

serverSocket = socket.socket()
noOfClients = 0
try:
    serverSocket.bind((socket.gethostname(),1024))
except socket.error as err:
    print(str(err))

print("Waiting for connection...")
serverSocket.listen(8)

def servicesProvided(client):
    df = pd.read_csv('Order.csv')
    name = client.recv(1000).decode('utf-8')
    print(name,"is online")
    client.send("Enter MAIL ID".encode('utf-8'))
    mail = client.recv(1000).decode('utf-8')
    home = "yes"
    while(home == "yes" or home == "Yes"):
        intro = '''Choose an option:
            1)View status of an order
            2)Make a New order
        '''
        client.send(intro.encode('utf-8'))
        opt = client.recv(1000).decode('utf-8')
        opt = int(opt)
        if (opt==1):

            client.send("Enter order ID : ".encode('utf-8'))
            pid = client.recv(1000).decode('utf-8')
            print(pid)
            info = df[df['orderID'] == int(pid)]
            info = info.to_string(index=False)
            requestedData = info.encode('utf-8')
            client.send(requestedData)
        elif (opt==2):
            menu = pd.read_csv('menu.csv')
            menuData = menu.to_string(index=False)
            client.send(menuData.encode('utf-8'))
            cont = "Yes"
            total = 0
            df1 = pd.DataFrame(columns=['Item', 'Quantity'], index=None)
            finalOrder = ""
            while (cont == "Yes"):

                client.send("Enter your order from the menu in the format ITEM-QUANTITY separated by comma(,)".encode('utf-8'))
                order = client.recv(1000).decode('utf-8')
                finalOrder+=order
                client.send("Order being processed...".encode('utf-8'))

                for m in order.split(","):
                    item, quantity = m.split("-")
                    quantity = int(quantity)
                    itemlist = menu[menu['Item'] == item]
                    cost = itemlist.iloc[0]['Cost']
                    df2 = {'Item': item, 'Quantity': quantity}
                    df1 = df1.append(df2, ignore_index=True)
                total += cost * quantity
                msg = "Order processed successfully....\n"
                msg += df1.to_string(index=False)
                client.send(msg.encode('utf-8'))
                client.send("Would you like to order anything else?".encode('utf-8'))
                cont = client.recv(1000).decode('utf-8')
            count = df.iloc[-1,0]
            orderentry = {'orderID':count+1, 'UserName': name, 'UserGmail': mail, 'OrderTaken': finalOrder, 'Cost': total, 'DeliveryStatus': "Order confirmed"}
            df = df.append(orderentry, ignore_index=True)
            df.to_csv("Order.csv",index=False)

            bill = '''
            BILL
------------------------------------------------\n'''
            bill += df1.to_string(index=False)
            bill += "\nGrand Total : " + str(total) + "\nOrder Placed Successfully.\nOrder Number : " + str(count+1)
            client.send(bill.encode('utf-8'))

            file = name + ".txt"
            file1 = open(file, 'a+')
            file1.write(bill)
            file1.close()



        else:
                client.send("Invalid option....closing connection".encode('utf-8'))
                client.close()
        home = client.recv(1000).decode('utf-8')
    client.close()
while True:
    client, adrs = serverSocket.accept()
    client.send("Connecting to server...".encode('utf-8'))
    start_new_thread(servicesProvided,(client,))
    noOfClients += 1