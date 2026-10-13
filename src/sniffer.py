"""Live packet capture -> feeds a NetworkGraph. Run as Admin/root."""
from graph_model import NetworkGraph

graph = NetworkGraph()


def process(pkt):
    try:
        from scapy.layers.inet import IP, TCP, UDP
        if IP in pkt:
            dport = 0
            if TCP in pkt:
                dport = pkt[TCP].dport
            elif UDP in pkt:
                dport = pkt[UDP].dport
            graph.add_packet(pkt[IP].src, pkt[IP].dst, dport)
    except Exception:
        pass


def start_live_capture():
    """Blocking sniff loop. Call in a background thread."""
    from scapy.all import sniff
    print("Live capture started...")
    sniff(prn=process, store=False)


if __name__ == "__main__":
    print("Capturing... (run as Administrator, Ctrl+C to stop)")
    try:
        start_live_capture()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Capture failed (need Administrator/root + scapy):", e)
    print(graph.summary())
    for ip, kind, reason in graph.detect():
        print(f"ALERT [{kind}] {ip} - {reason}")
