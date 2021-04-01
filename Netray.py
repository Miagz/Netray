#encoding:utf-8
from Client import client
from Service import service
import argparse
import sys
import re

class  netray(object):
    """docstring for  netray"""
    def __init__(self,hostname,port):
        super(netray, self).__init__()
        parser=argparse.ArgumentParser()
        parser.description="Netray Hostname[None] port [-Options] ..."
        parser.add_argument('-r',action="store_true",help='Netray reverse connection')
        parser.add_argument('-s',action="store_true",help='Server,Passive control')
        parser.add_argument('-c',action="store_true",help='Client,Control')
        args=parser.parse_args()
        if not args.s and not args.c:
            print("[ERROR] Please select Control[-c] or Passive control[-s] ")
            sys.exit()
        if args.s and args.c:
            print("[ERROR] [-s] and [-c] cannot exist at the same time")
            sys.exit()
        if len(hostname)>1 and args.s and not args.r:
            print("[WARNING] No need to enter the host name ")
        elif len(hostname)>1 and args.c and  args.r:
            print("[WARNING] No need to enter the host name ")
        if args.s:
            if args.r:service(hostname,port,True).conn()
            else:service(hostname,port,False).conn()
        elif args.c:
            if args.r:
                client(hostname,port,True).conn()
            else:
                client(hostname,port,False).conn()


if __name__ == "__main__":
    # 判断ip是否规范
    pattern = re.compile(r'^(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1}|[1-9]{1}\d{1}|1\d\d|2[0-4]\d|25[0-5])$')
    hostname,port = sys.argv[1],sys.argv[2]
    try:
        int(sys.argv[1])
        hostname = ""
        port = sys.argv[1]
        sys.argv = sys.argv[1:] #获取到port之后清除终端上的port
    except:
        sys.argv = sys.argv[2:]  #获取到hostname和port之后清除终端上的hostname和port
    if hostname == "":pass
    elif not pattern.search(hostname): #判断ip是否正确
        print("[ERROR] Please enter the correct ip")
        sys.exit()
    if int(port)>65535:
        print("[ERROR] port error! Please enter the correct port")
        sys.exit()
    netray(hostname,int(port))