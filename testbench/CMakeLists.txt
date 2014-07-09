#
# Copyright (C) 2013 University of Kaiserslautern
# Microelectronic Systems Design Research Group
#
# This file is part of the financial mathematics research project
# de.uni-kl.eit.ems.finance
# 
# Christian Brugger (brugger@eit.uni-kl.de)
# 03. May 2013
#

enable_testing()

include_directories(.)
include_directories(../src)

### Boost library ###
find_package(Boost 1.41 COMPONENTS unit_test_framework REQUIRED)
include_directories(${Boost_INCLUDE_DIR})
#####################

add_executable(unit_test unit_test_benchmark.cpp)
target_link_libraries(unit_test ${Boost_LIBRARIES})
target_link_libraries(unit_test heston_benchmark)

add_test(unit_test ${CMAKE_CURRENT_BINARY_DIR}/unit_test 
		--detect_memory_leaks=0)

