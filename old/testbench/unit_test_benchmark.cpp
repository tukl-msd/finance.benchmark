//
// Copyright (C) 2013 University of Kaiserslautern
// Microelectronic Systems Design Research Group
//
// This file is part of the financial mathematics research project
// de.uni-kl.eit.ems.finance
//
// Christian Brugger (brugger@eit.uni-kl.de)
// 17. January 2013
//

// Boost
#define BOOST_ALL_DYN_LINK
#define BOOST_TEST_MODULE Main
#include <boost/test/unit_test.hpp>

#include "HestonBenchmark.hpp"

#include <thread>

using namespace Finance;

class HestonPricer: public HestonPricerBase {
public:
	virtual PricerResultPtr Run(HestonBarrierOptionSetPtr set) {
		PricerResultPtr res(new std::vector<double>(1, 0));
		//std::this_thread::sleep_for(std::chrono::milliseconds(123));
		//usleep(123000);
		return res;
	}
};

BOOST_AUTO_TEST_CASE(Test1) {
	HestonPricer pricer;
	HestonBenchmark benchmark(&pricer);

	BOOST_CHECK(benchmark.RunAll());
}

