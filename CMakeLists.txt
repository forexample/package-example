cmake_minimum_required(VERSION 3.0)
project(foo-monolithic)

enable_testing()

# Monolithic version
file(GLOB subprojects LIST_DIRECTORIES true "${CMAKE_CURRENT_SOURCE_DIR}/*")
list(SORT subprojects ORDER DESCENDING)
foreach (subproject_path ${subprojects})
    if (IS_DIRECTORY "${subproject_path}")
        get_filename_component(subproject ${subproject_path} NAME)
        if (NOT subproject MATCHES ^[.]|build|wiki)
            add_subdirectory("${subproject}")
        endif()
    endif ()
endforeach ()
