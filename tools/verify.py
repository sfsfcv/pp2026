import numpy as np
import sys

N = int(sys.argv[1])
output_file = sys.argv[2]

A = np.load(f"data/A_{N}.npy")
B = np.load(f"data/B_{N}.npy")
expected = A @ B

with open(output_file) as f:
    lines = f.readlines()

n_from_file = int(lines[0])
result = np.array([[float(x) for x in line.split()] for line in lines[1:1+n_from_file]])

is_close = np.allclose(result, expected, rtol=1e-5, atol=1e-3)
max_abs_err = np.max(np.abs(result - expected))
max_rel_err = np.max(np.abs((result - expected) / (np.abs(expected) + 1e-12)))

print(f"Файл: {output_file}")
print(f"Совпадает с NumPy: {is_close}")
print(f"Макс. абсолютная ошибка: {max_abs_err:.2e}")
print(f"Макс. относительная ошибка: {max_rel_err:.2e}")
