# CMake generated Testfile for 
# Source directory: /home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain
# Build directory: /home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(MarkovChainFactoryTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain/MarkovChainFactoryTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/MarkovChainFactoryTestSuite.xml")
set_tests_properties(MarkovChainFactoryTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;17;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;0;")
add_test(ModelMixinTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain/ModelMixinTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/ModelMixinTestSuite.xml")
set_tests_properties(ModelMixinTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;17;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;0;")
add_test(ModelWrapperTestSuite "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain/ModelWrapperTestSuite" "--log_format=JUNIT" "--log_sink=/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/reports/ModelWrapperTestSuite.xml")
set_tests_properties(ModelWrapperTestSuite PROPERTIES  WORKING_DIRECTORY "/home/jadebeck/repos/hopsy/extern/hops/cmake-build-debug/tests/MarkovChain" _BACKTRACE_TRIPLES "/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;17;add_test;/home/jadebeck/repos/hopsy/extern/hops/tests/MarkovChain/CMakeLists.txt;0;")
subdirs("ParallelTempering")
subdirs("Proposal")
subdirs("Recorder")
subdirs("Tuning")
