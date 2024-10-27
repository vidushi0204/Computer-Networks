import socket
import threading
import time

start = time.time()
set_1={-1}
dic = {}
l = []
i1 = 0


def vayu_cn():
    global dic, start, l
    vayu_socket = socket.socket()
    vayu_socket.connect(("10.17.7.134", 9801))

    payload = b"SENDLINE\n"

    while True:
        if (len(dic) >= 1000):
            payload1 = b"SUBMIT\naseth@col334-672\n1000\n"
            for i in range(0, 1000):
                payload1 += str(i).encode()
                payload1 += b"\n"
                payload1 += dic[i].encode()
                payload1 += b"\n"
            vayu_socket.sendall(payload1)
            message = ""
            while True:
                data = vayu_socket.recv(4096).decode()
                message += data
                if (data[-1] == "\n"):
                    break
            print(message)
            print(time.time() - start)
            break
            
        vayu_socket.send(payload)
        message = ""
        while True:
            data = vayu_socket.recv(4096).decode()
            message += data
            if (data[-1] == "\n"):
                break

        # l.append(message)
        words = message.split("\n")
        if words[0] != '-1':
            if int(words[0]) not in set_1:
                l.append(message)
                set_1.add(int(words[0]))
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]
                # print(len(dic))
    vayu_socket.close()


def send_master():
    global i1, l
    host = "10.194.0.163"
    port = 12455

    master_send = socket.socket()
    master_send.connect((host, port))

    while True:
        if i1 < len(l):
            master_send.send(l[i1].encode())
            message = ""
            while True:
                data = master_send.recv(1024).decode()
                message += data
                if data[-1] == '\n':
                    break
            # print(message)
            i1 += 1
            


def recv_master():
    global dic, l 

    host = "10.194.0.163"
    port = 12456

    master_recv = socket.socket()
    master_recv.connect((host, port))

    while True:
        message = ""
        # count = 0
        while True:
            data = master_recv.recv(1024).decode()
            
            message += data
            if data[-1] == "\n":
                break
              
        words = message.split("\n")
        if len(words[0]) > 0:
            master_recv.send((words[0] + "\n").encode())
        else:
            master_recv.send("-1"+"\n".encode())
            
        if words[0] != '-1':
            if int(words[0]) not in set_1:
                set_1.add(int(words[0]))
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]
                # print(len(dic))


t1 = threading.Thread(target=vayu_cn)
t2 = threading.Thread(target=send_master)
t3 = threading.Thread(target=recv_master)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()