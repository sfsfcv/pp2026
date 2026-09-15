#!/bin/bash
set -e

SIZES=(100 250 500 1000 1500)
THREAD_COUNTS=(1 2 4 8)

for N in "${SIZES[@]}"; do
    if [ ! -f "data/input_${N}.txt" ]; then
        echo "Генерирую input_${N}.txt..."
        python3 tools/generate.py "$N"
    fi

    echo "=== N=$N, sequential ==="
    ./build/matmul "data/input_${N}.txt"

    for T in "${THREAD_COUNTS[@]}"; do
        echo "=== N=$N, threads=$T ==="
        ./build/matmul "data/input_${N}.txt" "$T"
    done
done

python3 tools/aggregate.py
