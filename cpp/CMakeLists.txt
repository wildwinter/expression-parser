cmake_minimum_required(VERSION 3.15)
project(ExpressionParser LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add include directory
include_directories(include)

# Source files
file(GLOB LIB_SOURCES "src/*.cpp")
file(GLOB LIB_HEADERS "include/expression_parser/*.h")

# Create the library (static or shared)
option(BUILD_SHARED_LIBS "Build shared libraries instead of static" ON)
add_library(${PROJECT_NAME} ${LIB_SOURCES} ${LIB_HEADERS})

# Set properties for export
set_target_properties(${PROJECT_NAME} PROPERTIES
    PUBLIC_HEADER "${LIB_HEADERS}"
)

# Install target
install(TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION lib  # For shared libraries
    ARCHIVE DESTINATION lib  # For static libraries
    PUBLIC_HEADER DESTINATION include/expression_parser
)

# Add a test executable
add_executable(tests 
    test/catch_amalgamated.cpp
    test/test_parser.cpp
    test/test_writer.cpp
    test/test_utils.cpp)

# Link the library to the test executable
target_link_libraries(tests PRIVATE ExpressionParser)

# Include Catch2 header (if not installed globally)
target_include_directories(tests PRIVATE include)

# Enable testing (CMake's built-in test support)
enable_testing()

# Register the test executable
add_test(NAME ExpressionParserTests COMMAND tests -r console)