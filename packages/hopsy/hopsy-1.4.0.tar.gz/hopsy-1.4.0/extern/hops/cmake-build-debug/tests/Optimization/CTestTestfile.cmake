# CMake generated Testfile for 
# Source directory: /home/jadebeck/repos/hopsy/extern/hops/tests/Optimization
# Build directory: /home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/Optimization
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(GaussianProcessTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/Optimization/GaussianProcessTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/GaussianProcessTestSuite.xml")
set_tests_properties(GaussianProcessTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/Optimization" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/Optimization/CMakeLists.txt;11;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/Optimization/CMakeLists.txt;0;")
add_test(ThompsonSamplingTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/Optimization/ThompsonSamplingTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/ThompsonSamplingTestSuite.xml")
set_tests_properties(ThompsonSamplingTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/Optimization" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/Optimization/CMakeLists.txt;11;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/Optimization/CMakeLists.txt;0;")
