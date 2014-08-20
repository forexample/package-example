cmake_minimum_required(VERSION 2.8)
project(Boo)

# Do not search temporary build directory of Foo project (Windows)
# See 5:
#    * http://www.cmake.org/cmake/help/v3.0/command/find_package.html
find_package(Foo CONFIG REQUIRED NO_CMAKE_BUILDS_PATH)

add_library(boo boo.cpp)

# Note:
# * library Foo::baz will be linked automatically
# * macro BAZ_DEBUG will be added automatically (Foo::baz usage requirement)
target_link_libraries(boo PUBLIC Foo::foo)
target_include_directories(
    boo
    PUBLIC
    "$<INSTALL_INTERFACE:include>"
)

set(boo_config "${CMAKE_CURRENT_BINARY_DIR}/BooConfig.cmake")
set(CFG_DEST lib/cmake/Boo)

include(CMakePackageConfigHelpers)

configure_package_config_file(
    "./BooConfig.cmake.in"
    "${boo_config}"
    INSTALL_DESTINATION ${CFG_DEST}
    PATH_VARS CFG_DEST
)

install(TARGETS boo DESTINATION lib EXPORT BooTargets)
install(EXPORT BooTargets NAMESPACE Boo:: DESTINATION ${CFG_DEST})
install(FILES "${boo_config}" DESTINATION ${CFG_DEST})
install(FILES "boo.hpp" DESTINATION include)
