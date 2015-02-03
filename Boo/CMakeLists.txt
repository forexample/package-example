cmake_minimum_required(VERSION 2.8.5)
project(Boo)

# Do not search temporary build directory of Foo project (Windows)
# See 5:
#    * http://www.cmake.org/cmake/help/v3.0/command/find_package.html
find_package(Foo CONFIG REQUIRED NO_CMAKE_BUILDS_PATH)

add_executable(boo boo.cpp)

# Note:
# * library Foo::baz will be linked automatically
# * macro BAZ_DEBUG will be added automatically (Foo::baz usage requirement)
target_link_libraries(boo Foo::foo)
