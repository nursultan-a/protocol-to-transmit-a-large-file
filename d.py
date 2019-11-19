import socket
import sys


# get ip adress of connected hosts
try:
    r2_ip = socket.gethostbyname('r2')
    print("r2 ip: %s" %(r2_ip))
except socket.gaierror:
    print("there was an error on resolving the r2")
    sys.exit()


try:
    r1_ip = socket.gethostbyname('r1')
    print("r1 ip: %s" %(r1_ip))
except socket.gaierror:
    print("there was an error on resolving the r1")
    sys.exit()

try:
    r3_ip = socket.gethostbyname('r3')
    print("r3 ip: %s" %(r3_ip))
except socket.gaierror:
    print("there was an error on resolving the r3")
    sys.exit()


port = 12345
# create client and server socet for r1
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    print("server_socket successfully created")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    print("client_socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" %(err))


destination = (r2_ip, port)
client_socket.sendto("hello from d".encode(),destination)

responded_msg = client_socket.recvfrom(1024)
print(responded_msg[0].decode())
