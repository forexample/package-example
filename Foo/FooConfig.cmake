# https://github.com/forexample/package-example

# See manual:
#     * http://www.cmake.org/cmake/help/v2.8.12/cmake.html#module:CMakePackageConfigHelpers

include("${CMAKE_CURRENT_LIST_DIR}/FooTargets.cmake")

# Use release variant library in default case;
# See CMakeLists.txt's `target_compile_definitions` command:
#    * Debug: -DFOO_DEBUG=1 use IMPORTED_LOCATION_DEBUG: libfood.a
#    * Release: -DFOO_DEBUG=0 use IMPORTED_LOCATION_RELEASE: libfoo.a
#    * other: -DFOO_DEBUG=0 use IMPORTED_LOCATION (release value): libfoo.a
#    * no config: -DFOO_DEBUG=0 use IMPORTED_LOCATION (release value): libfoo.a
function(_apply_release_imported_config_as_default tgt)
  get_target_property(location ${tgt} IMPORTED_LOCATION_RELEASE)
  get_target_property(link ${tgt} IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE)

  if(NOT location)
    message(FATAL_ERROR "Release target `${tgt}` not installed")
  endif()

  set_target_properties(
      ${tgt}
      PROPERTIES
      IMPORTED_LOCATION "${location}"
  )
  if(link)
    set_target_properties(
        ${tgt}
        PROPERTIES
        IMPORTED_LINK_INTERFACE_LIBRARIES "${link}"
    )
  endif()
endfunction()

_apply_release_imported_config_as_default(Foo::foo)
_apply_release_imported_config_as_default(Foo::baz)
