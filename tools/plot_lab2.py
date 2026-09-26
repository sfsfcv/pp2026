import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("report/lab2/figures", exist_ok=True)

df = pd.read_csv("data/results.csv")
seq = df[df["strategy"] == "sequential"]
omp = df[df["strategy"] == "parallel_openmp"]
sizes = sorted(omp["N"].unique())

# --- График 1: время от потоков ---
plt.figure(figsize=(8, 6))
for N in sizes:
    sub = omp[omp["N"] == N].sort_values("threads")
    plt.plot(sub["threads"], sub["time_seconds"], marker="o", label=f"N={N}")
plt.xlabel("Число потоков T")
plt.ylabel("Время выполнения, с")
plt.title("OpenMP: время выполнения от числа потоков")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("report/lab2/figures/time_vs_threads.png", dpi=150, bbox_inches="tight")
plt.close()

# --- График 2: ускорение S = t_seq / t_omp ---
plt.figure(figsize=(8, 6))
for N in sizes:
    seq_time = seq[seq["N"] == N]["time_seconds"].values
    if len(seq_time) == 0:
        continue
    seq_time = seq_time[0]
    sub = omp[omp["N"] == N].sort_values("threads")
    speedup = seq_time / sub["time_seconds"].values
    plt.plot(sub["threads"], speedup, marker="o", label=f"N={N}")
plt.xlabel("Число потоков T")
plt.ylabel("Ускорение S = t_seq / t_omp")
plt.title("OpenMP: ускорение от числа потоков")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("report/lab2/figures/speedup_vs_threads.png", dpi=150, bbox_inches="tight")
plt.close()

# --- График 3: эффективность E = S / T ---
plt.figure(figsize=(8, 6))
for N in sizes:
    seq_time = seq[seq["N"] == N]["time_seconds"].values
    if len(seq_time) == 0:
        continue
    seq_time = seq_time[0]
    sub = omp[omp["N"] == N].sort_values("threads")
    speedup = seq_time / sub["time_seconds"].values
    efficiency = speedup / sub["threads"].values
    plt.plot(sub["threads"], efficiency, marker="o", label=f"N={N}")
plt.axhline(1.0, color="gray", linestyle="--", linewidth=1)
plt.xlabel("Число потоков T")
plt.ylabel("Эффективность E = S / T")
plt.title("OpenMP: эффективность распараллеливания")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("report/lab2/figures/efficiency_vs_threads.png", dpi=150, bbox_inches="tight")
plt.close()

# --- График 4: масштабирование по размеру, T фиксирован (максимум сетки) ---
T_max = omp["threads"].max()
plt.figure(figsize=(8, 6))
seq_sorted = seq.sort_values("N")
plt.plot(seq_sorted["N"], seq_sorted["time_seconds"], marker="o", label="sequential")
omp_fixed = omp[omp["threads"] == T_max].sort_values("N")
plt.plot(omp_fixed["N"], omp_fixed["time_seconds"], marker="o", label=f"omp, T={T_max}")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Размер матрицы N (лог. шкала)")
plt.ylabel("Время выполнения, с (лог. шкала)")
plt.title(f"Масштабирование по размеру задачи (T={T_max})")
plt.legend()
plt.grid(True, alpha=0.3, which="both")
plt.savefig("report/lab2/figures/time_by_size_scaling.png", dpi=150, bbox_inches="tight")
plt.close()

print("Графики лабы 2 сохранены в report/lab2/figures/")
