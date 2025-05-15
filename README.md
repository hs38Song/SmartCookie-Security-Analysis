# SmartCookie Experiment: Evaluating Split-Proxy Security with Bloom Filter Defense

This repository contains scripts and topology definitions for evaluating the SmartCookie split-proxy SYN-flood defense, focusing on Bloom filter vulnerabilities and side-channel attacks in a controlled Mininet environment.

## Experiment Overview

We set up a custom Mininet topology to simulate a network with a Bloom filter-based switch (defender), legitimate client, server, attacker, and an accurate attacker for false positive evaluation. The experiment evaluates how SYN-flood and targeted false positive traffic can impact RTT and resource usage.

### Network Topology

- **s1:** Software switch running Bloom filter defense logic (`bloom_defender.py`)
- **h1:** Legitimate client measuring RTT to server (`client_h1.py`)
- **h2:** Server responding to connections (`server_h2.py`)
- **h3:** Attacker sending high-volume spoofed SYN packets (`attacker_h3.py`)
- **h4:** Accurate attacker replaying observed false positive traffic (`accurate_attacker_h4.py`)

All hosts are interconnected via s1. Switch and hosts are started in separate terminals for real-time monitoring.

## Running the Experiment

### 1. Start Mininet Topology

```bash
sudo mn --custom topo.py --topo bloomtopo --controller=none --link=tc
```
### 2. Open Xterm Windows (one per node)
From the Mininet CLI:

bash
Copy
Edit
xterm s1
xterm h2
xterm h1
xterm h3
xterm h4
### 3. Enable Switch Flooding
From the Mininet CLI:

bash
Copy
Edit
sh ovs-ofctl add-flow s1 priority=1,actions=flood
### 4. Start Server and Defender
In the h2 xterm:

bash
Copy
Edit
python3 server_h2.py
In the s1 xterm:

bash
Copy
Edit
python3 bloom_defender.py
### 5. Start Client and Attackers
In the h1 xterm (client):

bash
Copy
Edit
python3 client_h1.py
In the h3 xterm (random attacker):

bash
Copy
Edit
python3 attacker_h3.py
In the h4 xterm (accurate attacker):

bash
Copy
Edit
python3 accurate_attacker_h4.py
Log Collection
To automatically fetch logs from all hosts and the switch, run on the host VM:

bash
Copy
Edit
~/fetch_logs.sh
Logs will be collected into ~/experiment_logs/:

client_h1.log

server_h2.log

attacker_h3.log

bloom_defender.log

accurate_attacker_h4.log

Output Analysis
client_h1.log: RTT measurements, timestamps, and detection of RTT spikes.

attacker_h3.log: Source IP/port for every spoofed SYN, correlated with RTT spikes to detect false positives.

bloom_defender.log: Bloom filter insertions, drops, and false positive events.

accurate_attacker_h4.log: Targeted SYN flood with false positive tuple(s).
