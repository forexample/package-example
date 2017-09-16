# This file creates project 'Foo' with two library targets 'bar' and 'baz'.
# Target 'bar' depends on 'baz'. After installation this project can be found
# by 'find_package(... CONFIG)' command:
#
#    find_package(Foo CONFIG REQUIRED)
#    target_link_libraries(... Foo::bar)
#
# Note that requirements propagated automatically, for example:
#   * Foo::baz linked automatically
#   * <prefix>/include added to header search path
#   * FOO_BAZ_DEBUG=1/FOO_BAR_DEBUG=1 added on Debug
#   * FOO_BAZ_DEBUG=0/FOO_BAR_DEBUG=0 added on other configurations

####
# Set minimum version of CMake. Since command 'project' use
# VERSION sub-option we need 3.0.
cmake_minimum_required(VERSION 3.0)

####
# Set variables:
#   * PROJECT_NAME
#   * PROJECT_VERSION
project(Foo VERSION 1.2.3)

####
# Create targets
add_library(bar "Source/foo/Bar.cpp" "Source/foo/Bar.hpp")
add_library(baz "Source/foo/Baz.cpp" "Source/foo/Baz.hpp")

####
# Properties of targets

# Add definitions for targets
# Values:
#   * Debug: -DFOO_BAR_DEBUG=1
#   * Release: -DFOO_BAR_DEBUG=0
#   * other: -DFOO_BAR_DEBUG=0
target_compile_definitions(bar PUBLIC "FOO_BAR_DEBUG=$<CONFIG:Debug>")
target_compile_definitions(baz PUBLIC "FOO_BAZ_DEBUG=$<CONFIG:Debug>")

# Generate:
#   * ${CMAKE_CURRENT_BINARY_DIR}/bar_export.h with BAR_EXPORT
#   * ${CMAKE_CURRENT_BINARY_DIR}/baz_export.h with BAZ_EXPORT
include(GenerateExportHeader)
generate_export_header(bar)
generate_export_header(baz)

# Global includes. Used by all targets
# Note:
#   * header location in project: Foo/Source/foo/Bar.hpp
#   * header can be included by C++ code `#include <foo/Bar.hpp>`
#   * header location in project: ${CMAKE_CURRENT_BINARY_DIR}/bar_export.hpp
#   * header can be included by: `#include <bar_export.hpp>`
target_include_directories(
    baz PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/Source>"
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>"
)

# Link required library
target_link_libraries(bar PUBLIC baz)

####
# Installation (https://github.com/forexample/package-example)

# Layout. This works for all platforms:
#   * <prefix>/lib/cmake/<PROJECT-NAME>
#   * <prefix>/lib/
#   * <prefix>/include/
set(config_install_dir "lib/cmake/${PROJECT_NAME}")
set(include_install_dir "include")

set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")

# Configuration
set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")

# Include module with fuction 'write_basic_package_version_file'
include(CMakePackageConfigHelpers)

# Configure '<PROJECT-NAME>ConfigVersion.cmake'
# Use:
#   * PROJECT_VERSION
write_basic_package_version_file(
    "${version_config}" COMPATIBILITY SameMajorVersion
)

# Configure '<PROJECT-NAME>Config.cmake'
# Use variables:
#   * TARGETS_EXPORT_NAME
#   * PROJECT_NAME
configure_package_config_file(
    "cmake/Config.cmake.in"
    "${project_config}"
    INSTALL_DESTINATION "${config_install_dir}"
)

# Targets:
#   * <prefix>/lib/libbar.a
#   * <prefix>/lib/libbaz.a
#   * header location after install: <prefix>/include/foo/Bar.hpp
#   * headers can be included by C++ code `#include <foo/Bar.hpp>`
install(
    TARGETS bar baz
    EXPORT "${TARGETS_EXPORT_NAME}"
    LIBRARY DESTINATION "lib"
    ARCHIVE DESTINATION "lib"
    RUNTIME DESTINATION "bin"
    INCLUDES DESTINATION "${include_install_dir}"
)

# Headers:
#   * Source/foo/Bar.hpp -> <prefix>/include/foo/Bar.hpp
#   * Source/foo/Baz.hpp -> <prefix>/include/foo/Baz.hpp
install(
    DIRECTORY "Source/foo"
    DESTINATION "${include_install_dir}"
    FILES_MATCHING PATTERN "*.hpp"
)

# Export headers:
#   * ${CMAKE_CURRENT_BINARY_DIR}/bar_export.h -> <prefix>/include/bar_export.h
#   * ${CMAKE_CURRENT_BINARY_DIR}/baz_export.h -> <prefix>/include/baz_export.h
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/bar_export.h"
        "${CMAKE_CURRENT_BINARY_DIR}/baz_export.h"
    DESTINATION "${include_install_dir}"
)

# Config
#   * <prefix>/lib/cmake/Foo/FooConfig.cmake
#   * <prefix>/lib/cmake/Foo/FooConfigVersion.cmake
install(
    FILES "${project_config}" "${version_config}"
    DESTINATION "${config_install_dir}"
)

# Config
#   * <prefix>/lib/cmake/Foo/FooTargets.cmake
install(
    EXPORT "${TARGETS_EXPORT_NAME}"
    NAMESPACE "${namespace}"
    DESTINATION "${config_install_dir}"
)
