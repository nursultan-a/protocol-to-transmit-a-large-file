import socket
import sys
from _thread import *
import threading

print_lock = threading.Lock()

#thread function
def threaded(c, address, value):
    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            print('No data')

            # lock released on exit
            print_lock.release()
            break
        print(data)
        # reverse the given string from client
        data = data[::-1]

        # send back
        c.send(data)

    # close connection
    c.close()

def Main():
    ####### get ip adress of connected hosts #####################
    try:
        r1_ip = socket.gethostbyname('r1')
        print("r1 ip: %s" %(r1_ip))
    except socket.gaierror:
        print("there was an error on resolving the r1")
        sys.exit()


    try:
        d_ip = socket.gethostbyname('d')
        print("d ip: %s" %(d_ip))
    except socket.gaierror:
        print("there was an error on resolving the d")
        sys.exit()

    try:
        r3_ip = socket.gethostbyname('r3')
        print("r1 ip: %s" %(r3_ip))
    except socket.gaierror:
        print("there was an error on resolving the r3")
        sys.exit()


    try:
        s_ip = socket.gethostbyname('s')
        print("s ip: %s" %(s_ip))
    except socket.gaierror:
        print("there was an error on resolving the s")
        sys.exit()
    ##############################################################
    port = 12345
    ########### create client and server socet for r1 ############
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        print("server_socket successfully created")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        print("client_socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" %(err))


    server_socket.bind(("", port))
    print("server_socket binded to %s" %(port))

    while(True):
        value, address = server_socket.recvfrom(1024)
        c = server_socket.recvfrom(1024)

        print_lock.acquire()

        print('[',address,'] : ',value)

        # start new thread
        start_new_thread(threaded,(c, value, address))
        server_socket.sendto("hello from r2".encode(), (r1_ip,port))



if __name__ == '__main__':
    Main()
