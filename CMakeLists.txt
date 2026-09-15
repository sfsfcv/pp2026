cmake_minimum_required(VERSION 3.16)
project(matmul)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(matmul src/main.cpp)

find_package(Threads REQUIRED)
target_link_libraries(matmul PRIVATE Threads::Threads)
