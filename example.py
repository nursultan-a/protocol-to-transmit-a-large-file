import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAdress = {
        "r1" :"10.10.8.1",
        "r3" :"10.10.6.2",
        "s"  :"10.10.2.2",
        "d"  :"10.10.5.2"

        }
initiate = True
ThreadList = []
ThreadCount = 10
class UDPRequestHandler(socketserver.DatagramRequestHandler):

    def get_time():
          return int(round(time.time() * 1000))

    def Connect2Server(adress):
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        serverAdressPort = (address, 5050)

        msg = "S*"+str(get_time)+"*"
        bytesToSend = str.encode(msg)


        UDPClientSocket.sendto(bytesToSend, serverAsddresPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        msg = "Message from Server {}".format(msgFromServer[0])

             

        print(msg)
    #override
    def handle(self):
        datagram = str(self.rfile.readline().strip())
        address = "{}".format(self.client_address[0])

        #print("[" + address + "] : "+datagram)
        if(initiate and address == ClientAdress["s"]):
            for key in ClientAdress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAdress[key]))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()

                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()


        print("Thread Name: {}".format(threading.current_thread().name))

        self.wfile.write("Message from R2! Hello r1".encode())


UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()
