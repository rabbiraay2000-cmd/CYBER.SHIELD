"""Cyber Shield - graph-based network model.

Graph idea (for viva):
  Node  = an IP address seen on the network
  Edge  = packets sent from one IP to another (weight = packet count)

Threats pop out as graph shapes:
  Port scan  = one node with edges to MANY ports/hosts (star shape, high out-degree)
  DDoS       = MANY nodes with edges to ONE victim (funnel shape, high in-degree)
  Normal     = small balanced degrees
"""
import networkx as nx
from collections import defaultdict


class NetworkGraph:
    def __init__(self):
        self.g = nx.DiGraph()          # directed: src -> dst
        self.ports = defaultdict(set)  # src_ip -> set of dst ports touched

    def add_packet(self, src, dst, dport):
        if self.g.has_edge(src, dst):
            self.g[src][dst]["weight"] += 1
        else:
            self.g.add_edge(src, dst, weight=1)
        self.ports[src].add(dport)

    def degrees(self):
        return {n: (self.g.in_degree(n), self.g.out_degree(n))
                for n in self.g.nodes}

    def detect(self, scan_ports=10, ddos_flows=10):
        """Return list of (ip, threat_type, reason). Simple threshold rules."""
        threats = []
        for node in self.g.nodes:
            in_d = self.g.in_degree(node)
            out_d = self.g.out_degree(node)
            touched = len(self.ports.get(node, ()))
            if touched >= scan_ports and out_d >= 3:
                threats.append((node, "PORT_SCAN",
                                f"touched {touched} ports across {out_d} hosts"))
            if in_d >= ddos_flows:
                threats.append((node, "POSSIBLE_DDOS_VICTIM",
                                f"{in_d} incoming flows"))
        return threats

    def summary(self):
        return {"nodes": self.g.number_of_nodes(),
                "edges": self.g.number_of_edges(),
                "threats": self.detect()}
