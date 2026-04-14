# Simple QoS Priority Controller using SDN

## Problem Statement
To implement an SDN-based QoS controller using Mininet and POX that prioritizes network traffic.

## Objective
- Demonstrate controller-switch interaction
- Implement flow rules using OpenFlow
- Analyze network performance

## Tools Used
- Mininet
- POX Controller
- Ubuntu

## Topology
- 1 Switch (s1)
- 3 Hosts (h1, h2, h3)

## Implementation
- Traffic identified using MAC address
- h1 → High Priority (priority = 100)
- h2, h3 → Low Priority (priority = 10)
- Flow rules installed using OpenFlow
- TCP traffic → High Priority
- ICMP traffic → Low Priority

## Steps to Run

### Start Controller
cd ~/pox  
python3 pox.py log.level --DEBUG openflow.of_01 qos_controller  

### Start Mininet
sudo mn --topo single,3 --controller remote  

### Test Connectivity
pingall  

### Test Scenarios

#### Scenario 1: Priority-Based Traffic
h1 ping h3  
h2 ping h3  

#### Scenario 2: Throughput Comparison
h3 iperf -s &  
h1 iperf -c h3  
h2 iperf -c h3  

## Expected Output
- Controller logs show HIGH and LOW priority traffic
- Flow table contains priority values
- h1 performs better than h2

## Results
- QoS successfully implemented
- Traffic prioritization achieved
- Performance difference observed

## Conclusion
This project demonstrates QoS using SDN by assigning priorities and installing flow rules.
