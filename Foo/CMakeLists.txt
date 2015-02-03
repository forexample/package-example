cmake_minimum_required(VERSION 2.8.5)
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
set(CFG_DEST lib/cmake/Foo)
set(LIB_DEST lib)
set(INCL_DEST include)

# Create targets
add_library(foo foo.cpp)
add_library(baz baz.cpp)
set(FOO_VERSION 1.2.3)

# Values:
#     * Debug: -DFOO_DEBUG=1
#     * Release: -DFOO_DEBUG=0
#     * other: -DFOO_DEBUG=0
#     * no config: -DFOO_DEBUG=0
# see `FooConfig.cmake.in` for default library location
target_compile_definitions(foo PUBLIC "FOO_DEBUG=$<CONFIG:Debug>")
target_compile_definitions(baz PUBLIC "BAZ_DEBUG=$<CONFIG:Debug>")

include_directories("Source/headers")

target_include_directories(baz PUBLIC "$<INSTALL_INTERFACE:${INCL_DEST}>")

target_link_libraries(foo PUBLIC baz)

# Target config
include(CMakePackageConfigHelpers)

set(foo_config "${CMAKE_CURRENT_BINARY_DIR}/FooConfig.cmake")
set(foo_config_version "${CMAKE_CURRENT_BINARY_DIR}/FooConfigVersion.cmake")

# CFG_DEST can be used
# as PACKAGE_CFG_DEST in FooConfig.cmake.in
configure_package_config_file(
    "./FooConfig.cmake.in"
    "${foo_config}"
    INSTALL_DESTINATION ${CFG_DEST}
    PATH_VARS CFG_DEST
)

write_basic_package_version_file(
    "${foo_config_version}"
    VERSION ${FOO_VERSION}
    COMPATIBILITY SameMajorVersion
)

# Install targets and configs
install(FILES "${foo_config}" "${foo_config_version}" DESTINATION ${CFG_DEST})
install(TARGETS foo baz DESTINATION ${LIB_DEST} EXPORT FooTargets)
install(FILES "Source/headers/Foo.hpp" DESTINATION ${INCL_DEST})
install(EXPORT FooTargets NAMESPACE Foo:: DESTINATION ${CFG_DEST})
