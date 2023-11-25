cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

# -------------------------------------
# Get loco_cmake to help us configure our CMake based project
include(FetchContent)
FetchContent_Declare(
  loco_cmake
  GIT_REPOSITORY https://github.com/wpumacay/loco_cmake.git
  GIT_TAG d1ba4734dcf29bbc7318deea16213452a80b3f2a # Version v0.1.4
  GIT_PROGRESS FALSE
  GIT_SHALLOW TRUE)
FetchContent_MakeAvailable(loco_cmake)
include(${loco_cmake_SOURCE_DIR}/Index.cmake)

# -------------------------------------
# Define our project :)
project(
  Utils
  VERSION 0.2.8
  DESCRIPTION "A library of common functionality used alongside my projects"
  HOMEPAGE_URL "https://github.com/wpumacay/utils"
  LANGUAGES C CXX)

# -------------------------------------
# Define some options the user can set before|while configuring the project
option(UTILS_BUILD_PYTHON_BINDINGS "Build bindings (requires Pybind11)" ON)
option(UTILS_BUILD_EXAMPLES "Build C++ examples" ON)
option(UTILS_BUILD_DOCS "Build documentation (requires Doxygen)" OFF)
option(UTILS_BUILD_TESTS "Build C++ unit-tests (requires Catch2)" ON)

# cmake-format: off
set(UTILS_BUILD_CXX_STANDARD 17 CACHE STRING "The C++ standard to be used")
set_property(CACHE UTILS_BUILD_CXX_STANDARD PROPERTY STRINGS 11 14 17 20)
# cmake-format: on

# -------------------------------------
# Initialize the project using our helper modules :D
loco_initialize_project(CXX_STANDARD ${UTILS_BUILD_CXX_STANDARD})

# -------------------------------------
# Allow the usage of our helper macros and functions
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")

# -------------------------------------
# Bring our dependencies accordingly
include(UtilsDependencies)

# cmake-format: off
# -------------------------------------
# Setup the main C++ target `UtilsCpp`
loco_create_target(UtilsCpp STATIC
 SOURCES
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/common.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/logging.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/timing.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/profiling.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/path_handling.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/perlin_noise.cpp
   ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/obj_loader.cpp
 INCLUDE_DIRECTORIES
   ${CMAKE_CURRENT_SOURCE_DIR}/include
 TARGET_DEPENDENCIES
   spdlog::spdlog math::math tinyobjloader
 CXX_STANDARD
    ${UTILS_BUILD_CXX_STANDARD}
 WARNINGS_AS_ERRORS FALSE)
# cmake-format: on

# -------------------------------------
# Expose an alias for the library (CMake namespace convention)
add_library(utils::utils ALIAS UtilsCpp)

# -------------------------------------
# Add the set of examples created along this project
if(UTILS_BUILD_EXAMPLES)
  add_subdirectory(examples)
endif()

# -------------------------------------
# Add C++ tests to the build process
if(UTILS_BUILD_TESTS)
  add_subdirectory(tests/cpp)
endif()

# -------------------------------------
# Add the set of Python bindings created for UtilsCpp
if(UTILS_BUILD_PYTHON_BINDINGS)
  add_subdirectory(python/utils/bindings)
endif()

# -------------------------------------
# Build the required documentation accordingly
if(UTILS_BUILD_DOCS)
  # cmake-format: off
  # -------------------------------------
  # Setup documentation for our target
  loco_setup_cppdocs(UtilsCpp
    DOXYGEN_FILE_IN ${CMAKE_CURRENT_SOURCE_DIR}/docs/Doxyfile.in
    DOXYGEN_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/docs/Doxygen
    DOXYGEN_GENERATE_HTML FALSE
    DOXYGEN_GENERATE_LATEX FALSE
    DOXYGEN_GENERATE_XML TRUE
    DOXYGEN_QUIET TRUE
    SPHINX_FILE_IN ${CMAKE_CURRENT_SOURCE_DIR}/docs/conf.py.in
    SPHINX_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/docs/Sphinx
    SPHINX_BREATHE_PROJECT UtilsCpp
    SPHINX_DOXYGEN_XML_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/docs/Doxygen/xml)
  # cmake-format: on
endif()

# -------------------------------------
# Show the properties of our main target
loco_print_target_properties(UtilsCpp)

# -------------------------------------
# Show some info of the this project
loco_print_project_info()
