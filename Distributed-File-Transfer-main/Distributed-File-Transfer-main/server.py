import socket
import time
import threading

start = time.time()

set_check={-1}

dic = {}
set_1={-1}
check_l1 = [0] * 1000
check_l2 = [0] * 1000
check_l3 = [0] * 1000
l = []
i1 = 0
i2 = 0
i3 = 0
submitted=0
porti=0


def vayu_cn():
    global dic, start, l,submitted,porti,set_check
    vayu_socket = socket.socket()
    vayu_socket.connect(("10.17.7.134", 9801))
    # print("SYSTEM BETH GYA")
    porti=vayu_socket
    payload = b"SENDLINE\n"

    while True:
        if (len(dic) >= 1000):

            # print(sorted(set_check))
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

        words = message.split("\n")
        if words[0] != '-1':
            if int(words[0]) not in set_1:
                l.append(message)
                set_1.add(int(words[0]))
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]
                # print(len(dic))
    vayu_socket.close()


def recv_slave1():
    global dic, l, check_l1,submitted,porti,set_check
    host = socket.gethostname()
    port = 12455

    slave_s11 = socket.socket()
    slave_s11.bind((host, port))
    slave_s11.listen(1)

    while True:
        try:
            slave_s1, address = slave_s11.accept()
            break
        except TimeoutError:
            continue

    while True:
        if(len(dic)>=1000):
            print(sorted(set_check))
            payload1 = b"SUBMIT\naseth@col334-672\n1000\n"
            for i in range(0, 1000):
                payload1 += str(i).encode()
                payload1 += b"\n"
                payload1 += dic[i].encode()
                payload1 += b"\n"
            porti.sendall(payload1)
            message = ""
            while True:
                data = porti.recv(4096).decode()
                message += data
                if (data[-1] == "\n"):
                    break
            print(message)
            print(time.time() - start)

            break

        message = ""
        count = 0
        while True:
            data = slave_s1.recv(1024).decode()

            message += data

            if data[-1] == "\n":
                break

        # print("s1")
        # print(len(dic))

        words = message.split("\n")

        slave_s1.send((words[0] + "\n").encode())


        if words[0] != '-1':
            if int(words[0]) not in set_1:
                l.append( message)
                set_1.add(int(words[0]))
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]


def send_slave1():
    global i1, dic, l, check_l1,submitted,set_check

    host = socket.gethostname()
    port = 12456

    slave11_send = socket.socket()
    slave11_send.bind((host, port))
    slave11_send.listen(1)

    while True:
        try:
            slave1_send, address = slave11_send.accept()
            break
        except TimeoutError:
            continue

    while True:


        if i1 < len(l):


            slave1_send.send((l[i1]).encode())
            smth=l[i1].split("\n")
            set_check.add(int(smth[0]))

            message = ""
            while True:
                data = slave1_send.recv(1024).decode()

                message += data
                if data[-1] == '\n':
                    break
            i1+=1






def recv_slave2():
    global dic, l, check_l2,submitted,porti,set_check
    host = socket.gethostname()
    port = 12457

    slave_s12 = socket.socket()
    slave_s12.bind((host, port))
    slave_s12.listen(1)

    while True:
        try:
            slave_s2, address = slave_s12.accept()
            break
        except TimeoutError:
            continue

    while True:
        if (len(dic) >= 1000):
            print(sorted(set_check))
            payload1 = b"SUBMIT\naseth@col334-672\n1000\n"
            for i in range(0, 1000):
                payload1 += str(i).encode()
                payload1 += b"\n"
                payload1 += dic[i].encode()
                payload1 += b"\n"
            porti.sendall(payload1)
            message = ""
            while True:
                data = porti.recv(4096).decode()
                message += data
                if (data[-1] == "\n"):
                    break
            print(message)
            print(time.time() - start)

            break

        message = ""
        count = 0
        while True:
            data = slave_s2.recv(1024).decode()

            message += data
            if data[-1] == "\n":
                break

        # print("s2")
        # print(len(dic))

        words = message.split("\n")

        slave_s2.send( ("hii\n").encode())

        if words[0] != '-1':
            if int(words[0]) not in set_1:
                l.append( message)
                set_1.add(int(words[0]))
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]


def send_slave2():
    global i2, dic, l, check_l2,submitted

    host = socket.gethostname()
    port = 12458

    slave21_send = socket.socket()
    slave21_send.bind((host, port))
    slave21_send.listen(1)

    while True:
        try:
            slave2_send, address = slave21_send.accept()
            break
        except TimeoutError:
            continue

    while True:


        if i2 < len(l):

            slave2_send.send(l[i2].encode())
            message = ""
            while True:
                data = slave2_send.recv(1024).decode()

                message += data
                if data[-1] == '\n':
                    break


            i2 += 1

           


def recv_slave3():
    global dic, l,submitted,porti
    host = socket.gethostname()
    port = 12459

    slave_s13 = socket.socket()
    slave_s13.bind((host, port))
    slave_s13.listen(1)

    while True:
        try:
            slave_s3, address = slave_s13.accept()
            break
        except TimeoutError:
            continue

    while True:
        if (len(dic) >= 1000):
            print(sorted(set_check))
            payload1 = b"SUBMIT\naseth@col334-672\n1000\n"
            for i in range(0, 1000):
                payload1 += str(i).encode()
                payload1 += b"\n"
                payload1 += dic[i].encode()
                payload1 += b"\n"
            porti.sendall(payload1)
            message = ""
            while True:
                data = porti.recv(4096).decode()
                message += data
                if (data[-1] == "\n"):
                    break
            print(message)
            print(time.time() - start)

            break


        message = ""
        count = 0
        while True:
            data = slave_s3.recv(1024).decode()
            if not data:
                continue
            message += data
            if data[-1] == "\n":
                break

        # print("s3")
        # print(len(dic))

        words = message.split("\n")

        slave_s3.send((words[0] + "\n").encode())

        if words[0] != '-1':
            if int(words[0]) not in set_1:
                set_1.add(int(words[0]))
                l.append(message)
            if int(words[0]) not in dic.keys():
                dic[int(words[0])] = words[1]


def send_slave3():
    global i3, dic, l,submitted,set_1

    host = socket.gethostname()
    port = 12460

    slave31_send = socket.socket()
    slave31_send.bind((host, port))
    slave31_send.listen(1)

    while True:
        try:
            slave3_send, address = slave31_send.accept()
            break
        except TimeoutError:
            continue

    while True:

        if i3 < len(l):
            slave3_send.send(l[i3].encode())
            message = ""
            while True:
                data = slave3_send.recv(1024).decode()
                if not data:
                    continue
                message += data
                if data[-1] == '\n':
                    break


            i3 += 1

            


t1 = threading.Thread(target=vayu_cn)
t2 = threading.Thread(target=recv_slave1)
t3 = threading.Thread(target=send_slave1)
t4 = threading.Thread(target=recv_slave2)
t5 = threading.Thread(target=send_slave2)
t6 = threading.Thread(target=recv_slave3)
t7 = threading.Thread(target=send_slave3)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
