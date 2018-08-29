Homework3: HTTP and Web Proxies

readme:

Files:
web_proxy.py: Receives data from client, sends it to webserver which it receives back data and sends it back to the webclient.
web_client.py: Sends GET command to proxy and waits and "listens" for response.

Linux:
Open Two Terminals

First Terminal:
1.)run: python3 web_proxy.py
4.)Here the proxy will attempt to connect to the webserver and receive back data.

Second Terminal
2.)run: python3 web_client.py
3.)On "Enter URL: ", type in the url which you want to request.
5.) Once proxy receives data from webserver, client should receive HTML file as well and print it out.

Websites it works for:
wesleyan.edu
www.wesleyan.edu/mathcs/index.html
gabrieldrozdov.com 
