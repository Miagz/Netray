import socket
import os,sys
import argparse
import platform
import struct,json,math
class conn(object):
    def __init__(self,Port,reverse,Host=""):
        self.delimiter = b"\xef"
        self.Host = Host
        self.Port = Port
        self.reverse = reverse
        self.bufsize=8000
        if self.reverse:
            self.host_port=(self.Host,self.Port)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind(self.host_port)
            self.sock.listen(5)
        else:
            self.host_port=(self.Host,self.Port)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.sock.connect(self.host_port)
                print("connection succeeded")

            except Exception as e :
                print('connect error: {}'.format(e))
                sys.exit()
    def conn(self):
        status=False
        while not status:
            if self.reverse:
                sockets,client_addr=self.sock.accept() # 收连接者数据-堵塞式
                ip,port=client_addr
            else:
                sockets=self.sock
            while not status:
                info=sockets.recv(self.bufsize).decode() # 接收返回的信息
                value = self.habit(input(info),sockets)      
                try:
                    sockets.send(value.encode())
                    data=sockets.recv(1000000) # 接收返回的数据
                    print(data.decode())
                except:
                    print("%s Disconnected"%(self.Host))
                    if self.reverse:
                        self.sock.close()
                        sockets.close()
                    else:
                        sockets.close()
                    sys.exit()


    def habit(self,value,sockets):
        command = value.split(' ')
        if platform.system()=='Windows':
            if not command[0].strip():
                value = "ignore"
            elif command[0] =="quit" or command[0] =="exit":
                sys.exit()
            elif command[0]=="quit_service":
                sockets.send(command[0].encode())
                sys.exit()
            elif command[0] == 'upload':
                if len(command)>1:
                    if len(command)>2:
                        if os.path.exists(command[1]):
                            sockets.send(value.encode()) # 向被控端发送upload命令
                            self.upload(sockets,command[1],command[2])
                            value = " "
                        else:
                            print(" {} 文件不存在".format(command[1]))
                            value = "ignore"
                    else:
                        print("远程会话存放路径未选择")
                        value = "ignore"
                else:
                    print("请选择文件路径")
                    value = "ignore"
        return value

    def upload(self,conn,file_path,service_file_path):
        max_output_size = 65536
        info_dict={
        "filename":service_file_path,
        "max_output_size":max_output_size
        }
        header_bytes = json.dumps(info_dict).encode()
        header_len = struct.pack('i', len(header_bytes))
        conn.send(header_len)
        conn.send(header_bytes)#报文头
        total_size = os.path.getsize(file_path)

        file = open(file_path, "rb")
        self.sent=0
        while 1:

            buf = file.read(max_output_size)
            self.progressbar(len(buf),total_size)
            self.sent += len(buf)
            if len(buf)<=0:
                conn.send(b'hello_word_file_is_end')
                break
            conn.send(buf)
        print("\n传输完成")
        file.close()

    def progressbar(self,max_output_size,total_size):
        percent='{:.2%}'.format(self.sent/total_size)
        test = "%sKB|%sKB"%(self.sent//1024,total_size//1024)
        sys.stdout.write('\r') 
        sys.stdout.write('%s[%-50s] %s'%(percent,'#'*int(math.floor(self.sent*50/total_size)),test))
        sys.stdout.flush()   



class cmd(object):
    def __init__(self):
        parser=argparse.ArgumentParser()
        parser.description="test"
        parser.add_argument('-r',action="store_true",help='tcp反向连接,客户端连接本机')
        parser.add_argument('-s',type=str,help='主机名')
        parser.add_argument('-p',type=int,help='端口')
        args=parser.parse_args()
        if args.r:
            if args.p:
                print("Waiting for connection... ")
                conn(args.p,True,"").conn()
            else:
                print("Please enter the port ")
        else:
            if args.s and args.p:
                conn(args.p,False,args.s).conn()
            else:
                print("Please enter the host and port")
        
cmd()

