import socketserver
import threading
import socket
import time


ServerAddress = ("", 5050)

ClientAdress = {
        "d"  :"10.10.7.1",
        "s"  :"10.10.3.1",
        "r2" :"10.10.6.1"
        }

initiate = True
ThreadList = []
ThreadCount = 1000
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

    start_time =int(msgFromServer.split("*")[2])
    visited_host = msgFromServer.split("*")[0].split("_")[1].lower()

    global total_time_s
    global total_time_r2
    global total_time_d

    global terminate

    if len(msgFromServer.split("*")) >= 4:
        difference = end_time - start_time
        #print(str(end_time)+" - "+str(start_time)+"="+str(difference))
        terminate -= 1

        print("CONDITION-----------------------------------------"+str(terminate))
        if(visited_host == "s"):
            total_time_s += difference
        elif(visited_host == "r2"):
            total_time_r2 += difference
        elif(visited_host == "d"):
            total_time_d += difference
        if(terminate == 0):
            print("terminating server from ACK side")

            UDPServerObject.shutdown()
            rtt_s = total_time_s/ThreadCount
            rtt_r2 = total_time_r2/ThreadCount
            rtt_d = total_time_d/ThreadCount
            print ("rtt for s: "+str(rtt_s)+" rtt for r2: "+str(rtt_r2)+" rtt for d: "+str(rtt_d))

            f = open("link_costs.txt", "w+")
            f.write(str(rtt_s)+", "+str(rtt_r2)+", "+str(rtt_d))
            f.close()

class UDPRequestHandler(socketserver.DatagramRequestHandler):
    #override
    def handle(self):
        datagram = str(repr(self.rfile.readline().strip())[2:-1])
        address = "{}".format(self.client_address[0])

        print("[" + address + "] : "+datagram)
        global initiate
        global ThreadCount
        global ThreadList
        global terminate

        global total_time_s
        global total_time_r2
        global total_time_d

        global UDPServerObject
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

            terminate -= 1
            print("condition -----------------"+ str(terminate))
            ACK = "ACK_R3*"+datagram
            self.wfile.write(ACK.encode())
            if(terminate == 0):
                print("terminating server from ACK side")

                UDPServerObject.shutdown()
                rtt_s = total_time_s/ThreadCount
                rtt_r2 = total_time_r2/ThreadCount
                rtt_d = total_time_d/ThreadCount
                print ("rtt for s: "+str(rtt_s)+" rtt for r2: "+str(rtt_r2)+" rtt for d: "+str(rtt_d))

                f = open("link_costs.txt", "w+")
                f.write(str(rtt_s)+", "+str(rtt_r2)+", "+str(rtt_d))
                f.close()

UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress,UDPRequestHandler)

UDPServerObject.serve_forever()

