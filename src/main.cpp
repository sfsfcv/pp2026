#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>
#include <string>

using Matrix = std::vector<std::vector<double>>;

Matrix readMatrix(std::ifstream& in, int N) {
    Matrix M(N, std::vector<double>(N));
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            in >> M[i][j];
    return M;
}

void multiplyRange(const Matrix& A, const Matrix& B, Matrix& C, int N, int rowStart, int rowEnd) {
    for (int i = rowStart; i < rowEnd; ++i)
        for (int j = 0; j < N; ++j)
            for (int k = 0; k < N; ++k)
                C[i][j] += A[i][k] * B[k][j];
}

void multiplySequential(const Matrix& A, const Matrix& B, Matrix& C, int N) {
    multiplyRange(A, B, C, N, 0, N);
}

void multiplyParallel(const Matrix& A, const Matrix& B, Matrix& C, int N, int T) {
    std::vector<std::thread> workers;
    int rowsPerThread = N / T;
    for (int t = 0; t < T; ++t) {
        int rowStart = t * rowsPerThread;
        int rowEnd = (t == T - 1) ? N : rowStart + rowsPerThread;
        workers.emplace_back(multiplyRange, std::cref(A), std::cref(B), std::ref(C), N, rowStart, rowEnd);
    }
    for (auto& w : workers) w.join();
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Использование: ./matmul <input_file> [threads]\n";
        std::cerr << "  threads=0 или не указан -> последовательная версия\n";
        std::cerr << "  threads=N -> параллельная версия на N потоках\n";
        return 1;
    }
    std::ifstream in(argv[1]);
    if (!in) {
        std::cerr << "Не могу открыть файл: " << argv[1] << "\n";
        return 1;
    }

    int T = (argc >= 3) ? std::stoi(argv[2]) : 0;

    int N;
    in >> N;
    Matrix A = readMatrix(in, N);
    Matrix B = readMatrix(in, N);
    Matrix C(N, std::vector<double>(N, 0.0));

    std::string strategy = (T > 0) ? "parallel_threads" : "sequential";

    auto start = std::chrono::high_resolution_clock::now();
    if (T > 0) {
        multiplyParallel(A, B, C, N, T);
    } else {
        multiplySequential(A, B, C, N);
    }
    auto end = std::chrono::high_resolution_clock::now();
    double seconds = std::chrono::duration<double>(end - start).count();

    std::string suffix = (T > 0) ? ("_threads" + std::to_string(T)) : "_sequential";
    std::string outputPath = "data/output_" + std::to_string(N) + suffix + ".txt";
    std::ofstream out(outputPath);
    out << N << "\n";
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) out << C[i][j] << " ";
        out << "\n";
    }
    out << "strategy " << strategy << "\n";
    out << "threads " << T << "\n";
    out << "time_seconds " << seconds << "\n";

    std::cout << "N=" << N << " strategy=" << strategy << " threads=" << T << " time=" << seconds << "s\n";
    return 0;
}
