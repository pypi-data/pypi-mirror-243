# CMake generated Testfile for 
# Source directory: /home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/ParallelTempering
# Build directory: /home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/MarkovChain/ParallelTempering
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ColdnessTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/MarkovChain/ParallelTempering/ColdnessTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/reports/ColdnessTestSuite.xml")
set_tests_properties(ColdnessTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/MarkovChain/ParallelTempering" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/ParallelTempering/CMakeLists.txt;8;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/ParallelTempering/CMakeLists.txt;0;")
add_test(ParallelTemperingTestSuite "/usr/bin/mpiexec" "--oversubscribe" "-n" "3" "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/MarkovChain/ParallelTempering/ParallelTemperingTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/test-reports/ColdnessTestSuite.xml")
set_tests_properties(ParallelTemperingTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-release/tests/MarkovChain/ParallelTempering" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/ParallelTempering/CMakeLists.txt;22;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/ParallelTempering/CMakeLists.txt;0;")
