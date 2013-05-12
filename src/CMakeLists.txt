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

include_directories(.)

### Boost library ###
find_package(Boost 1.44)
include_directories(${Boost_INCLUDE_DIR})
#####################

set(HEADERS
	DataTypes.hpp
	HestonBenchmark.hpp
	HestonPricerBase.hpp
)
source_group("Header Files" FILES ${HEADERS})

set(SOURCE
	HestonBenchmark.cpp
)

add_library(benchmark STATIC ${SOURCE} ${HEADERS})

INSTALL(FILES ${HEADERS} DESTINATION include)
INSTALL(TARGETS benchmark
		LIBRARY DESTINATION lib)