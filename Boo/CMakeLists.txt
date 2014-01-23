cmake_minimum_required(VERSION 2.8)
project(Boo)

find_package(Foo CONFIG REQUIRED)

add_executable(boo boo.cpp)

# Note:
# * library Foo::baz will be linked automatically
# * macro BAZ_DEBUG will be added automatically (Foo::baz usage requirement)
target_link_libraries(boo Foo::foo)
