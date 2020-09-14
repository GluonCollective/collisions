cmake_minimum_required(VERSION 3.13)
project(collisions)

set(CMAKE_BUILD_TYPE Debug)


list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "-O2 -pedantic -W -Wall -Wshadow -fPIC")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

find_package(Boost 1.67 COMPONENTS program_options REQUIRED)
find_package(yaml-cpp 0.6.2 REQUIRED)
find_package(Pythia8 REQUIRED)

include_directories("${PYTHIA8_INCLUDE_DIR}")

add_library(config STATIC config.cc)
target_link_libraries(config 
                     ${CMAKE_DL_LIBS} 
                     ${PYTHIA8_LIBRARIES} 
                     ${Boost_LIBRARIES}
                     yaml-cpp)


add_executable(generate generate.cc)
target_link_libraries(generate 
                      config 
                      ${CMAKE_DL_LIBS} 
                      ${PYTHIA8_LIBRARIES})


