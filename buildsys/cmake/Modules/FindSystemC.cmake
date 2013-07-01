# - Finds SystemC
# Try to find SystemC include dirs and libraries
# 
# Once done the following variables will be defined
#  SystemC_FOUND
#  SystemC_INCLUDE_DIRS
#  SystemC_LIBRARIES
#
# You may set the following variables
#
#	SYSTEMC_ROOT	The preferred installation prefix for searching for
#					SystemC. Set this if the module has problems finding
#					the propper SystemC isntallation.
#
#					The variable is also available as environment variable.
#					Also, note that it is completely uppercase.
#
#	SystemC_DEBUG	Set this to TRUE to enable debugging output
#
 
# ============================================================================
# Copyright (C) 2013 University of Kaiserslautern
# Microelectronic Systems Design Research Group
#
# This file is part of the financial mathematics research project
# de.uni-kl.eit.ems.finance
# 
# Christian Brugger (brugger@eit.uni-kl.de)
# 25. January 2013
# ============================================================================

if(MSVC)
	add_definitions(/vmg)
endif()

# find include path
find_path(SystemC_INCLUDE_DIR systemc.h
	PATH_SUFFIXES include src
	PATHS ${SYSTEMC_ROOT} ENV SYSTEMC_ROOT
)

# find release libs
find_library(SystemC_LIBRARY_RELEASE systemc
	PATH_SUFFIXES lib-linux64 msvc80/SystemC/Release
	PATHS ${SYSTEMC_ROOT} ENV SYSTEMC_ROOT
)

# find debug libs
find_library(SystemC_LIBRARY_DEBUG systemc
	PATH_SUFFIXES lib-linux64 msvc80/SystemC/Debug
	PATHS ${SYSTEMC_ROOT} ENV SYSTEMC_ROOT
)

# if the generator supports configuration types then set
# optimized and debug libraries, or if the CMAKE_BUILD_TYPE has a value
if(CMAKE_CONFIGURATION_TYPES OR CMAKE_BUILD_TYPE)
	set(SystemC_LIBRARY optimized ${SystemC_LIBRARY_RELEASE} debug ${SystemC_LIBRARY_DEBUG})
else()
	# if there are no configuration types and CMAKE_BUILD_TYPE has no value
	# then just use the release libraries
	set(SystemC_LIBRARY ${SystemC_LIBRARY_RELEASE} )
endif()

set(SystemC_INCLUDE_DIRS ${SystemC_INCLUDE_DIR})
set(SystemC_LIBRARIES ${SystemC_LIBRARY})

if(SystemC_DEBUG)
	message(STATUS "CMAKE_SYSTEM_INCLUDE_PATH = ${CMAKE_SYSTEM_INCLUDE_PATH}")
	message(STATUS "CMAKE_SYSTEM_FRAMEWORK_PATH = ${CMAKE_SYSTEM_FRAMEWORK_PATH}")
	message(STATUS "SYSTEMC_ROOT = $ENV{SYSTEMC_ROOT} ${SYSTEMC_ROOT}")
	message(STATUS "SystemC_INCLUDE_DIRS = ${SystemC_INCLUDE_DIRS}")
	message(STATUS "SystemC_LIBRARIES = ${SystemC_LIBRARIES}")
endif()

#TODO: extract version from header file

set(SystemC_ERROR_MSG "Could NOT find SystemC. 
		Please set SYSTEMC_ROOT to the root directory containing SystemC.")

#TODO: check version
#TODO: print version
find_package_handle_standard_args(SystemC ${SystemC_ERROR_MSG}
		SystemC_INCLUDE_DIR SystemC_LIBRARY)

# show these variables only in the advanced view
mark_as_advanced(SystemC_INCLUDE_DIR SystemC_LIBRARY)

