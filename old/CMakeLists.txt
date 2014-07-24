#
# Copyright (C) 2013 University of Kaiserslautern
# Microelectronic Systems Design Research Group
#
# This file is part of the financial mathematics research project
# de.uni-kl.eit.ems.finance
# 
# Christian Brugger (brugger@eit.uni-kl.de)
# 19. April 2013
#

cmake_minimum_required(VERSION 2.8)
project(finance.pricingbenchmark)

include(buildsys/CMakeShared.txt)

if(CMAKE_COMPILER_IS_GNUCXX)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=gnu++0x")
endif(CMAKE_COMPILER_IS_GNUCXX)

add_doxygen_support(../../)

enable_testing()
add_subdirectory(src)
add_subdirectory(testbench)

