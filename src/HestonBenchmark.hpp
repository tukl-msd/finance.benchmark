//
// Copyright (C) 2011, 2013 University of Kaiserslautern
// Microelectronic Systems Design Research Group
//
// This file is part of the financial mathematics research project
// de.uni-kl.eit.ems.finance

/// \file
/// \brief a reference benchmark for Heston pricers
/// \author Christian Brugger Christian de Schryver
//

#pragma once

#include "DataTypes.hpp"
#include "HestonPricerBase.hpp"

namespace Finance
{
/**
 * \brief a reference benchmark for Heston pricers with a new case 
 * from Baldeaux, Roberts, Quasi-Monte Carlo Methods for the 
 * Heston Model, p. 7 Table 1
 */
class HestonBenchmark
{
public:
	HestonBenchmark(HestonPricerBase* pricer, bool bOwn=false);

	~HestonBenchmark();

	/// Get benchmark set
	HestonBenchmarkSetPtr GetBenchmarkSet(unsigned int benchmark_set);

	/// run the selected benchmark set and check the results
	/// \return true if the returned price matches the reference price
	bool RunSingleSet(unsigned int benchmark_set);

	/// run all benchmark set and check the results
	/// \return true if the returned price matches the reference price
	bool RunAll();

	unsigned int GetNumberOfBenchmarkSets();


private:
	HestonPricerBase* _pPricer;
	bool _ownPricer;
};

}
