# Cyber Shield — Explain Like I'm 5 + Demo Steps 👶

## 1. What is this project? (a story)
Imagine a **village**. Every **house** is a computer (we call it an IP, like `192.168.1.5`).
Every **road** between houses is a connection (we call it an edge).

Normal days: houses visit each other a little. Thieves make **strange shapes**:
- **Port scan thief** 🚨: ONE house knocks on 10+ doors = star shape ⭐
- **DDoS gang** 🚨: 10+ houses attack ONE house together = funnel shape 🔻

Cyber Shield **draws the village map live** and shouts when it sees a thief-shape.

## 2. What does each file do? (only 5 files!)
| File | Job in one line |
|---|---|
| `shield.py` | EASY mode: watched village + thieves, prints ALERTs. Just run it. |
| `src/graph_model.py` | The brain: draws map (NetworkX), decides thief or not |
| `src/sniffer.py` | The eyes: reads REAL Wi-Fi packets (Scapy) |
| `src/app.py` | The mouth: shows website dashboard (Flask) |
| `dashboard/index.html` | The face: what sir sees in browser |

## 3. Install (do once, copy-paste these)
```
python -m pip install -r requirements.txt
```
That's it. (Needs Python + internet.)

## 4. Run EASY mode (2 minutes, no setup)
```
python shield.py
```
You will see:
```
[ok] packet 1: 192.168.1.8 -> 192.168.1.3     <- normal houses visiting
[!] hacker 192.168.1.99 starts scanning...    <- thief enters!
>>> ALERT [PORT_SCAN] 192.168.1.99            <- CAUGHT! 🎉
```
Stop with **Ctrl+C**.

## 5. Run REAL mode (for full marks)
Terminal as **Administrator**:
```
python src/app.py
```
Open `http://localhost:7860` → YOUR real Wi-Fi traffic becomes dots and lines.
(This needs Administrator because Windows only lets the boss read packets.)

## 6. Demo to sir (exact words, 4 minutes)
1. **Say:** "Sir, this is Cyber Shield. Houses are computers, roads are connections."
2. **Run** `python shield.py`. **Say:** "Green lines are normal traffic."
3. **Wait for ALERT.** Point at it. **Say:** "One house knocked 12 doors — port scan thief, caught."
4. **Wait more.** Second alert. **Say:** "Eleven houses hit one house — DDoS gang, caught."
5. **Open** the hosted website link. **Say:** "Same project, deployed online with Docker."
6. **Close:** "Detection is pure graph shapes — star means scan, funnel means DDoS."

## 7. If sir asks (answers in simple words)
- **What is a graph?** "Dots joined by lines. Dots = computers, lines = connections."
- **How do you catch a port scan?** "If one dot touches 10 or more doors, it's a thief."
- **How do you catch DDoS?** "If 10 or more dots attack one dot, it's a gang."
- **What tools?** "Scapy reads packets, NetworkX draws the map, Flask shows the website."
- **Is it real-time?** "Yes sir — it checks the map every second / every 3 seconds on the site."
