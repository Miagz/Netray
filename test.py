
from tqdm import tqdm
import time
for i in tqdm(range(10000)):
    time.sleep(0.01)

# for i in
# for i in open('E:\\系统镜像\\Centos6.iso','rb').read(65536):
# file = open('E:\\Desktop\\1.pdf','rb')
# while 1:
#     buf = file.read(65536)
#     if len(buf)<=0:
#         break
#     print(len(buf))
# file.close()
# file = b'hello_word_file_is_end'
# print(len(file))
# import math
# import sys
# def progressbar(cur,total):
#     percent = '{:.2%}'.format(cur / total)
#     sys.stdout.write('\r')
#     sys.stdout.write('[%-50s] %s' % ( '#' * int(math.floor(cur * 50 /total)),percent))
#     sys.stdout.flush()
#     if cur == total:
#         sys.stdout.write('\n')
 
# if __name__ == '__main__':
#     file_size = 102400000
#     size = 1024
#     while file_size > 0:
#         progressbar(size,file_size)
#         file_size -= 1024
# import sys  
# import time
# for i in range(51):
#     time.sleep(0.1)
#     sys.stdout.write('\r') 
#     sys.stdout.write('[%-50s]'%('#'*i))  
#     sys.stdout.flush()

# size=65536

# zhuan=62845548
# count=0
# while 1:
#     zhuan-=size
#     if zhuan<=0:
#         break
#     print('percent: {:.2%}'.format(count/zhuan))
#     count+=size

import sys,math
block = 65536
sumb = 5374584761
sent = 0
# percent = '{:.2%}'.format(sent / sumb)
# value= '[%-50s] %s'%('#'*int(math.floor(sent/sumb*50)),percent)
# print(value)

while 1:
    percent='{:.2%}'.format(sent/sumb)
    sys.stdout.write('\r') 
    sys.stdout.write('[%-50s] %s'%('#'*int(math.floor(sent/sumb*50)),percent))
    sys.stdout.flush()
    # send
    sent += block
    if sent >= sumb:
        sys.stdout.write('\r')
        sys.stdout.write('[%-50s]'%('#'*50))
        sys.stdout.flush()
        break