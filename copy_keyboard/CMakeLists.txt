
cmake_minimum_required(VERSION 3.10)
project(copy_keyboard)

set(CMAKE_CXX_STANDARD 11)

include_directories(./cpp)

add_executable(copy_keyboard ./cpp/main.cpp)
