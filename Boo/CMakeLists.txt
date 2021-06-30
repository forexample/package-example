get_filename_component(EXEC_NAME "${CMAKE_CURRENT_SOURCE_DIR}" NAME)
string(REPLACE " " "_" EXEC_NAME ${EXEC_NAME})
set(TEST_NAME "${EXEC_NAME}Test")

# Since CMake 3.3 'NO_CMAKE_BUILDS_PATH' was removed:
# * https://cmake.org/cmake/help/latest/release/3.3.html#deprecated-and-removed-features
cmake_minimum_required(VERSION 3.3)
project("${EXEC_NAME}")

# Introduce variables:
# * CMAKE_INSTALL_LIBDIR
# * CMAKE_INSTALL_BINDIR
# * CMAKE_INSTALL_INCLUDEDIR
include(GNUInstallDirs)

set(test_path "")

if(TARGET bar)
  add_library(Foo::bar ALIAS bar)
  list(APPEND test_path "$<TARGET_FILE_DIR:Foo::bar>")
else()
  find_package(Foo CONFIG REQUIRED)
  message("Foo_DIR: ${Foo_DIR}")

  # TODO: Make it robust
  list(APPEND test_path "${Foo_DIR}/../../../${CMAKE_INSTALL_BINDIR}")
endif()

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

add_executable("${EXEC_NAME}" boo.cpp)

# Note:
# * library Foo::baz will be linked automatically
# * macro FOO_BAZ_DEBUG will be added automatically (Foo::baz usage requirement)
target_link_libraries("${EXEC_NAME}" Foo::bar)

# CMAKE_<CONFIG>_POSTFIX has no effect on executable
# * http://www.cmake.org/Bug/view.php?id=7868
set_target_properties("${EXEC_NAME}" PROPERTIES DEBUG_POSTFIX "d")

enable_testing()
add_test(NAME "${TEST_NAME}" COMMAND "${EXEC_NAME}")

install(TARGETS "${EXEC_NAME}" DESTINATION "${CMAKE_INSTALL_BINDIR}")

if(WIN32 OR CYGWIN)
  # Add location of library to PATH (for DLL).
  set(new_path "$ENV{PATH};${test_path}")

  if(WIN32)
    string(REPLACE ";" "\;" new_path "${new_path}")
  elseif(CYGWIN)
    string(REPLACE ";" ":" new_path "${new_path}")
  else()
    message(FATAL_ERROR "Unreachable")
  endif()

  set_tests_properties("${TEST_NAME}" PROPERTIES ENVIRONMENT "PATH=${new_path}")
endif()
