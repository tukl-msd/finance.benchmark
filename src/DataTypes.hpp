//
// Copyright (C) 2011, 2013 University of Kaiserslautern
// Microelectronic Systems Design Research Group
//
// This file is part of the financial mathematics research project
// de.uni-kl.eit.ems.finance

/// \file
/// \brief common data structures used for option pricers
/// \author Christian Brugger, Christian de Schryver, Ivan Shcherbakov
//

#pragma once

#define BOOST_ALL_DYN_LINK
#include <boost/shared_ptr.hpp>

#include <vector>

using boost::shared_ptr;

namespace Finance
{

//TODO: check if still needed
typedef double DataPathType;

/**
 * \brief defines the type of the option
 * \details At the moment, we only consider European barrier options.
 */
enum OptionType
{
	/// put option with regular payoff
	kPut = 2,
	/// call option with regular payoff
	kCall = 1,
	/// digital put option with fixed payoff
	kPutDigital = 4,
	/// digital call option with fixed payoff
	kCallDigital = 3,
};

/**
 * \brief defines the type of a barrier or removes it
 */
enum BarrierType
{
	kKnockIn = 2,
	kKnockOut = 1,
	kInvalid = 0 // no barrier set
};

/**
 * \brief a barrier structure
 */
class Barrier
{
public:
	double Value;
	/// also used to mark barrier as invalid
	BarrierType Type;
};

/**
 * \brief defines all parameters of a barrier option
 * \details At the moment, we only consider European barrier options 
 * with two barriers. A barrier can be set to invalid with BarrierType 
 * kInvalid.
 */
struct BarrierOption
{
	/// the run time of the option in years; i.e. 2.75 means 2.75 years
	double TimeToMaturity;	//T
	double StrikePrice;		//K
	Barrier LowerBarrier, UpperBarrier;
	OptionType Type;
};

/**
 * \brief defines all market parameters used in the Heston model
 */
struct HestonMarket
{
	// S_0 = asset price at t=0
	double AssetSpotPrice;
	// mu = drift or riskless interest rate
	double RisklessInterestRate;
	// V_0 = volatility at t=0
	double CurrentVolatility;
	// eta = volatility of the volatility = variance of v(t)
	double VolatilityOfVolatility;
	// kappa = rate at which v(t) reverts to theta
	double ModelRevertionRate;
	// theta = long run average price variance
	double LongTermAverageVolatility;
	// rho = correlation
	double Correlation;	
};

/**
 * \brief Combines heston market and barrier option parameters
 */
struct HestonBarrierOption
{
	HestonMarket market;
	BarrierOption option;
};

/**
 * \brief Reference value for comparison
 */
struct ReferencePrice
{
	double Price;
	double PricePrecision;
};

/**
 * \brief Combines heston barrier option parameters and reference price
 */
struct HestonBenchmarkParams
{
	HestonBarrierOption params;
	ReferencePrice reference;
};

typedef shared_ptr<std::vector<HestonBenchmarkParams> > HestonBenchmarkSetPtr;
typedef shared_ptr<std::vector<HestonBarrierOption> > HestonBarrierOptionSetPtr;
typedef shared_ptr<std::vector<double> > PricerResultPtr;




}

