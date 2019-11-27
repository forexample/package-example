cmake_minimum_required(VERSION 3.0)
project(foo-monolithic)

enable_testing()

# Monolithic version
add_subdirectory(Boo)
add_subdirectory(Foo)
