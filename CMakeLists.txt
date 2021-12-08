macro (declare_cmake_min_version)
    cmake_minimum_required(VERSION 3.16)
endmacro(declare_cmake_min_version)
declare_cmake_min_version()

project(pylem_package)

add_subdirectory(pylem)

