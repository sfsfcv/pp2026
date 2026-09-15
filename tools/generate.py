import numpy as np
import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 100
outdir = sys.argv[2] if len(sys.argv) > 2 else "data"

A = np.random.rand(N, N)
B = np.random.rand(N, N)

with open(f"{outdir}/input_{N}.txt", "w") as f:
    f.write(f"{N}\n")
    for row in A:
        f.write(" ".join(map(str, row)) + "\n")
    for row in B:
        f.write(" ".join(map(str, row)) + "\n")

np.save(f"{outdir}/A_{N}.npy", A)
np.save(f"{outdir}/B_{N}.npy", B)
print(f"Сгенерировано: {outdir}/input_{N}.txt ({N}x{N})")
