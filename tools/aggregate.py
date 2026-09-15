import glob
import csv

rows = []
for filepath in sorted(glob.glob("data/output_*.txt")):
    with open(filepath) as f:
        lines = f.readlines()
    N = int(lines[0])
    meta = {}
    for line in lines[1+N:]:
        parts = line.split()
        if len(parts) == 2:
            meta[parts[0]] = parts[1]
    rows.append({
        "N": N,
        "strategy": meta.get("strategy", ""),
        "threads": int(meta.get("threads", 0)),
        "time_seconds": float(meta.get("time_seconds", 0)),
        "file": filepath,
    })

with open("data/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["N", "strategy", "threads", "time_seconds", "file"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Собрано {len(rows)} результатов в data/results.csv")
