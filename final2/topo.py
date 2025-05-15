from mininet.topo import Topo
from mininet.link import TCLink
from mininet.node import CPULimitedHost

class BloomTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        # 添加 Hosts 并限制 CPU
        h1 = self.addHost('h1', cpu=0.1)  # h1 限制为 10% CPU
        h2 = self.addHost('h2', cpu=0.3)  # h2 限制为 30% CPU
        h3 = self.addHost('h3', cpu=0.3)  # h3 限制为 30% CPU
        h4 = self.addHost('h4')
        self.addLink(h1, s1)
        self.addLink(h2, s1, bw=1)  # 设置为 1 Mbps
        self.addLink(h3, s1)
        self.addLink(h4, s1)

topos = {
    'bloomtopo': (lambda: BloomTopo())
}
