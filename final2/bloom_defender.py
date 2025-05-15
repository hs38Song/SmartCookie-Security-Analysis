#!/usr/bin/env python3
import logging
from scapy.all import sniff, sendp, IP, TCP, Ether, get_if_list
from bitarray import bitarray
import mmh3, math, random, re, os

# ——— set up logging to file
LOG_FILE = "/tmp/bloom_defender.log"
logging.basicConfig(filename=LOG_FILE,
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("bloom_defender")
log.info("Starting Bloom defender")

def detect_interfaces():
    all_ifaces = get_if_list()
    sniff_ifaces = []
    send_iface = None

    for iface in all_ifaces:
        if re.match(r's1-eth[0-9]+', iface):
            # choose port 2 as the server-facing port, others to sniff
            if iface.endswith("2"):
                send_iface = iface
            else:
                sniff_ifaces.append(iface)
    if not send_iface:
        send_iface = "s1-eth2"
    return sniff_ifaces, send_iface

class BloomFilter:
    def __init__(self, n, p=0.076):
        self.m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2))
        self.k = math.ceil((self.m / n) * math.log(2))
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)
        self._preload_noise(p)

    def _preload_noise(self, p):
        f = p ** (1 / self.k)
        bits_to_set = int(f * self.m)
        ones = random.sample(range(self.m), bits_to_set)
        for i in ones:
            self.bit_array[i] = 1
        log.info("Preloaded %d noise bits into bloom", bits_to_set)

    def add(self, item):
        for i in range(self.k):
            idx = mmh3.hash(item, i) % self.m
            self.bit_array[idx] = 1

    def __contains__(self, item):
        for i in range(self.k):
            idx = mmh3.hash(item, i) % self.m
            if not self.bit_array[idx]:
                return False
        return True

# initialize
bloom = BloomFilter(100)
bloom.add("10.0.0.1")
bloom.add("10.0.0.2")

sniff_ifaces, send_iface = detect_interfaces()
log.info("Sniffing on %s, sending on %s", sniff_ifaces, send_iface)

def handle(pkt):
    if IP in pkt and TCP in pkt:
        src_ip = pkt[IP].src
        if src_ip in bloom:
            log.debug("[ALLOW ] %s → forward", src_ip)
            sendp(pkt, iface=send_iface, verbose=False)
        else:
            log.debug("[DROP  ] %s → dropped", src_ip)

sniff(iface=sniff_ifaces, prn=handle, store=0)
