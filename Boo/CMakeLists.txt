cmake_minimum_required(VERSION 3.0)
project(Boo)

if(TARGET bar)
  add_library(Foo::bar ALIAS bar)
else()
  # Add NO_CMAKE_BUILDS_PATH for windows if using CMake-GUI to build packages
  # to avoid searching in temporary build directory of Foo project
  # See 5:
  #    * http://www.cmake.org/cmake/help/v3.0/command/find_package.html
  find_package(Foo CONFIG REQUIRED)
  message("Foo_DIR: ${Foo_DIR}")
endif()

add_executable(boo boo.cpp)

# Note:
# * library Foo::baz will be linked automatically
# * macro FOO_BAZ_DEBUG will be added automatically (Foo::baz usage requirement)
target_link_libraries(boo Foo::bar)

# CMAKE_<CONFIG>_POSTFIX has no effect on executable
# * http://www.cmake.org/Bug/view.php?id=7868
set_target_properties(boo PROPERTIES DEBUG_POSTFIX "d")

enable_testing()
add_test(NAME BooTest COMMAND boo)

# Introduce variables:
# * CMAKE_INSTALL_LIBDIR
# * CMAKE_INSTALL_BINDIR
# * CMAKE_INSTALL_INCLUDEDIR
include(GNUInstallDirs)

install(TARGETS boo DESTINATION ${CMAKE_INSTALL_BINDIR})
