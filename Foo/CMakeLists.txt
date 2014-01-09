cmake_minimum_required(VERSION 2.8)
project(Foo)

# If library postfix will be empty,
# release variant will overwrite debug variant;
# Note: update before `add_library` command
if(NOT CMAKE_DEBUG_POSTFIX)
  set(CMAKE_DEBUG_POSTFIX d)
endif()

# Library install layout:
#     * <prefix>/lib/cmake/Foo
#     * <prefix>/lib/
#     * <prefix>/include/
set(CONFIG_INSTALL_DESTINATION lib/cmake/Foo)
set(LIB_INSTALL_DESTINATION lib)
set(INCLUDE_INSTALL_DESTINATION include)

# Create target
add_library(foo foo.cpp)
set(FOO_VERSION 1.2.3)

# Values:
#     * Debug: -DFOO_DEBUG=1
#     * Release: -DFOO_DEBUG=0
#     * other: -DFOO_DEBUG=0
#     * no config: -DFOO_DEBUG=0
# see `FooConfig.cmake.in` for default library location
target_compile_definitions(foo PUBLIC "FOO_DEBUG=$<CONFIG:Debug>")

target_include_directories(
    foo
    PUBLIC
        "$<INSTALL_INTERFACE:${INCLUDE_INSTALL_DESTINATION}>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/Source/headers>"
)

# Target config
include(CMakePackageConfigHelpers)

set(foo_config "${CMAKE_CURRENT_BINARY_DIR}/FooConfig.cmake")
set(foo_config_version "${CMAKE_CURRENT_BINARY_DIR}/FooConfigVersion.cmake")

# CONFIG_INSTALL_DESTINATION can be used
# as PACKAGE_CONFIG_INSTALL_DESTINATION in FooConfig.cmake.in
configure_package_config_file(
    "./FooConfig.cmake.in"
    "${foo_config}"
    INSTALL_DESTINATION ${CONFIG_INSTALL_DESTINATION}
    PATH_VARS CONFIG_INSTALL_DESTINATION
)

write_basic_package_version_file(
    "${foo_config_version}"
    VERSION ${FOO_VERSION}
    COMPATIBILITY SameMajorVersion
)

# Install targets and configs
install(
    FILES "${foo_config}" "${foo_config_version}"
    DESTINATION ${CONFIG_INSTALL_DESTINATION}
)
install(TARGETS foo DESTINATION ${LIB_INSTALL_DESTINATION} EXPORT FooTargets)
install(
    FILES "Source/headers/Foo.hpp" DESTINATION ${INCLUDE_INSTALL_DESTINATION}
)
install(
    EXPORT FooTargets NAMESPACE Foo:: DESTINATION ${CONFIG_INSTALL_DESTINATION}
)
