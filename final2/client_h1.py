#!/usr/bin/env python3
import time, socket, logging

# ——— set up logging
LOG_FILE = "/tmp/client_h1.log"
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s RTT: %(message)s")
log = logging.getLogger("client_h1")

while True:
    try:
        s = socket.socket()
        start = time.time()
        s.connect(("10.0.0.2", 80))
        s.sendall(b"ping")
        _ = s.recv(1024)
        end = time.time()
        rtt = end - start
        log.info(f"{rtt:.4f}s")
        s.close()
    except Exception as e:
        log.warning("Connection failed: %s", e)
    time.sleep(1)
