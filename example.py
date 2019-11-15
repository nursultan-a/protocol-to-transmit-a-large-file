from socket import *
import thread
import time 

# TCP server part

serverPort = 12002	# initializing TCP server's TCP listening port variable
serverSocket = socket(AF_INET,SOCK_STREAM)  # initializing TCP server's TCP socket variable
serverSocket.bind(('',serverPort))  # assigning TCP server's TCP socket's listening port
serverSocket.listen(1)	# starting TCP server's TCP socket's listening at port 12002

def t3_thread(connectionSocket):	# TCP server's thread function
	data = connectionSocket.recv(1024)  # receiving the TCP connection's message that comes from TCP router and its buffer at most 1024 bits
	print "Received From T2: " + str(data)
	modifiedData = data + ", returned from T3"  # changing the received data before sending back to TCP router
	t_last=time.time()  # measuring the time to compare with starting time t_before
	print "end time :", t_last
	connectionSocket.send(modifiedData) # sending back the modified message to the TCP router
	print "Sent To T2: " + modifiedData
	connectionSocket.close()    # closing the connection with TCP router
	print "\n"

print "The server is ready to receive\n" 
try:    # tries to create and run TCP connection's threads
	while True:
		connectionSocket, addr = serverSocket.accept()	# starting the TCP server's TCP socket to accept connection at its listening port 12002
		thread.start_new_thread( t3_thread, (connectionSocket, ) )  # creating and running the TCP server's thread
except:	# if some problem happened when creating and running threads
   print "Error: unable to start thread"

while True: # this while is for main process's waiting for the threads
        pass
