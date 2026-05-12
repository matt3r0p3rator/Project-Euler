cmake_minimum_required(VERSION 3.20)

project(project_euler_solvers LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

file(GLOB LEGACY_PROBLEM_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/problems/*.cpp")
file(GLOB FOLDER_PROBLEM_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/problems/*/main.cpp")
set(PROBLEM_SOURCES ${LEGACY_PROBLEM_SOURCES} ${FOLDER_PROBLEM_SOURCES})

if(NOT PROBLEM_SOURCES)
    message(FATAL_ERROR "No problem source files were found in cpp/problems")
endif()

foreach(problem_source IN LISTS PROBLEM_SOURCES)
    get_filename_component(source_name "${problem_source}" NAME_WE)

    if(source_name STREQUAL "main")
        get_filename_component(problem_directory "${problem_source}" DIRECTORY)
        get_filename_component(problem_name "${problem_directory}" NAME)
    else()
        set(problem_name "${source_name}")
    endif()

    add_executable("${problem_name}" "${problem_source}")
    target_include_directories("${problem_name}" PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include")
    if(MSVC)
        target_compile_options("${problem_name}" PRIVATE /W4 /WX-)
    else()
        target_compile_options("${problem_name}" PRIVATE -Wall -Wextra -Wpedantic)
    endif()
endforeach()
