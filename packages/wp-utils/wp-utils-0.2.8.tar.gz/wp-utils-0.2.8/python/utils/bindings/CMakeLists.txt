# ~~~
# CMake configuration rules used to generate Python Bindings via Pybind11
# ~~~

if(NOT TARGET utils::utils)
  loco_message("Bindings require the [utils::utils] target to be defined"
               LOG_LEVEL WARNING)
  return()
endif()

# Create target for our python bindings (standalone MODULE)
pybind11_add_module(
  utils_bindings
  MODULE
  ${CMAKE_CURRENT_SOURCE_DIR}/logging_py.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/path_handling_py.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/timing_py.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/perlin_noise_py.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/profiling_py.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/bindings_py.cpp)
target_include_directories(utils_bindings
                           PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(utils_bindings PRIVATE utils::utils)
