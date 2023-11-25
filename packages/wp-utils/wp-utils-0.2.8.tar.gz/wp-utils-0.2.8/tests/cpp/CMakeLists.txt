# ~~~
# CMake configuration for C++ unittests
# ~~~
if(NOT TARGET utils::utils)
  loco_message("Unittests require target [utils::utils], but wasn't found"
               LOG_LEVEL WARNING)
  return()
endif()

if(NOT TARGET Catch2::Catch2)
  loco_message("Unittests require target [Catch2::Catch2], but wasn't found"
               LOG_LEVEL WARNING)
  return()
endif()

include(CTest)
include(Catch)

add_executable(UtilsCppTests ${CMAKE_CURRENT_SOURCE_DIR}/test_main.cpp
                             ${CMAKE_CURRENT_SOURCE_DIR}/test_logging.cpp)
target_link_libraries(UtilsCppTests PRIVATE utils::utils Catch2::Catch2)
# Discover tets and pick an integer as the random seed
catch_discover_tests(UtilsCppTests)
