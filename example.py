import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAdress = {
        "s"  :"10.10.3.1",
        "r2" :"10.10.6.1",
        "d"  :"10.10.7.1"
        }

initiate = True
ThreadList = []
ThreadCount = 10
bufferSize = 1024


rtt_s  = 0
rtt_r2 = 0
rtt_d  = 0

total_time_s  = 0
total_time_r2 = 0
total_time_d  = 0
terminate = ThreadCount*6 

def get_time():
      return int(round(time.time() * 1000))

def Connect2Server(address, msg_id):
    global terminate
    if(terminate <= 0):
        print("server is closing")
        UDPServerObject.server_close()
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverAddressPort = (address, 5050)

    msg = "START_R3*"+str(get_time())+"*NA*"+str(msg_id)
    bytesToSend = str.encode(msg)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msgFromServer = str(repr(msgFromServer[0])[2:-1])
    msg = "["+address+"] : "+msgFromServer

    print(msg)
    end_time = get_time()
    start_time =(msgFromServer.split("*"))
    for i in start_time:
        print(i)
#    print(start_time[0])
    #print("start time: "+str(start_time)+"   end time: "+ str(end_time_))
#    difference = end_time - start_time

#    host = msgFromServer.split("*")[0]
    global total_time_s
#    if host == "START_S":
#        total_time_s += difference
#        terminate -= 1




class UDPRequestHandler(socketserver.DatagramRequestHandler):
    #override
    def handle(self):
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)
        global initiate
        global ThreadCount
        global ThreadList

        # initiated from R2 => send discovery message to : S, R2, D
        if(initiate == True and address == ClientAdress["s"]):
            
            initiate = False
            for key in ClientAdress:
                for index in range(ThreadCount):
                    ThreadInstance = threading.Thread(target=Connect2Server(ClientAdress[key], index))
                    ThreadList.append(ThreadInstance)
                    ThreadInstance.start()
                #main thread to wait till all connection threads are complete
                for index in range(ThreadCount):
                    ThreadList[index].join()
        
        # respond to requested UDP messages
        else:
            #print("Thread Name: {}".format(threading.current_thread().name))
            ACK = "ACK_R3*"+datagram
            self.wfile.write(ACK.encode())

UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()

