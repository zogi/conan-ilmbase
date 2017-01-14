PROJECT(PackageTest)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package(IlmBase REQUIRED)

ADD_EXECUTABLE(testPackage main.cpp testMatrix.cpp)
include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${ILMBASE_INCLUDE_DIRS})
link_directories(${ILMBASE_LIBRARY_DIR})
TARGET_LINK_LIBRARIES(testPackage ${ILMBASE_LIBRARIES})
