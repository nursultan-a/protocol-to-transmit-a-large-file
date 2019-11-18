import socket
import time
import threading

def get_time():
      return int(round(time.time() * 1000))



bufferSize = 1024


serverAddressPort = ("10.10.8.2", 5050)

def Connect2Server():
    msgFromClient = "START_R1*" + str(get_time()) + "*NA"
    bytesToSend = str.encode(msgFromClient)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = str(repr(msgFromServer[0])[2:-1])
    msg = "10.10.8.2 : " + msgFromServer
    print(msg)

print("Client - Main thread started")
ThreadList = []
ThreadCount = 20

for index in range(ThreadCount):
    ThreadInstance = threading.Thread(target=Connect2Server())
    ThreadList.append(ThreadInstance)

    ThreadInstance.start()

for index in range(ThreadCount):
    ThreadList[index].join()
