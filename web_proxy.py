#!/usr/bin/python3
#
# Wesleyan University
# COMP 332, Spring 2018
# Homework 3: Simple multi-threaded web proxy

# Usage:
#   python3 web_proxy.py <proxy_host> <proxy_port> <requested_url>
#

# Python modules
#************************************************************************************************
#                                   COMP332: Homework 2
#                                 Author: Shota Nakamura
#Usage: run python3 web_client.py
#Purpose: This Server (web_proxy) listens for connections from the web_client and acts as the "middle-man" 
#         to connect the client to the requested webserver. This means that this server takes multiple clients.
#         Therefore, once it receives a GET request, it then sends it to the webserver by using port 80.
#         Once the web_proxy receives data from the server, it sends it back to the client. 
#************************************************************************************************
import socket
import sys
import threading


class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1
        self.web_cache = {}
        self.start()

    def start(self):

        # Initialize server socket on which to listen for connections
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.bind((self.proxy_host, self.proxy_port))
            proxy_sock.listen(self.proxy_backlog)

        except OSError as e:
            print ("Unable to open proxy socket: ", e)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Wait for client connection
        while True:
            client_conn, client_addr = proxy_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(
                    target = self.serve_content, args = (client_conn, client_addr))
            thread.start()
    
    #Decodes binary data with endflag
    def decoder(self,conn):
        decoded_data = ''
        while True:
            decoded_data += (conn.recv(4096)).decode('utf-8')
            try:
                decoded_data.index("\r\n\r\n")
                break
            except ValueError:
                pass
        return decoded_data

    #Decodes binary data without endflag 
    def decoder2(self,conn):
        print("Check 1")
        decoded_data = b''
        while True:
            d = conn.recv(1024)
            if not d:
                break
            decoded_data += d
        print("Check 2")
        return decoded_data

    def serve_content(self, client_conn, client_addr):

        # Todos
        # Receive request from client
        #Decodes message from client 
        decoded_msg = self.decoder(client_conn)
        #Encodes client message to send back and adds an end flag
        encoder = decoded_msg.encode('utf-8')

        # Open connection to web server
        server_host1 = decoded_msg[(decoded_msg.index("Host: ") + 6):]
        server_host = server_host1[:server_host1.index("\r\n\r\n")]
        try:
            web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Here web_sock is the socket for the webserver
            web_sock.connect((server_host, 80)) #We use the host from the GET command, and use port 80 to connect to the internet
            web_sock.sendall(encoder) 
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", e)
            if web_sock:
                web_sock.close()
            sys.exit(1)

        #Wait for Webserver.................		

        #decodes data from the webserver and saves in cat
        cat = self.decoder2(web_sock)

        # Send web server response to client 
        client_conn.sendall(cat)
        print(cat)
        #Closes Client Connection
        client_conn.close()

def main():

    print (sys.argv, len(sys.argv))

    proxy_host = 'localhost'
    proxy_port = 50007

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)

if __name__ == '__main__':

    main()
