#!/usr/bin/python3
#
#
# Wesleyan University
# COMP 332, Spring 2018
# Homework 3: Simple web client to interact with proxy
#
# Example usage:
#
#   python3 web_client.py <proxy_host> <proxy_port> <requested_url>
#

# Python modules
#************************************************************************************************
#                                   COMP332: Homework 2
#                                 Author: Shota Nakamura
#Usage: run python3 web_client.py
#Purpose: Opens a connection to the 'server' which is on the web_proxy file.
#         Prompts user to type in a URL to connect to, parses URL and forms a request message (GET)
#         Takes Get message, encodes it and send it to the proxy.
#         Then it waits for a response from the proxy (which it is receiving from a webserver, 
#         and receives it and prints out the HTML file.   
#************************************************************************************************
import binascii
import socket
import sys

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url
        self.start()
    
    def decoder(self,sock): #Using this function makes Play more efficient because it will "break" decoder everytime an end happens
        decode_rows = ''
        while True:
            decode_rows += (sock.recv(4096)).decode('utf-8')
            try:
                decode_rows.index("\r\n\r\n")
                break
            except ValueError:
                pass
        return decode_rows

    def start(self):

        # Open connection to proxy
        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_sock.connect((self.proxy_host, self.proxy_port))
            print("Connected to socket")
        except OSError as e:
            print("Unable to connect to socket: ", message)
            if proxy_sock:
                proxy_sock.close()
            sys.exit(1)

        # Prompts user to type in URL
        url = input(str("Enter URL: \n"))
        #We use code below to split up the webpage and create a GET command
        subUrl = ' /'
        try:
            # Send requested URL to proxy
            mainUrl = url[:url.index("/")]
            subUrl += url[url.index("/")+1]
        except ValueError:
            mainUrl = url 
        get_cmd = "GET" + subUrl + " HTTP/1.1\r\nHost: " + mainUrl + "\r\n\r\n"
        #Encodes the GET command and sends it to the web_proxy
        proxy_sock.sendall(get_cmd.encode('utf-8'))
        # Receive binary data from proxy
        str_prox = self.decoder(proxy_sock)
        print(str_prox)
        proxy_sock.close()

def main():

    print (sys.argv, len(sys.argv))
    proxy_host = 'localhost'
    proxy_port = 50007

    url = 'www.wesleyan.edu/mathcs/index.html'
    #url = 'www.google.com'
    #url = 'www.mit.edu'
    #url = 'www.cyberciti.biz'

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)

if __name__ == '__main__':
    main()
