import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/results.csv")

# --- График 1: время от N, отдельная линия на каждую стратегию/T ---
plt.figure(figsize=(8, 6))
seq = df[df["strategy"] == "sequential"].sort_values("N")
plt.plot(seq["N"], seq["time_seconds"], marker="o", label="sequential")

for T in sorted(df[df["strategy"] == "parallel_threads"]["threads"].unique()):
    sub = df[(df["strategy"] == "parallel_threads") & (df["threads"] == T)].sort_values("N")
    plt.plot(sub["N"], sub["time_seconds"], marker="o", label=f"threads={T}")

plt.xlabel("Размер матрицы N")
plt.ylabel("Время выполнения, с")
plt.title("Время выполнения от размера задачи")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("report/lab1/figures/time_vs_size.png", dpi=150, bbox_inches="tight")
plt.close()

# --- График 2: ускорение (speedup) от числа потоков, для каждого N ---
plt.figure(figsize=(8, 6))
for N in sorted(df["N"].unique()):
    sub = df[df["N"] == N]
    seq_time = sub[sub["strategy"] == "sequential"]["time_seconds"].values
    if len(seq_time) == 0:
        continue
    seq_time = seq_time[0]

    par = sub[sub["strategy"] == "parallel_threads"].sort_values("threads")
    threads = par["threads"].values
    speedup = seq_time / par["time_seconds"].values

    plt.plot(threads, speedup, marker="o", label=f"N={N}")

plt.xlabel("Число потоков T")
plt.ylabel("Ускорение (speedup = t_seq / t_par)")
plt.title("Ускорение от числа потоков")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("report/lab1/figures/speedup_vs_threads.png", dpi=150, bbox_inches="tight")
plt.close()

print("Графики сохранены: report/lab1/figures/time_vs_size.png, report/lab1/figures/speedup_vs_threads.png")
