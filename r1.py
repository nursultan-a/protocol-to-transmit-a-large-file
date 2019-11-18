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
    d_ip = socket.gethostbyname('d')
    print("d ip: %s" %(d_ip))
except socket.gaierror:
    print("there was an error on resolving the d")
    sys.exit()

try:
    s_ip = socket.gethostbyname('s')
    print("s ip: %s" %(s_ip))
except socket.gaierror:
    print("there was an error on resolving the s")
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
client_socket.sendto("hello from r1".encode(),destination)

responded_msg = client_socket.recvfrom(1024)
print(responded_msg[0].decode())

