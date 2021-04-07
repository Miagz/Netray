import socket
import os,sys
import platform
import struct,json,math

class client(object):
    def __init__(self,Host,Port,reverse):
        self.Host = Host
        self.Port = Port
        self.reverse = reverse
        self.bufsize=8000
        if self.reverse:
            self.host_port=(self.Host,self.Port)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.sock.bind(self.host_port)
            except:
                print("The port is occupied or the port is greater than 65535")
                sys.exit()
            self.sock.listen(5)
        else:
            self.host_port=(self.Host,self.Port)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.sock.connect(self.host_port)
                print("connection succeeded")

            except Exception as e :
                print('Netray: {}'.format(e))
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
                            print(" {} file does not exist".format(command[1]))
                            value = "ignore"
                    else:
                        print("The remote session storage path is not selected ")
                        value = "ignore"
                else:
                    print("Please select file path ")
                    value = "ignore"
        return value

    def progressbar(self,max_output_size,total_size):
        percent='{:.2%}'.format(self.sent/total_size)
        test = "%sKB|%sKB"%(self.sent//1024,total_size//1024)
        sys.stdout.write('\r') 
        sys.stdout.write('%s[%-50s] %s'%(percent,'#'*int(math.floor(self.sent*50/total_size)),test))
        sys.stdout.flush()   

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
        print("\nTransfer complete ")
        file.close()
    def download(self,conn,service_file_path,file_path):
        pass



