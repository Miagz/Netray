# encoding: utf-8
import sys
import pty
import tty
from select import select
import os
import signal
from socket import *
# 创建pty设备(从主)
class server(object):
    def __init__(self,host_port):
        self.host_port = host_port
    def hup_handle(self,signum,frame):
        sock.send("\n")
        sock.close()
        raise SystemExit
    def main(self):
        self.m,self.s = pty.openpty()
        self.pid = os.fork()
        if self.pid == 0:
            os.setsid()
            os.close(self.m)
            # 将子进程的stdio连接到pty的从设备
            os.dup2(self.s,0) #将一个文件描述符 s 复制到另一个 0
            os.dup2(self.s,1)
            os.dup2(self.s,2)
            # exec特性,除非失败,否则不会返回
            os.execlp("/bin/sh","/bin/sh")
            os.close(self.s)
        else:
            #"子进程创建成功, PID为:"+pid
            os.close(self.s)
            signal.signal(signal.SIGINT,self.hup_handle) #处理键盘信号

            try:
                sock = socket(AF_INET, SOCK_STREAM)
                sock.setsockopt(SOL_SOCKET,SO_REUSEADDR ,1)
                sock.bind(self.host_port)
                sock.listen(5)
                conn,addr = sock.accept()
                conn.settimeout(3)
                fds = [self.m,conn]
                mode = tty.tcgetattr(0)
                while True:
                    # if not conn.connect_ex(addr):raise Exception
                    r,w,e = select(fds,[],[])
                    if self.m in r:
                        data = os.read(self.m,1024)
                        if data:
                            conn.send(data)
                        else:
                            fds.remove(self.m)
                    if conn in r:
                        data = conn.recv(1024)
                        if not data:
                            fds.remove(conn)
                            conn.close()
                            sock.close()
                        if data:
                            os.write(self.m,data)
            except Exception as e:
                print(e)
                conn.close()
                sock.close()
            finally:
                os.close(self.m)

class client(object):
    def __init__(self,host_port):
        self.host_port = host_port 
        try:
            self.conn = socket(AF_INET, SOCK_STREAM)
            self.conn.connect(self.host_port)
            self.mode = tty.tcgetattr(0)
        except Exception as e:
            print(e)
            raise SystemExit
    def main(self):
        tty.setraw(sys.stdin.fileno())
        try:
            while True:
                r,w,e = select([sys.stdin,self.conn],[],[])
                if self.conn in r:
                    data = self.conn.recv(1024)
                    if data:
                        os.write(sys.stdout.fileno(),data)
                    else:
                        raise SystemExit
                if sys.stdin in r:
                    self.conn.send(os.read(sys.stdin.fileno(),1024))
        except Exception as e:
            print(e)
        finally:
            tty.tcsetattr(sys.stdin.fileno(),tty.TCSAFLUSH,self.mode)
