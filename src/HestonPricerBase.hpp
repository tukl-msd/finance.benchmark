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

#pragma once

#include "DataTypes.hpp"

namespace Finance
{

/**
 * \brief implements the interface for all Heston pricers
 * \details This is the base class for all Heston model pricers.
 * The pricers in general consume two input structures:
 * The first defines the parameters of the option to be prices,
 * the second gives all market parameters needed in the Heston model.
 * The pricers return the computed option price,
 * as well as the run time of the computation.
 */
class HestonPricerBase
{
public:
	virtual ~HestonPricerBase() {};

	/// computes a new result and returns it
	virtual PricerResultPtr Run(HestonBarrierOptionSetPtr set) = 0;
};

}
