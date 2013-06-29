//
// Copyright (C) 2011, 2013 University of Kaiserslautern
// Microelectronic Systems Design Research Group
//
// This file is part of the financial mathematics research project
// de.uni-kl.eit.ems.finance

/// \file
/// \brief base class for all Heston pricers
/// \author Christian Brugger, Christian de Schryver
//

//a reference benchmark for Heston pricers with a new case from Baldeaux, 
//Roberts, Quasi-Monte Carlo Methods for the Heston Model, p. 7 Table 1

#include "HestonBenchmark.hpp"

#include <boost/make_shared.hpp>

#include <iostream>
#include <chrono>
#include <stdexcept>

namespace Finance
{

HestonBenchmark::HestonBenchmark(HestonPricerBase* pricer, bool bOwn)
	: _pPricer(pricer), _ownPricer(bOwn)
{
}

HestonBenchmark::~HestonBenchmark()
{
	if (_ownPricer)
		delete _pPricer;
}


void HestonBenchmark::PrettyPrintSimResult(HestonBenchmarkSetPtr set, 
			PricerResultPtr res_set) {
	printf("======================RESULT====================\n");
	for (std::vector<HestonBenchmarkParams>::size_type i = 0; 
			i < set->size(); ++i) {
		printf("Simulation result      = %f\n", res_set->at(i));
		printf("Reference value        = %f\n", set->at(i).reference.Price);
		printf("Precicion of reference = %f\n", set->at(i).reference.PricePrecision);
	}
	printf("======================RESULT====================\n\n");
}


HestonBarrierOptionSetPtr HestonBenchmark::getHestonBarrierOptionSet(
		HestonBenchmarkSetPtr set) {
	
	HestonBarrierOptionSetPtr res(
			new std::vector<HestonBarrierOption>(set->size()));
	for (std::vector<HestonBenchmarkParams>::size_type i = 0; 
			i < set->size(); ++i) {
		(*res)[i] = (*set)[i].params;
	}
	return res;
}

bool HestonBenchmark::RunSingleSet(unsigned int benchmark_set)
{
	HestonBenchmarkSetPtr set = GetBenchmarkSet(benchmark_set);
	HestonBarrierOptionSetPtr barrier_set = getHestonBarrierOptionSet(set);
	auto t1 = std::chrono::high_resolution_clock::now();
	PricerResultPtr res_set = _pPricer->Run(barrier_set);
	auto t2 = std::chrono::high_resolution_clock::now();

	if (res_set->size() != set->size())
		throw std::runtime_error("Returned to few results");

	std::cout << "Benchmark " << benchmark_set << " took " <<
		std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() /
		1000. / 1000	<< " s." << std::endl;

	PrettyPrintSimResult(set, res_set);

	//this->SelectBenchmarkSet(benchmark_set);

	//HestonPricerResult MyResult = _pPricer->Run(set.params.option, set.params.market);

	//return CheckPrice(MyResult.Price, precision);
	return true;
}

bool HestonBenchmark::RunAll()
{
	bool res = true;
	for (unsigned int i = 1; i <= GetNumberOfBenchmarkSets(); ++i)
		res &= RunSingleSet(i);
	return res;
}

unsigned int HestonBenchmark::GetNumberOfBenchmarkSets()
{
	return 13;
}

HestonBenchmarkSetPtr HestonBenchmark::GetBenchmarkSet(unsigned int benchmark_set)
{
	HestonBenchmarkParams set;
	switch (benchmark_set)
	{
	//values taken from schjun_11
	case 1:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2;
		set.params.market.LongTermAverageVolatility = 0.09;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0.05;
		set.params.market.CurrentVolatility = 0.09;
		set.params.market.Correlation = -0.3;
		set.params.option.TimeToMaturity = 5;
		set.params.option.StrikePrice = 100;
		//set.params.option.LowerBarrier.Value = 90;
		//set.params.option.UpperBarrier.Value = 110;
		set.params.option.LowerBarrier.Type = kInvalid;
		set.params.option.UpperBarrier.Type = kInvalid;
		set.params.option.Type = kCall;

		set.reference.Price = 34.9998;
		set.reference.PricePrecision = 0.0001;
		break;

	case 2:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2;
		set.params.market.LongTermAverageVolatility = 0.09;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0.05;
		set.params.market.CurrentVolatility = 0.09;
		set.params.market.Correlation = -0.3;
		set.params.option.TimeToMaturity = 5;
		set.params.option.StrikePrice = 100;
		//set.params.option.LowerBarrier.Value = 90;
		set.params.option.UpperBarrier.Value = 120;
		set.params.option.LowerBarrier.Type = kInvalid;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.10280;
		set.reference.PricePrecision = 0.0001;
		break;

	case 3:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 1;
		set.params.market.LongTermAverageVolatility = 0.09;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.09;
		set.params.market.Correlation = -0.3;
		set.params.option.TimeToMaturity = 5;
		set.params.option.StrikePrice = 100;
		//set.params.option.LowerBarrier.Value = 90;
		set.params.option.UpperBarrier.Value = 120;
		set.params.option.LowerBarrier.Type = kInvalid;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.31606;
		set.reference.PricePrecision = 0.0003;
		break;

	case 4:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 0.5;
		set.params.market.LongTermAverageVolatility = 0.04;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.04;
		set.params.market.Correlation = 0;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 100;
		set.params.option.LowerBarrier.Value = 90;
		set.params.option.UpperBarrier.Value = 110;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.74870;
		set.reference.PricePrecision = 0.00001;
		break;

	case 5:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2.75;
		set.params.market.LongTermAverageVolatility = 0.035;
		set.params.market.VolatilityOfVolatility = 0.425;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.0384;
		set.params.market.Correlation = -0.4644;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 90;
		set.params.option.LowerBarrier.Value = 80;
		set.params.option.UpperBarrier.Value = 120;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 5.7576;
		set.reference.PricePrecision = 0.001;
		break;

	case 6:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 1;
		set.params.market.LongTermAverageVolatility = 0.09;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.09;
		set.params.market.Correlation = -0.3;
		set.params.option.TimeToMaturity = 5;
		set.params.option.StrikePrice = 100;
		set.params.option.LowerBarrier.Value = 66;
		set.params.option.UpperBarrier.Value = 150;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 3.0421;
		set.reference.PricePrecision = 0.005;
		break;

	case 7:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 0.5;
		set.params.market.LongTermAverageVolatility = 0.04;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0.08;
		set.params.market.CurrentVolatility = 0.04;
		set.params.market.Correlation = -0.9;
		set.params.option.TimeToMaturity = 10;
		set.params.option.StrikePrice = 90;
		set.params.option.LowerBarrier.Value = 66;
		set.params.option.UpperBarrier.Value = 150;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.017117;
		set.reference.PricePrecision = 0.0002;
		break;

	case 8:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2.75;
		set.params.market.LongTermAverageVolatility = 0.35;
		set.params.market.VolatilityOfVolatility = 0.425;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.384;
		set.params.market.Correlation = -0.4644;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 100;
		set.params.option.LowerBarrier.Value = 66;
		set.params.option.UpperBarrier.Value = 150;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.82286;
		set.reference.PricePrecision = 0.001;
		break;

	case 9:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2.75;
		set.params.market.LongTermAverageVolatility = 0.035;
		set.params.market.VolatilityOfVolatility = 0.425;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.0384;
		set.params.market.Correlation = -0.4644;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 100;
		set.params.option.LowerBarrier.Value = 80;
		set.params.option.UpperBarrier.Value = 120;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kPut;

		set.reference.Price = 1.5294;
		set.reference.PricePrecision = 0.0005;
		break;

	case 10:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2.75;
		set.params.market.LongTermAverageVolatility = 0.35;
		set.params.market.VolatilityOfVolatility = 0.425;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.384;
		set.params.market.Correlation = -0.4644;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 120;
		set.params.option.LowerBarrier.Value = 66;
		set.params.option.UpperBarrier.Value = 150;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCall;

		set.reference.Price = 0.17167;
		set.reference.PricePrecision = 0.0005;
		break;

	case 11:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 2.75;
		set.params.market.LongTermAverageVolatility = 0.035;
		set.params.market.VolatilityOfVolatility = 0.425;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.0384;
		set.params.market.Correlation = -0.4644;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 100;
		//set.params.option.LowerBarrier.Value = 80;
		set.params.option.UpperBarrier.Value = 120;
		set.params.option.LowerBarrier.Type = kInvalid;
		set.params.option.UpperBarrier.Type = kKnockIn;
		set.params.option.Type = kCall;

		set.reference.Price = 4.9783;
		set.reference.PricePrecision = 0.0005;
		break;

	case 12:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 1;
		set.params.market.LongTermAverageVolatility = 0.09;
		set.params.market.VolatilityOfVolatility = 1;
		set.params.market.RisklessInterestRate = 0;
		set.params.market.CurrentVolatility = 0.09;
		set.params.market.Correlation = -0.3;
		set.params.option.TimeToMaturity = 5;
		set.params.option.StrikePrice = 100;
		set.params.option.LowerBarrier.Value = 66;
		set.params.option.UpperBarrier.Value = 150;
		set.params.option.LowerBarrier.Type = kKnockOut;
		set.params.option.UpperBarrier.Type = kKnockOut;
		set.params.option.Type = kCallDigital;

		set.reference.Price = 0.16805;
		set.reference.PricePrecision = 0.0001;
		break;
	// value form Baldeaux, Roberts
	case 13:
		set.params.market.AssetSpotPrice = 100;
		set.params.market.ModelRevertionRate = 6.21;
		set.params.market.LongTermAverageVolatility = 0.019;
		set.params.market.VolatilityOfVolatility = 0.61;
		set.params.market.RisklessInterestRate = 0.0319;
		set.params.market.CurrentVolatility = 0.010201;
		set.params.market.Correlation = -0.70;
		set.params.option.TimeToMaturity = 1;
		set.params.option.StrikePrice = 100;
		//set.params.option.LowerBarrier.Value = 90;
		//set.params.option.UpperBarrier.Value = 110;
		set.params.option.LowerBarrier.Type = kInvalid;
		set.params.option.UpperBarrier.Type = kInvalid;
		set.params.option.Type = kCall;

		set.reference.Price = 6.80611;
		set.reference.PricePrecision = 0.0001;
		break;

	default:
		throw std::runtime_error("Unknown benchmark set");
		break;
	}

	HestonBenchmarkSetPtr res(new std::vector<HestonBenchmarkParams>(1, set));
	return res;
}

};
