cmake_minimum_required(VERSION 3.0)
project(foo-monolithic)

enable_testing()

# Monolithic version
add_subdirectory(Foo)
add_subdirectory(Boo)
