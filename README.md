# Reliable Data Transfer (RDT) 3.0 Simulation

## Overview
This Python simulation demonstrates the Reliable Data Transfer 3.0 protocol, featuring both Sender and Receiver components. It simulates packet transmission over a network, handling issues such as packet loss, corruption, and ensuring reliable data transfer using sequence numbers and checksums.

## Components

### 1. Receiver Class (`receiver.py`)
- Manages packet reception, simulating timeouts and corrupted ACKs.
- Implements methods to bind the socket, receive and process packets, and extract messages from packets.
- Simulates various network issues like packet loss and corruption based on packet numbers.

### 2. Sender Class (`sender.py`)
- Handles sending of packets to the Receiver.
- Manages timeouts, resends packets if ACKs are not received or are corrupted.
- Uses sequence numbers to ensure reliable transmission.

### 3. Utility Functions (`util.py`)
- Includes functions for checksum creation and verification, packet creation, and sequence/ACK number extraction.

## Features
- Simulates packet transmission with conditions for timeouts and corrupted ACKs.
- Dynamically adjusts sequence numbers for packet tracking.
- Verifies packet integrity using checksums.

## Usage
1. **Receiver Setup**:
   - Run `receiver.py` and input the port number when prompted.
   - The Receiver will listen for packets and simulate network behaviors based on packet numbers.
2. **Sender Setup**:
   - Run `sender.py`, input the Receiver's IP address and port number when prompted.
   - Use the `rdt_send()` method to send messages.

## Scenarios Handled
1. **Receiver**:
   - **Timeout Simulation**: Simulates a timeout for packets divisible by 6.
   - **Corrupted Packet Simulation**: Simulates a corrupted packet for packets divisible by 3 (but not by 6).
   - **Correct ACKs**: Sends correct ACKs for other packets.
2. **Sender**:
   - Resends packets on timeout or receiving a corrupted ACK.
