import socket
import hashlib
import pickle
import random
from collections import namedtuple
import time
import random
Packet = namedtuple("Packet", ["SeqN","Data", "CheckSum"])
Ack = namedtuple("Ack", ["Ack"])


## Provides an abstraction for the network layer
class NetworkLayer:
    #configuration parameters
    prob_pkt_loss = 0
    prob_byte_corr = 0
    prob_pkt_reorder = 0
    
    #class variables
    sock = None
    conn = None
    buffer_S = ''
    lock = threading.Lock()
    collect_thread = None
    stop = None
    socket_timeout = 0.1
    reorder_msg_S = None
    
    def __init__(self, role_S, server_S, port):
        if role_S == 'client':
            print('Network: role is client')
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((server_S, port))
            self.conn.settimeout(self.socket_timeout)
            
        elif role_S == 'server':
            print('Network: role is server')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('localhost', port))
            self.sock.listen(1)
            self.conn, addr = self.sock.accept()
            self.conn.settimeout(self.socket_timeout)
        
        #start the thread to receive data on the connection
        self.collect_thread = threading.Thread(name='Collector', target=self.collect)
        self.stop = False
        self.collect_thread.start()
        

    def disconnect(self):
        if self.collect_thread:
            self.stop = True
            self.collect_thread.join()
        

    def __del__(self):
        if self.sock is not None: self.sock.close()
        if self.conn is not None: self.conn.close()

        
    def udt_send(self, msg_S):
        #return without sending if the packet is being dropped
        if random.random() < self.prob_pkt_loss:
            return
        #corrupt a packet
        if random.random() < self.prob_byte_corr:
            start = random.randint(RDT.Packet.length_S_length,len(msg_S)-5)
            num = random.randint(1,5)
            repl_S = ''.join(random.sample('XXXXX', num)) #sample length >= num
            msg_S = msg_S[:start]+repl_S+msg_S[start+num:]
        #reorder packets - either hold a packet back, or if one held back then send both
        if random.random() < self.prob_pkt_reorder or self.reorder_msg_S:
            if self.reorder_msg_S is None:
                self.reorder_msg_S = msg_S
                return None
            else:
                msg_S += self.reorder_msg_S
                self.reorder_msg_S = None
                
        #keep calling send until all the bytes are transferred
        totalsent = 0
        while totalsent < len(msg_S):
            sent = self.conn.send(msg_S[totalsent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            
            
    ## Receive data from the network and save in internal buffer
    def collect(self):
#         print (threading.currentThread().getName() + ': Starting')
        while(True):
            try:
                recv_bytes = self.conn.recv(2048)
                with self.lock:
                    self.buffer_S += recv_bytes.decode('utf-8')
            # you may need to uncomment the BlockingIOError handling on Windows machines
#             except BlockingIOError as err:
#                 pass
            except socket.timeout as err:
                pass
            if self.stop:
#                 print (threading.currentThread().getName() + ': Ending')
                return
           
    ## Deliver collected data to client 
    def udt_receive(self):
        with self.lock:
            ret_S = self.buffer_S
            self.buffer_S = ''
        return ret_S
    

#rewriting commentedclass
# class RDT:
#     ## latest sequence number used in a packet
#     seq_num = 1
#     ## buffer of bytes read from network
#     byte_buffer = '' 

#     def __init__(self, role_S, server_S, port):
#         self.network = Network.NetworkLayer(role_S, server_S, port)
    
#     def disconnect(self):
#         self.network.disconnect()
        
#     def rdt_1_0_send(self, msg_S):
#         p = Packet(self.seq_num, msg_S)
#         self.seq_num += 1
#         self.network.udt_send(p.get_byte_S())
        
#     def rdt_1_0_receive(self):
#         ret_S = None
#         byte_S = self.network.udt_receive()
#         self.byte_buffer += byte_S
#         #keep extracting packets - if reordered, could get more than one
#         while True:
#             #check if we have received enough bytes
#             if(len(self.byte_buffer) < Packet.length_S_length):
#                 return ret_S #not enough bytes to read packet length
#             #extract length of packet
#             length = int(self.byte_buffer[:Packet.length_S_length])
#             if len(self.byte_buffer) < length:
#                 return ret_S #not enough bytes to read the whole packet
#             #create packet from buffer content and add to return string
#             p = Packet.from_byte_S(self.byte_buffer[0:length])
#             ret_S = p.msg_S if (ret_S is None) else ret_S + p.msg_S
#             #remove the packet bytes from the buffer
#             self.byte_buffer = self.byte_buffer[length:]
#             #if this was the last packet, will return on the next iteration
            
    
#     def rdt_2_1_send(self, msg_S):
#         pass
        
#     def rdt_2_1_receive(self):
#         pass
    
#     def rdt_3_0_send(self, msg_S):
#         pass
        
#     def rdt_3_0_receive(self):
#         pass



BUFSIZ = 1024
lossRate = 0.5
timeout = 2 # not needed
Port = 8009
rcvPort = 8008
rcvlocal = "127.0.0.1"
rcvlocal = (rcvIP,rcvPort)
sd = None

# Calculate md5 hash
def CheckSum(Data):
    hash = hashlib.md5(Data).digest()
    return hash

# Assign and bind a socket
def Sock_A():
        global sd
        sd = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sd.bind(("localhost",Port))

def RDT():
    Sock_A()
    # current = 0
    # winSize = 4
    filename = RecvData()
    Data = []
    while(True):
        # Blocking wait for Receive
        msg1 = RecvData()
        # Check if Transfer Complete
        if(msg1==b'FIN'):
            SendData(b'FIN')
            break
        # Simulate Loss
        if(random.random()<lossRate):
            print("Client Not Responding/Dropping Packet")
            time.sleep(timeout+1)
            continue
        # Deserialize the data
        data = pickle.loads(msg1)
        print(data)
        msg = data.Data.decode("utf-8")
        print(msg)
        chk = CheckSum(data.Data)
        # print(chk)
        # print(data.CheckSum)
        # Verify Checksum and duplicate packet
        if chk==data.CheckSum:
            if(data.SeqN<len(Data)):
                print("Duplicate Packet!")
                continue
            print("Valid Checksum")
            Data.append(msg)
        else:
            print("Invalid Checksum")
        # Create and Send Ack
        ack = pickle.dumps(Ack(data.SeqN))
        SendData(ack)
    Output = " ".join(Data)
    print("Message Received:", Output)
    return

def SendData(message):
    sd.sendto(message, rcvAdd)
    return

def RecvData():
    (msg1, addr) = sd.recvfrom(BUFSIZ)
    return msg1

RDT()



class Packet:
    ## the number of bytes used to store packet length
    seq_num_S_length = 10
    length_S_length = 10
    ## length of md5 checksum in hex
    checksum_length = 32 
        
    def __init__(self, seq_num, msg_S):
        self.seq_num = seq_num
        self.msg_S = msg_S
        
    @classmethod
    def from_byte_S(self, byte_S):
        if Packet.corrupt(byte_S):
            raise RuntimeError('Cannot initialize Packet: byte_S is corrupt')
        #extract the fields
        seq_num = int(byte_S[Packet.length_S_length : Packet.length_S_length+Packet.seq_num_S_length])
        msg_S = byte_S[Packet.length_S_length+Packet.seq_num_S_length+Packet.checksum_length :]
        return self(seq_num, msg_S)
        
    # if __name__ == '__main__':
    # parser =  argparse.ArgumentParser(description='RDT implementation.')
    # parser.add_argument('role', help='Role is either client or server.', choices=['client', 'server'])
    # parser.add_argument('server', help='Server.')
    # parser.add_argument('port', help='Port.', type=int)
    # args = parser.parse_args()
    
    # rdt = RDT(args.role, args.server, args.port)
    # if args.role == 'client':
    #     rdt.rdt_1_0_send('MSG_FROM_CLIENT')
    #     sleep(2)
    #     print(rdt.rdt_1_0_receive())
    #     rdt.disconnect()
        