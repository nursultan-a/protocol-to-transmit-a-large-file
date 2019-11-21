import socket
import time

msgFromClient       = ["Hello Destination Node","What is your IP?"]
serverAddressPort   = ("10.10.3.2", 20001)
bufferSize          = 1024
experiment_number = 1
total_time = 0
rtt = 0


def get_time():
    return int(round(time.time() * 1000))


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
for experiment in range(experiment_number):
    for msg in msgFromClient:

        experiment_id = experiment_number - experiment - 1
        bytesToSend   = str.encode(msg+"*"+str(experiment_id)+"*")
        
        start_time = get_time()

        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        end_time = get_time()

        msgFromServer = repr(msgFromServer[0])[2:-1]
        print("r3->s: "+msgFromServer)

        total_time = end_time - start_time

rtt = total_time / float(experiment_number * 2)

print("rtt: "+ str(rtt))
