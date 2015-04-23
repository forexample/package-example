cmake_minimum_required(VERSION 2.8.11) # target_compile_definitions
project(Foo)

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

# Target version
include(CMakePackageConfigHelpers)

set(foo_config_version "${CMAKE_CURRENT_BINARY_DIR}/FooConfigVersion.cmake")

write_basic_package_version_file(
    "${foo_config_version}"
    VERSION ${FOO_VERSION}
    COMPATIBILITY SameMajorVersion
)

# Install targets and configs
install(FILES FooConfig.cmake "${foo_config_version}" DESTINATION ${CFG_DEST})
install(TARGETS foo baz DESTINATION ${LIB_DEST} EXPORT FooTargets)
install(FILES "Source/headers/Foo.hpp" DESTINATION ${INCL_DEST})
install(EXPORT FooTargets NAMESPACE Foo:: DESTINATION ${CFG_DEST})
