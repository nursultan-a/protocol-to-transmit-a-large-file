import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAddress = {
        "r1" :"10.10.1.2",
        "r2" :"10.10.2.1",
        "r3" :"10.10.3.2",
        }
initiate = True
ThreadList = []
ThreadCount = 10

# initiate hosts: R2, R3, D
r1_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
r2_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
r3_init_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

msg = "initiate message from S :)"
r1_init_socket.sendto(str.encode(msg+" start working R1"), (ClientAddress["r1"], 5050))
r2_init_socket.sendto(str.encode(msg+" start working R2"), (ClientAddress["r2"], 5050))
r3_init_socket.sendto(str.encode(msg+" start working R3"), (ClientAddress["r3"], 5050))

def get_time():
      return int(round(time.time() * 1000))

def Connect2Server(adress):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAdressPort = (address, 5050)

    msg = "S*"+str(get_time)+"*"
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAsddresPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromserver = str(repr(msgFromServer[0])[2:-1])
    msg = "[" + adress +"] :" +msgFromServer

    print(msg)

class UDPRequestHandler(socketserver.DatagramRequestHandler):

    #override
    def handle(self):
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)

        #print("Thread Name: {}".format(threading.current_thread().name))

        ACK = "ACK_S*"+datagram

        self.wfile.write(ACK.encode())


UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
