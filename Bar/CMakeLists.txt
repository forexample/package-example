cmake_minimum_required(VERSION 3.0)
project(Bar)

add_executable(bar bar.cpp)

find_package(Boo REQUIRED CONFIG NO_CMAKE_BUILDS_PATH)

target_link_libraries(bar Boo::boo)
