TCP-like Reliable File Transfer with Congestion Control over UDP

## Objective

The objective of this assignment is to develop a UDP-based file transfer client that ensures reliable data transfer while implementing congestion control mechanisms. The client interacts with a server to request and receive file data, ensuring that data integrity is maintained using MD5 hash verification. Additionally, the client adapts to network conditions to prevent penalties and squishing, ensuring efficient file transfer.

The project is divided into three milestones:

1. **Milestone 1**: Reliable data transfer by sending requests slowly and handling lost requests due to network or server-side loss.
2. **Milestone 2**: Implementing the client for a constant rate server using leaky bucket parameters.
3. **Milestone 3**: Generalizing the client to handle a variable rate server using a token bucket model.

## Approach

### 1. Reliable Data Transfer

For reliable data transfer, the client sends file requests and handles the loss of requests or responses by retransmitting any missing pieces. The server simulates different loss rates, and the client ensures it receives all parts of the file before verifying the MD5 hash for data integrity.

### 2. AIMD Approach for Congestion Control

To ensure efficient transfer without overwhelming the server, the client uses an **Additive Increase, Multiplicative Decrease (AIMD)** approach:
- Requests are sent in bursts, and the burst size is incremented by 1 whenever the client successfully receives replies for all sent requests.
- If a reply is not received, the burst size is halved to avoid overwhelming the server.

### 3. Timeout Calculation

The client adapts its timeout intervals using **Exponential Weighted Moving Average (EWMA)**, similar to TCP’s approach:
- **Sample RTT**: Measured as the time between sending a request and receiving a response.
- **Estimated RTT**: An EWMA of the sample RTTs.
- **DevRTT**: An EWMA of the deviation between the sample RTT and the estimated RTT.

The timeout interval is calculated as:
```bash
TimeoutInterval = EstimatedRTT + 2 * DevRTT
```
This ensures the timeout is dynamically adjusted based on current network conditions.

### 4. Handling Variable Server Rate

In milestone 3, the server operates with a variable token generation rate. To handle this:
- The client reduces the burst size continuously if the server rate decreases, ensuring that the number of requests sent does not exceed the server’s capacity.
- In case of squishing (when the server is overwhelmed), the client’s burst size is reduced to 1 and locked until the squishing period ends.

### 5. Request Window Management

The client maintains a list of offsets representing parts of the file that have not been received. It sends requests for the first few unreceived offsets in each burst. Once a piece of data is received, the corresponding offset is removed from the list to avoid duplicate requests.

### 6. Doubling the Timeout Interval

If a timeout occurs for a specific request, the client doubles the timeout interval for that request and resends it. This reduces the chances of repeated timeouts for the same request in congested or lossy network conditions.

## Observations

- The AIMD approach ensures that the client gradually increases its request rate when the network conditions are favorable and reduces it when packet loss or server-side squishing occurs.
- The dynamic timeout calculation using EWMA ensures that the client adjusts to varying network latencies effectively.
- On a local server with 1 lakh lines of data, the client completed the transfer in approximately **25 seconds** with zero squishing and fewer than 30 penalties.
- On the Vayu server (50,000 lines of data), the client took **25-30 seconds** with penalties ranging between 20-30 and no squishing.

## Exception Handling

- All critical operations within the file transfer loop are wrapped in `try`-`except` blocks to handle errors like connection timeouts or lost responses gracefully.
- A **Squish Lock** mechanism is employed to prevent further requests when squishing occurs, ensuring that the client does not overwhelm the server during congested periods.
