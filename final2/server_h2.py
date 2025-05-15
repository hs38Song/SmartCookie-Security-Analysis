#!/usr/bin/env python3
import socket
import time
import threading
import psutil
import logging
from datetime import datetime
from scapy.all import send, IP, TCP, Raw

VALID_CLIENT_IP = "10.0.0.1"
MY_IP = "10.0.0.2"
LISTEN_PORT = 80

# ——— set up logging
LOG_FILE = "/tmp/server_h2.log"
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s server: %(message)s")
log = logging.getLogger("server_h2")

def monitor_cpu():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)  # 每秒更新一次
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.info(f"CPU Usage: {cpu_usage}%")

# 启动 CPU 监控线程
threading.Thread(target=monitor_cpu, daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((MY_IP, LISTEN_PORT))
server.listen(5)

log.info(f"Listening on {MY_IP}:{LISTEN_PORT}")

while True:
    try:
        client, addr = server.accept()
        src_ip = addr[0]
        data = client.recv(1024)

        if src_ip == VALID_CLIENT_IP:
            log.info(f"Accepted connection from {src_ip}, processing...")
            time.sleep(0.1)  # 合法请求延迟
            response = IP(src=MY_IP, dst=src_ip) / TCP(sport=LISTEN_PORT, dport=12345, flags="A") / Raw(load=data)
            send(response, verbose=False)
            log.info(f"Responded to {src_ip}")
        else:
            log.info(f"Detected spoofed packet from {src_ip}, simulating processing delay...")
            duration = 0.005
            end = time.time() + duration
            # Busy‐wait loop
            while time.time() < end:
                _ = 0
                for i in range(100):
                    _ += i*i  # trivial CPU work

        client.close()

    except Exception as e:
        log.error(f"Error: {e}")

