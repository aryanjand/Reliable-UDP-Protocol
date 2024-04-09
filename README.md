# Network Reliability Mechanisms over UDP

## COMP 7005 - Applied Computer Science, Network Security Applications Development Option Jan 2024

This project is a pairs assignment for COMP 7005. If you intend to work alone, you must obtain the instructor's permission.

### Objective
- Understand and implement reliability mechanisms over an unreliable protocol (UDP) akin to TCP's.
- Explore the challenges and solutions in ensuring data integrity and delivery in network communication.

### Learning Outcomes
- Gain practical experience in socket programming with UDP.
- Understand the principles behind TCP’s reliability and how to implement similar mechanisms in UDP.
- Develop skills in creating robust network applications that can handle network unreliability.
- Learn to use command-line arguments for dynamic application configuration.
- Analyze and interpret network behavior through data visualization.

### Components
#### Client
- Sends data to the server via the proxy.
- Must handle acknowledgments and timeouts.

#### Server
- Receives data from the client, processes it, and possibly sends a response.
- Must handle duplicate and out-of-order packets.

#### Proxy
- Simulates network unreliability.
- Introduces packet loss and delays according to specified probabilities and ranges.
  - % chance to drop packets coming from the client
  - % chance to drop packets coming from the server
  - % chance to drop delay coming from the client
  - % chance to drop delay coming from the server
  - Range (min/max) milliseconds to delay if a packet is delayed coming from the client
  - Range (min/max) milliseconds to delay if a packet is delayed coming from the server

### Functionality
- Implement reliability features such as packet acknowledgment, retransmission on timeout, and sequence numbering to handle duplicates and ordering.
- Use command-line arguments to configure all parameters (e.g., IP addresses, ports, packet drop probability, delay range, etc.).
- Bonus: real-time graph.

### Visualization
- Generate graphs to visualize packets sent, received, retransmitted packets, etc., for both the client and server.

### Documentation
#### Design Document
- Describe the architecture, components, and algorithms used to ensure UDP reliability.

#### Testing Document
- Detail the testing methodology, scenarios, and outcomes.
- Include how the proxy's behavior was varied, how the system was observed, and how it responded to different challenges.

### Constraints
- Follow the guidelines.
- Ensure all components are robust against network unreliability scenarios.
- Dynamic configuration through command-line arguments is mandatory; hardcoding of parameters is not allowed.
- Both students must participate equally in all aspects of the project, or you may fail.

### Resources
- Provide references to UDP and TCP documentation, socket programming tutorials, and any libraries or tools used for graph generation.

Project Structure

udp_reliable/
│
├── client/
│   ├── __init__.py
│   └── client.py
│
├── server/
│   ├── __init__.py
│   └── server.py
│
├── proxy/
│   ├── __init__.py
│   └── proxy.py
│
└── utils/
    ├── __init__.py
    └── packet.py


BaseReliability Class
- Abstraction (Abstract Class)

Packet Class
- Reliability Attributes


Session Class
- Teardown

ClientSession Class
- 3-Way Handshake

ClientConnection Class


TCP (Transmission Control Protocol) is considered reliable due to several key features and mechanisms designed to ensure the reliable delivery of data:

    Acknowledgment: TCP uses acknowledgments to ensure that data is successfully delivered. When a sender sends a segment of data, it waits for an acknowledgment from the receiver before sending more data.

    Sequence Numbers: TCP uses sequence numbers to ensure that data segments are delivered in the correct order. Each segment is assigned a sequence number, and the receiver uses these numbers to reorder segments if necessary.

    Retransmission: If a sender does not receive an acknowledgment for a segment within a certain timeout period, it assumes that the segment was lost and retransmits it.

    Flow Control: TCP uses flow control mechanisms to prevent a sender from overwhelming a receiver with data. The receiver can advertise a window size, indicating how much data it is willing to accept, and the sender adjusts its sending rate accordingly.

    Congestion Control: TCP has congestion control mechanisms to avoid network congestion. It uses techniques such as slow start, congestion avoidance, and fast retransmit to adapt the sending rate based on network conditions.

    Checksum: TCP includes a checksum in each segment to detect errors in the data. If a segment arrives with a checksum error, it is discarded, and the sender is notified to retransmit the data.

    Connection Establishment and Termination: TCP uses a three-way handshake to establish a connection and a four-way handshake to terminate a connection, ensuring that both sides are ready to send and receive data.

These features make TCP a reliable protocol for transmitting data over networks, suitable for applications where data integrity and order are crucial, such as web browsing, email, and file transfer.