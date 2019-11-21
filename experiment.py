import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAddress = {"r3" :"10.10.3.2"}
ThreadList = []
ThreadCount = 10
bufferSize = 1024

terminate = ThreadCount*6 - 1

flag = (ThreadCount*3) 

def get_time():
      return int(round(time.time() * 1000))

def Connect2Server(address, msg_id):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    serverAddressPort = (address, 5050)

    msg = "FROM_S*"+str(get_time())+"INTERLINK_R3*TO_D*NURSULTAN"
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "[" + address +"] :" +str(repr(msgFromServer[0])[2:-1])

    print(msg)
    global terminate
    global UDPServerObject

    terminate -= 1
    #print("condition--------------"+str(terminate))
    if terminate == 0:
        print("Terminating server! Bye")
        UDPServerObject.shutdown()

for index in range(ThreadCount):
    ThreadInstance = threading.Thread(target=Connect2Server(ClientAddress[0], index))
    ThreadList.append(ThreadInstance)
    ThreadInstance.start()

for index in range(ThreadCount):
    ThreadList[index].join()
