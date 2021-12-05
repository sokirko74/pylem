macro (declare_cmake_min_version)
    cmake_minimum_required(VERSION 3.16)
endmacro(declare_cmake_min_version)
declare_cmake_min_version()

project(pylem)

include_directories("${CMAKE_CURRENT_SOURCE_DIR}")
set(BUILD_DICTS 1)
set(DICTS_FOLDER  ${PROJECT_SOURCE_DIR}/Dicts )

add_subdirectory (morph_dict)

add_subdirectory(pybind11)

pybind11_add_module(pylem src/main.cpp)

target_compile_features(pylem PUBLIC cxx_std_17)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(pylem
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

target_link_libraries(pylem PRIVATE
        ${PYTHON_LIBRARIES} LemmatizerBaseLib
)
