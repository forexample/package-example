# Since CMake 3.3 'NO_CMAKE_BUILDS_PATH' was removed:
# * https://cmake.org/cmake/help/latest/release/3.3.html#deprecated-and-removed-features
cmake_minimum_required(VERSION 3.3)
project(Boo)

if(TARGET bar)
  add_library(Foo::bar ALIAS bar)
else()
  find_package(Foo CONFIG REQUIRED)
  message("Foo_DIR: ${Foo_DIR}")
endif()

# Introduce variables:
# * CMAKE_INSTALL_LIBDIR
# * CMAKE_INSTALL_BINDIR
# * CMAKE_INSTALL_INCLUDEDIR
include(GNUInstallDirs)

if(BUILD_SHARED_LIBS)
  if(IOS)
    # TODO
  elseif(ANDROID)
    # TODO
  elseif(UNIX)
    if(APPLE)
      set(CMAKE_INSTALL_RPATH "@executable_path/../${CMAKE_INSTALL_LIBDIR}")
    else()
      set(CMAKE_INSTALL_RPATH "\$ORIGIN/../${CMAKE_INSTALL_LIBDIR}")
    endif()
  endif()
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

install(TARGETS boo DESTINATION ${CMAKE_INSTALL_BINDIR})
