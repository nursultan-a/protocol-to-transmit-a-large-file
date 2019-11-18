import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAdress = {
        "s"  :"10.10.2.2",
        "r1" :"10.10.8.1",
        "r3" :"10.10.6.2",
        "d"  :"10.10.5.2"

        }
initiate = True
ThreadList = []
ThreadCount = 10
bufferSize = 1024


def get_time():
      return int(round(time.time() * 1000))

def Connect2Server(address):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (address, 5050)

    msg = "START_R2*"+str(get_time())+"*NA"
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    msg = address +" : "+str(repr(msgFromServer[0])[2:-1])

    print(msg)



class UDPRequestHandler(socketserver.DatagramRequestHandler):
    #override
    def handle(self):
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)
        global initiate
        global ThreadCount
        global ThreadList

        # initiated from S => send discovery message to : R1, R2, R3, S, D
        if(initiate == True and address == ClientAdress["s"]):
            
            initiate = False
            for key in ClientAdress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAdress[key]))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()
                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()
        
        # respond to requested UDP messages
        else:
            #print("Thread Name: {}".format(threading.current_thread().name))
            ACK = "ACK_R2*"+datagram
            self.wfile.write(ACK.encode())


UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
