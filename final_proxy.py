from socket import *
import os
import sys
import threading
from collections import OrderedDict

# Create a server socket, bind it to a port and start listening
serv_port = 8888

class LRUCache:

    def __init__(self , _max : int):
        self.cache = OrderedDict()
        self.max_cache = _max

    def get(self, key: str) -> int:
        if key not in self.cache:
            return 0
        else:
            self.cache.move_to_end(key)
            return 1

    def put(self, key :str, value: str):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if(len(self.cache) > self.max_cache):
            self.cache.popitem(last = False)
            self.cache.


class kerver():

    def __init__(self):
        self.serv_socket = socket(AF_INET, SOCK_STREAM)
        self.serv_socket.bind(('', serv_port))
        self.serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.lock = threading.Lock()
        self.cache_obj = LRUCache(5)

    def find_file(self, filename, socket_to_browser, addr, fileExist=False):
        try:
            
            print("The file to look for in cache: ", filename)
            f_name = filename.replace('/', 'sentinel')
            
            f = open(f_name , "rb")
            flag_cache = self.cache_obj.get(f_name)
            outputdata = f.read()

            # for i in range (0, len(outputdata)):
            socket_to_browser.sendall(outputdata)

            # socket_to_browser.send("\r\n")
            print("Read from cache")
            socket_to_browser.close()
            fileExist = True
            return fileExist
        except IOError:
            print("Exception for opening file raised. ")
            return fileExist
        except Exception as file_reading:
            print("The error in the function def_file: ", str(file_reading))
            return fileExist

    def _start(self):
        
        thread_count = 0
        threads=[]
        self.serv_socket.listen(10)
        print("Server has started to listen\n")
        while True:
            # start receiving from client
            print("Proxy Server Ready to serve")
            # socket_to_browser.settimeout(10)
            socket_to_browser, addr = self.serv_socket.accept()
            print("Received a connection from: ", addr)
            # self.func_proxy(socket_to_browser,addr)
            thrd = threading.Thread(
                target=self.func_proxy, args=(socket_to_browser, addr, thread_count))
            threads.append(thrd)
            thrd.start()

    def func_proxy(self, socket_to_browser, addr, thread_count):

        print("XXXXXX STARTED THREAD #",thread_count," XXXXXX")
        message = socket_to_browser.recv(1024).decode()
        print("This message is sent by browser: ", message)

        # now extracting the filename from http request
        msg_part = message.split()
        x = message.split()[1]
        print("The destination given to proxy server is: ", x)
        pos_http = x.find("://")
        http_check = ""
        if(pos_http == -1):
            temp = x
            middle_message = "http://"+temp
        else:
            temp = x[(pos_http+3):]
            http_check = x[:pos_http]
            middle_message = x.replace("https", "http", 1)

        print(http_check)

        file_to_look = temp

        self.lock.acquire()
        fileExist = self.find_file(
            file_to_look, socket_to_browser, addr, False)
        if( fileExist == False):
            self.lock.release()
        
        if(fileExist == False):
            
        
            flag1 = 0
            flag2 = 0
            org_serv_pos = temp.find("/")
            if org_serv_pos == -1:
                org_serv_pos = len(temp)
                flag1 = 1
            else:
                experiment = temp[org_serv_pos:]
                if(len(experiment) == 1):
                    flag2 = 1

            originserver = ""

            # if(port_pos == -1 or web_serv_pos < port_pos):
            port = 80
            originserver = temp[:org_serv_pos]
            print("The origin server and port are: ", originserver, " ", port)

            # Create a socket on the proxyserver
            c = None
            tmpfile = None
            try:
                c = socket(AF_INET, SOCK_STREAM)
                c.connect((originserver, port))

                # fileobject = c.makefile('rwb')
                useragent = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
                if flag1 == 1 or flag2 == 1:
                    #msg_to_be_sent="GET / HTTP/1.1\r\nHost: www.google.com\r\n"+useragent+"\r\n\r\n"
                    msg_to_be_sent = msg_part[0]+" / " + \
                        msg_part[2]+"\r\nHost: "+originserver + \
                        "\r\n"+useragent+"\r\n\r\n"
                    tmpfile = open("./"+temp[:org_serv_pos], "wb+")
                    string = temp[:org_serv_pos]
                    self.cache_obj.put(string, string)
                else:
                    msg_to_be_sent = msg_part[0]+" "+middle_message+" " + \
                        msg_part[2]+"\r\nHost: "+originserver + \
                        "\r\n"+useragent+"\r\n\r\n"
                    
                    tmpfile = open("./"+temp.replace("/","sentinel"),"wb+")
                    string = temp.replace("/","sentinel")
                    self.cache_obj.put(string)
                    
                # print("THE Request TO ORIGIN SERVER: ", msg_to_be_sent)
                # fileobject.write(msg_to_be_sent.encode())
                # fileobject.flush()
                # print("Message flushed")
                # print("Message has been sent to origin server")

                # print("Starting reading the origin server response")
                # buffer = fileobject.readlines()
                # print("Response has been read")

                #print("File has been read. This is the file content: \n",buffer)
                # for j in range(0, len(buffer)):
                #     proxy_cnnct_socket.send(buffer[j])
                #     print("Response being relayed to Browser")

                c.send(msg_to_be_sent.encode())
                # c.send("\r\n\r\n".encode())
                while True:
                    print("Before polling.")
                    data = None
                    try:
                        c.settimeout(5)
                        data = c.recv(4096)
                        c.settimeout(None)
                    except Exception as ex:
                        print("The timeout exception: ", str(ex))
                        break
                    try:
                        # c.settimeout(None)
                        # print(len(data))
                        if len(data) > 0:
                            socket_to_browser.send(data)
                            tmpfile.write(data)
                            
                        else:
                            print("Timed out!")
                            tmpfile.close()
                            break
                    except Exception as f:
                        print("The other exception is: ",str(f))
                
                tmpfile.close()
                print("All of the response has been sent.")
            
            except Exception as e:
                print("The error is: ", e)
                if tmpfile != None:
                    tmpfile.close()

            # close the socket to the origin server and current connection socket
            c.close()
        
        self.lock.release()
        socket_to_browser.close()
        print(" XXXXX FINISHED THREAD #",thread_count," XXXXXXXXXX")


if __name__ == "__main__":
    s_erv = kerver()
    s_erv._start()
