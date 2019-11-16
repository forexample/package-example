cmake_minimum_required(VERSION 3.0)
project(foo-monolithic)

set(THIRD_PARTY_TOP_DIR ${CMAKE_CURRENT_LIST_DIR})

enable_testing()

# Monolithic version
if(NOT TARGET bar)
  add_subdirectory(Foo)
endif()

if(NOT TARGET boo)
  add_subdirectory(Boo)
endif()
