declare_cmake_min_version()

project(pylem_binary)

include_directories("${CMAKE_CURRENT_SOURCE_DIR}")

IF (NOT DEFINED MSVC)
    set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC" )
    set( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -fPIC" )
endif()

set(BUILD_DICTS 1)
message("==== CMAKE_LIBRARY_OUTPUT_DIRECTORY = ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
set(DICTS_FOLDER  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/Dicts )
add_subdirectory (morph_dict)


add_subdirectory(pybind11)

pybind11_add_module(${PROJECT_NAME} binding/main.cpp)

target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_17)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(${PROJECT_NAME}
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

target_link_libraries(${PROJECT_NAME} PRIVATE
        ${PYTHON_LIBRARIES} LemmatizerBaseLib
)
