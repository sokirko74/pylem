declare_cmake_min_version()

project(pylem_binary)

include_directories("${CMAKE_CURRENT_SOURCE_DIR}")

IF (NOT DEFINED MSVC)
    set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -fPIC" )
    set( CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -fPIC" )
endif()

set(BUILD_DICTS 1)

if (EXISTS  ${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.my)
    message ("use " ${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.my)
    include (${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.my)
endif()


set(DICTS_FOLDER  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/Dicts )
add_subdirectory (morph_dict)


add_subdirectory(pybind11)

pybind11_add_module(${PROJECT_NAME} binding/main.cpp)

target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_17)

# PYLEM_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
if (NOT DEFINED PYLEM_VERSION_INFO)
    set (PYLEM_VERSION_INFO "dev")
endif()

target_compile_definitions(${PROJECT_NAME}
                           PRIVATE VERSION_INFO=${PYLEM_VERSION_INFO})

target_link_libraries(${PROJECT_NAME} PRIVATE
        ${PYTHON_LIBRARIES} LemmatizerBaseLib
)
