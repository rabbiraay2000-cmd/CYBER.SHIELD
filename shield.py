"""Cyber Shield EASY - one file, no install, just run:  python shield.py

What you see:
  [ok]    normal traffic (small dots joining the graph)
  [ALERT] attack found (port scan or DDoS) with reason

Graph idea: IP = dot, connection = line.
  Port scan = 1 dot touching 10+ ports (star shape)
  DDoS      = 10+ dots hitting 1 dot (funnel shape)
"""
import random
import time

edges = {}        # (src, dst) -> packet count
ports = {}        # src -> set of ports touched


def add(src, dst, port):
    edges[(src, dst)] = edges.get((src, dst), 0) + 1
    ports.setdefault(src, set()).add(port)


def check():
    """Return list of (ip, type, reason) using graph degrees."""
    in_d, out_d = {}, {}
    for (s, d) in edges:
        out_d[s] = out_d.get(s, 0) + 1
        in_d[d] = in_d.get(d, 0) + 1
    found = []
    for ip in set(list(in_d) + list(out_d)):
        if len(ports.get(ip, ())) >= 10 and out_d.get(ip, 0) >= 3:
            found.append((ip, "PORT_SCAN",
                          f"touched {len(ports[ip])} ports"))
        if in_d.get(ip, 0) >= 10:
            found.append((ip, "DDOS_VICTIM",
                          f"{in_d[ip]} attackers hitting it"))
    return found


def main():
    hosts = [f"192.168.1.{i}" for i in range(2, 12)]
    print("Cyber Shield watching... (Ctrl+C to stop)\n")
    n = 0
    try:
        while True:
            n += 1
            # 1. normal traffic every second
            a, b = random.choice(hosts), random.choice(hosts)
            add(a, b, random.choice([80, 443, 53]))
            print(f"[ok] packet {n}: {a} -> {b}")
            # 2. every 15 packets: a hacker starts a port scan
            if n % 15 == 0:
                print("\n[!] hacker 192.168.1.99 starts scanning...\n")
                for p in range(1, 13):
                    add("192.168.1.99", f"192.168.1.{p % 4 + 1}", p)
            # 3. every 25 packets: DDoS on one victim
            if n % 25 == 0:
                print("\n[!] botnet attacking 192.168.1.50...\n")
                for i in range(1, 12):
                    add(f"10.0.0.{i}", "192.168.1.50", 80)
            # 4. check graph + shout alerts
            for ip, kind, reason in check():
                print(f">>> ALERT [{kind}] {ip} - {reason}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped. Dots:", len(set(
            [s for s, d in edges] + [d for s, d in edges])),
            "| Lines:", len(edges))


if __name__ == "__main__":
    main()
