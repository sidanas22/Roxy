import socket
import hashlib
import os
import pickle
import random
import time
from collections import namedtuple

Packet = namedtuple("Packet", ["SeqN","Data","CheckSum"])
Ack = namedtuple("Ack", ["Ack"])


class LRUCache:

    def __init__(self, _max: int):
        self.cache = OrderedDict()
        self.max_cache = _max

    def get(self, key: str) -> int:
        if key not in self.cache:
            return 0
        else:
            self.cache.move_to_end(key)
            return 1

    def put(self, key: str, value: str) -> str:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if(len(self.cache) > self.max_cache):
            extra = self.cache.popitem(last=False)
            return str(extra[0])
        return "Removed Nothing"




BUFSIZ = 1024
lossRate = 0.3 # not needed
timeout = 2
Port = 8008
rcvPort = 8009
rcvlocal = "127.0.0.1"
rcvAdd = (rcvlocal,rcvPort)
sd = None

def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

# Assign and bind a socket
def Sock_a():
    global sd
    try:
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sd.bind(("localhost",Port))
        sd.setblocking(0)
    except:
        print("Socket Assignment Failed!")
        return

def RDT():
    

    Data_l = ["Mehran","lives","in","Gulshan e iqbal","Karachi"]
    Sock_a()
    SendData(filename.encode('utf-8'))

    for i in range(len(Data_l)):
        data = Data_l[i].encode()
        
        
         print("File did not exist before. Current Cache: ",
                  self.cache_obj.cache)

            # flag1 = 0
            # flag2 = 0
            # org_serv_pos = temp.find("/")
            # if org_serv_pos == -1:
            #     org_serv_pos = len(temp)
            #     flag1 = 1
            # else:
            #     experiment = temp[org_serv_pos:]
            #     if(len(experiment) == 1):
            #         flag2 = 1

        
        chk = CheckSum(data)
        pkt = Packet(i,data,chk)
        bpkt = pickle.dumps(pkt)
        while(True):
            try:
                SendData(bpkt)
                print("Sent Packet#", i)
            except:
                print("Error Sending Data")
            start = time.time()
            flag = 0
            while(True):
                try:
                    # Check timer
                    if(time.time()-start>=timeout):
                        print("Timeout!")
                        flag=1
                        break
                    ack, addr = sd.recvfrom(BUFSIZ)
                    break
                except OSError:
                    # print("No Data")
                    continue
            if(flag==1):
                continue
            Resp = pickle.loads(ack)
            print(Resp)
            if(Resp.Ack==i):
                # Correct Ack Received
                break
            else:
                # Wrong Ack Received
                continue
    print("All Data Sent")
    sd.setblocking(1)
    while(True):
        SendData(b'FIN')
        Resp = RecvData()
        if Resp == b'FIN':
            print("Closing Server")
            break
    return

def SendData(message):
    sd.sendto(message, rcvAdd)
    return

def RecvData():
    (msg1, addr) = sd.recvfrom(BUFSIZ)
    return msg1






filename = "1.png"
script_dir = os.path.dirname(__file__) 
rel_path = "send/" + filename
abs_file_path = os.path.join(script_dir, rel_path)

# def SplitFile():
#     try:
#         file = open(abs_file_path, 'rb')
#         Data = file.read()
#         file.close()
#         return Data
  
#     except:
#         print("Error Reading File!")
#         return None


RDT()

#CERTFILE, KEYFILE = 'localhost.crt', 'localhost.key'
#CACHE_SIZE_REQUIRED = 5
#serv_port = 8888



class kerver():

    def __init__(self):
        self.serv_socket = socket(AF_INET, SOCK_STREAM)
        self.serv_socket.bind(('', serv_port))
        self.serv_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # self.cntxt = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.cntxt.load_cert_chain(CERTFILE, KEYFILE)
        # self.cntxt.set_ciphers(
        #     'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')

        self.lock = threading.Lock()
        self.cache_obj = LRUCache(CACHE_SIZE_REQUIRED)

    def find_file(self, filename, socket_to_browser, addr, fileExist=False):
        try:

            print("The file to look for in cache: ", filename)
            f_name = filename.replace('/', 'sentinel')

            f = open(f_name, "rb")
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
        threads = []
        self.serv_socket.listen(10)
        print("Server has started to listen\n")
        while True:
            # start receiving from client
            print("Proxy Server Ready to serve")
            # socket_to_browser.settimeout(10)
            socket_to_browser, addr = self.serv_socket.accept()
            print("Received a connection from: ", addr)
            # self.func_proxy(socket_to_browser,addr)

            # try:
            #     conn_socket_to_browser = self.cntxt.wrap_socket(
            #         socket_to_browser, server_side=True)
            # except ssl.SSLError as s:
            #     print("Here is what is wrong: ",s)

            thread_count = thread_count + 1
            thrd = threading.Thread(
                target=self.func_proxy, args=(socket_to_browser, addr, thread_count))
            threads.append(thrd)
            thrd.start()

    def func_proxy(self, socket_to_browser, addr, thread_count):

        print("XXXXXX STARTED THREAD #", thread_count, " XXXXXX")
        message = socket_to_browser.recv(1024).decode()
        print("This message is sent by browser: ", message)

        # now extracting the filename from http request
        msg_part = message.split()
        z = message.split()[0]
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
            middle_message = x

        # print(http_check)

        file_to_look = temp

        self.lock.acquire()
        fileExist = self.find_file(
            file_to_look, socket_to_browser, addr, False)
        if(fileExist == True):
            self.lock.release()

        if(fileExist == False):

            print("File did not exist before. Current Cache: ",
                  self.cache_obj.cache)

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

            # port checking phase now
            pos_port = temp.find(":")
            port = -1
            if(pos_port == -1):
                port = 80
                originserver = temp[:org_serv_pos]
            else:  # port 443
                port = int(temp[pos_port+1:][:org_serv_pos-pos_port-1])
                print(port)
                originserver = temp[:pos_port]

            if(z == "CONNECT"):
                port=443

            print("The origin server and port are: ", originserver, " ", port)

            
            
            c = None
            tmpfile = None
            try:
                c = socket(AF_INET, SOCK_STREAM)
                
                c.connect((originserver, port))
                if z == 'CONNECT':
                    try:

                        print("Connect message sent by browser")
                        
                        socket_to_browser.sendall(
                            "HTTP/1.1 200 Connection established\r\n\r\n".encode())
                    except Exception as err:
                        print("The CONNECT Rrequest Error is: ", str(err))
                    
                    #socket_to_browser.setblocking()
                    
                    while True:
                        try:
                            # socket_to_browser.settimeout(1)
                            msg_to_be_sent = socket_to_browser.recv(4096)
                            # socket_to_browser.settimeout(None)

                            # c.settimeout(1)
                            c.sendall(msg_to_be_sent)
                            # c.settimeout(None)
                            print("DATA BEING SENT: BROWSER -> PROXY -> ORIGIN")
                        except Exception as ne:
                            print("The 1st try error in new while is:\n",str(ne))
                            pass
                            

                            
                        try:
                            # c.settimeout(1)
                            reply = c.recv(4096)
                            # c.settimeout(None)
                            if(len(reply) > 0):
                                # socket_to_browser.settimeout(1)
                                socket_to_browser.sendall(reply)
                                # socket_to_browser.settimeout(None)
                                print("DATA BEING SENT: BROWSER <- PROXY -< OrIGIN")
                            else:
                                break
                        except Exception as nw:
                            print("The 2nd try error in new while is:\n",str(nw))
                            pass


                        

                useragent = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
                if (flag1 == 1 or flag2 == 1) and z!='CONNECT':
                    #msg_to_be_sent="GET / HTTP/1.1\r\nHost: www.google.com\r\n"+useragent+"\r\n\r\n"
                    msg_to_be_sent = msg_part[0]+" / " + \
                        msg_part[2]+"\r\nHost: "+originserver + \
                        "\r\n"+useragent+"\r\n\r\n"
                    #msg_to_be_sent = message
                    tmpfile = open("./"+temp[:org_serv_pos], "wb+")
                    string = temp[:org_serv_pos]

                    print("Now making a new entry in cache:")
                    print("Cache Before Entry: ", self.cache_obj.cache)
                    mehran = self.cache_obj.put(string, string)
                    print("Cache After Entry BUT Before OSREMOVE: ",
                            self.cache_obj.cache)
                    if(mehran != "Removed Nothing"):

                        os.remove(mehran)
                        print("File: ", mehran, " has been removed")
                        print("Cache After Entry AND After OSREMOVE: ",
                                self.cache_obj.cache)
                    c.send(msg_to_be_sent.encode())

                elif z!= 'CONNECT':
                    msg_to_be_sent = msg_part[0]+" "+middle_message+" " + \
                        msg_part[2]+"\r\nHost: "+originserver + \
                        "\r\n"+useragent+"\r\n\r\n"
                    # msg_to_be_sent = message

                    tmpfile = open("./"+temp.replace("/", "sentinel"), "wb+")
                    string = temp.replace("/", "sentinel")
                    print("Now making a new entry in cache:")
                    print("Cache Before Entry: ", self.cache_obj.cache)
                    mehran = self.cache_obj.put(string, string)
                    print("Cache After Entry BUT Before OSREMOVE: ",
                          self.cache_obj.cache)
                    if(mehran != "Removed Nothing"):
                        os.remove(mehran)
                        print("File: ", mehran, " has been removed")
                        print("Cache After Entry AND After OSREMOVE: ",
                              self.cache_obj.cache)

                    c.send(msg_to_be_sent.encode())

                while True and z!="CONNECT":
                    print("Before polling.")
                    data = None
                    try:
                        
                        c.settimeout(5)
                        data = c.recv(4096)
                        print("The data is:\n",data)
                        c.settimeout(None)
                        # conn.close()
                    except Exception as ex:
                        print("The error for time is: ", str(ex))
                        break
                    try:
                        # c.settimeout(None)
                        # print(len(data))
                        if len(data) > 0:
                            socket_to_browser.send(data)
                            if(tmpfile != None):
                                tmpfile.write(data)

                        else:
                            print("TIME OUT")
                            if(tmpfile != None):
                                tmpfile.close()
                            break
                    except Exception as f:
                        print("The error is", f)

                if(tmpfile!=None):
                    tmpfile.close()
                print("Response complete")

            except Exception as e:
                print("The error is: ", e)
                if tmpfile != None:
                    tmpfile.close()

            # close the socket to the origin server and current connection socket
            c.close()

        self.lock.release()
        socket_to_browser.close()
        print(" XXXXX FINISHED THREAD #", thread_count, " XXXXXXXXXX")


