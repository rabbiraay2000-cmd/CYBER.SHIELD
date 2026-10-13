# Cyber Shield — Live Network Threat Detection (Graph Data Structure)

## Idea (1 line for viva)
IPs are **nodes**, packet flows are **edges**; attacks appear as abnormal graph shapes.

| Attack | Graph shape |
|---|---|
| Port scan | 1 node → many ports/hosts (star, high out-degree) |
| DDoS | many nodes → 1 victim (funnel, high in-degree) |

## Run (live capture)
```
python -m pip install -r requirements.txt
python src/sniffer.py        # terminal as Administrator, Ctrl+C to stop + print alerts
python src/app.py            # dashboard at http://localhost:5000
```

## Files
- `src/graph_model.py` — NetworkX directed graph + detection rules
- `src/sniffer.py` — live packet capture feeding the graph
- `src/app.py` + `dashboard/index.html` — dashboard, auto-refresh alerts every 3s
