cmake_minimum_required(VERSION 2.8)
project(Boo)

find_package(Foo REQUIRED)

add_executable(boo boo.cpp)
target_link_libraries(boo Foo::foo)
