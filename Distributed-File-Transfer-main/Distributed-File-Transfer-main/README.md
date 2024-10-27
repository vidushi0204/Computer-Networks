Distributed File Download and Reassembly System as part of Computer Networks course at IIT Delhi (2023-24, Semester I)

## Objective

The objective of this assignment is to implement a distributed file download and reassembly system. Multiple clients (1-4) collaboratively download and reassemble a file in the shortest time possible. Each client requests a random line from the server, shares the received lines with other clients, and works together to reassemble the complete file.

## System Overview

We implemented a Peer-to-Peer (P2P) system where:
- **Master Client**: Manages downloading and assembly of the file. It receives lines from both the server and slave clients.
- **Slave Clients**: Download parts of the file from the server and exchange missing lines with the master client.

### Flow of Communication

```plaintext
Server <--> Master <--> Slave 1
                         <--> Slave 2
                         <--> Slave 3
```

## Approach

### 1. **Data Structure - Dictionary (dic)**

Each client maintains a dictionary to store the received lines. The key is the line index, and the value is the line content. Once the dictionary size reaches 1000 (the total number of lines), the client submits the complete file to the server.

### 2. **Master Client Role**

The master client has the following responsibilities:
- **Downloading from Server**: Requests lines from the server and stores them in the dictionary.
- **Receiving from Slaves**: Receives lines from slave clients and adds any new, unique lines to the dictionary.
- **Sharing with Slaves**: Sends downloaded lines to slave clients.
- **Submission**: Submits the file to the server once the dictionary contains all 1000 lines.

The master client uses 7 threads:
- 1 thread to communicate with the server.
- 6 threads for communication with slave clients (3 for sending lines, 3 for receiving).

### 3. **Slave Client Role**

The slave clients perform the following actions:
- **Downloading from Server**: Requests random lines from the server and stores them in the dictionary.
- **Sharing with Master**: Sends downloaded lines to the master client.
- **Requesting from Master**: Requests missing lines from the master client to complete the file.

The slave clients work in parallel to minimize the overall time to download and assemble the file.

### 4. **Concurrency Management**

Each client runs multiple threads:
- The master client manages server communication and communication with multiple slaves.
- Slave clients handle communication with the master to ensure missing lines are requested and received efficiently.

## Test Cases and Results

We tested the system using the following configurations:
- **Run 1**: Single client (master only) downloads the file.
- **Run 2**: Two clients (1 master, 1 slave) download and reassemble the file.
- **Run 3**: Three clients (1 master, 2 slaves) work in parallel.
- **Run 4**: Four clients (1 master, 3 slaves) collaborate.

### Results

Here are the submission times for the master client across the test runs:

| Run Configuration     | Submission Time (Seconds) |
|-----------------------|---------------------------|
| Run 1 (Single client)  | 69.26 seconds             |
| Run 2 (Two clients)    | 56.22 seconds             |
| Run 3 (Three clients)  | 29.98 seconds             |
| Run 4 (Four clients)   | 20.10 seconds             |

### Performance Plots

- The submission time reduces as the number of clients increases. This behavior is expected, as multiple clients share the task of downloading and assembling the file.
- However, the speedup is not perfectly linear due to the communication overhead between the master and slave clients.

## Observations

1. **Time Reduction**: As more clients participate, the submission time decreases. However, there is diminishing return due to communication overhead as more clients are added.
2. **Thread Management**: The master client handles multiple threads for communication, which increases complexity as the number of slave clients increases.
3. **File Assembly**: Once the file is completely assembled, the master submits it to the server, and the process is concluded.

## Exception Handling

### Client Disconnection
- If a client disconnects mid-process, the system is designed to continue without the client. The master client maintains a record of which lines have already been received and ensures no duplicate lines are processed.

### Line Acknowledgment
- To ensure lines are not lost during transmission, each line sent by a client is acknowledged by the receiver. This prevents missing or duplicate lines and guarantees the file is assembled correctly.
