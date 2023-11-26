# CMake generated Testfile for 
# Source directory: /home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram
# Build directory: /home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(LinearProgramFactoryTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram/LinearProgramFactoryTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/LinearProgramFactoryTestSuite.xml")
set_tests_properties(LinearProgramFactoryTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;22;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;0;")
add_test(LinearProgramClpImplTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram/LinearProgramClpImplTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/LinearProgramClpImplTestSuite.xml")
set_tests_properties(LinearProgramClpImplTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;22;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;0;")
add_test(LinearProgramGurobiImplTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram/LinearProgramGurobiImplTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/LinearProgramGurobiImplTestSuite.xml")
set_tests_properties(LinearProgramGurobiImplTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/LinearProgram" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;22;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/LinearProgram/CMakeLists.txt;0;")
