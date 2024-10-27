import socket
import hashlib
import threading
import time

start=time.time()
lock = threading.Lock()
#'10.17.7.134'

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.settimeout(0.04)
msg="SendSize\nReset\n\n"

port_number=9802
ip_add='127.0.0.1'

squish_lock=0
#time_segment=0.5
number_of_req=1

number_of_bytes = 0

L=[]

time_sent={}
time_recv={}

RTT_estimation=0.004
Dev_estimation=0.0001
time_out=0.0043




while True:

    try:
        client_socket.sendto(msg.encode("utf-8"), (ip_add, port_number))
        data, addr = client_socket.recvfrom(4096)
        number_of_bytes = int((data.decode())[6:-2])
        #print(number_of_bytes)
        #print("system baith gaya hai")
        break
    except:

        continue


thisdic = {}
# time_1={}
# time_2={}

count = 0
rem = number_of_bytes % 1448
div = number_of_bytes // 1448
target = div

if rem!=0:
    while True:
        try:
            msg=""
            msg = "Offset: " + str(target*1448) + "\n"
            msg+="NumBytes: "+ str(rem)+"\n\n"
            client_socket.sendto(msg.encode("utf-8"), (ip_add, port_number))
            data, addr = client_socket.recvfrom(4096)
            data_recv=data.decode()
            le=len(data_recv)
            thisdic[target]=data_recv[le-rem:]
            break
        except:
            continue

for i in range(0,target):
    L.append(i)

client_socket.settimeout(None)
count_vadapav=0

def thread_2():
    global count,target,thisdic,L,count_vadapav,squish_lock,time_sent,time_out,Dev_estimation,RTT_estimation
    while count<target:
        try:
            data, addr = client_socket.recvfrom(2048)
            data_recv = data.decode()
            dummy = data_recv.split('\n')
            offset = int(dummy[0][8:])/1448
            dummy = data_recv.split('\n')
            if dummy[2] == 'Squished':
                count_vadapav += 1
                squish_lock = 1
                print(count_vadapav)
            else:
                squish_lock = 0

            if offset not in thisdic.keys():
                le = len(data_recv)
                thisdic[offset] = data_recv[le - 1448:]

                count+=1
                #print(count)
                sample_rtt=time.time()-time_sent[offset]
                RTT_estimation=0.95*RTT_estimation+0.05*sample_rtt
                Dev_estimation=0.9*Dev_estimation+0.1*abs(sample_rtt-RTT_estimation)
                time_out=RTT_estimation+2*Dev_estimation


                # time_2[time.time()-start]=offset*1448

                # time_dic[offset] = time.time() - start
        except:
            continue

def thread_1():
    global count, target, thisdic, L, number_of_req,squish_lock,time_sent,time_out

    while count<target:
        count_recv_prev = count
        no_sent=0
        indx=0
        # time_1[time.time()-start]=number_of_req
        while no_sent<number_of_req:
            if indx==target:
                break
            elif indx not in thisdic.keys():
                msg = ""
                msg = "Offset: " + str(indx * 1448) + "\n"
                msg += "NumBytes: " + str(1448) + "\n\n"
                client_socket.sendto(msg.encode("utf-8"), (ip_add, port_number))
                time_sent[indx]=time.time()
                #time_1[time.time()-start]=indx*1448
                no_sent+=1
                time.sleep(0.0006)
            indx+=1
        #print(time_out)
        # time.sleep(time_out)
        time.sleep(max(time_out,0.015))
        # time.sleep(0.02)
        # print(no_sent,end=" ")

        req_recv=count-count_recv_prev
        # print(req_recv)
        if req_recv-no_sent>=0:
            number_of_req=number_of_req+1
        else:
            #number_of_req=2*(number_of_req)/3
            number_of_req=number_of_req//2
            #print(no_sent)
            #print("yes")
            if number_of_req<=1:
                number_of_req=1
        if squish_lock==1:
            number_of_req=1

        #time.sleep(0.01)
    #print(number_of_req)
    submit_string = ""
    for k in range(0, target):
        #print(k)
        submit_string += thisdic[k]
    if rem != 0:
        submit_string += thisdic[target]

    md5_hash = hashlib.md5(submit_string.encode('utf-8'))
    md5_hex = md5_hash.hexdigest()
    client_socket.settimeout(0.04)
    while True:
        try:
            msg = "Submit: 2021CS10562@virat\n"
            msg += "MD5: " + md5_hex + "\n\n"
            client_socket.sendto(msg.encode("utf-8"), (ip_add, port_number))
            data, addr = client_socket.recvfrom(4096)
            chk_str=data.decode()
            if(chk_str[0]=='R'):
                print(data.decode())
                print(time.time() - start)



                # for i in range(0, target):
                #     print(time_dic[i])
                # i=0
                # while i<target:
                #     print(time_dic[i])
                #     i=i+3
                break
        except:
            continue
    client_socket.close()

t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)

t2.start()
t1.start()

t2.join()
t1.join()







