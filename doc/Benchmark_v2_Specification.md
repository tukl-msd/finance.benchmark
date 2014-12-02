Heston Benchmark v2.0 - Specification

Motivation and Goals
===

Developing accelerators for financial computations is currently a hot research topic. Many publications are out presenting dedicated SIMD, GPU, FPGA, ASIP, or ASIC implementations aimed to increase either the speed or the energy efficiency of one or a set of tasks. However, due to the large variety of underlying problems, models, algorithms, implementations, and evaluation metrics, it is nearly impossible to fairly tell which implementation is “best” for a given scenario.
Evaluating and comparing different implementations is a challenge, especially if the target platforms differ.

The point is that not all algorithms are suitable for all architectures, e.g. Monte Carlo methods might not converge as fast as quadrature or finite difference methods, but can easily be parallelized and therefore fit to highly parallel architectures like FPGAs or clusters. At the same time, cloud computing is moving into the finance domain and more and more institutes are going to offload compute intensive applications to cloud services. It is hard to evaluate how “good” those services perform compared to optimized GPU or FPGA solutions that can be kept in house.

In addition, there is a difference between pricing only a single product and running a complete batch of pricing tasks. The system latency is a critical factor that needs to be considered here.

We therefore see a strong demand for a portable benchmark set that allows to evaluate the performance of a pricing system independent of its underlying architecture.

Our goals are:

* To provide an unambiguous, platform and algorithm independent benchmark of derivatives pricing problems.
    * As part of the derivatives pricing benchmark, we provide an executable implementation that generates the correct reference results. This reference implementation is freely available here `TODO: Insert link here`
    * The benchmark parameters reflect meaningful and realistic scenarios found in markets, but also cover corner cases as observed in the days just before a crash or other peculiar events.
    * The benchmark framework is modular, and so is easily extendable to more products and models. Where possible, we provide guidance as to how it should be extended.
    
* To provide clear guidance on the performance metrics that should be reported for an implementation of the benchmark
    * The categories and units of metrics that should be reported are specified as part of this benchmark.
    * Where necessary we offer guidance as to how these metrics should be gathered and/or reported.

In order to achieve these goals, we need researchers and developers, both in academic institutions and private companies:

* To use and endorse the benchmark. The benchmark is only useful if it is credible amongst the target audience of computational finance acceleration research community.
* Input in the form of suggestions for the improvement and extension of the benchmark

Pricing Problems
===

Problem Structure
---

Depending on their application (single price computation vs. portfolio evaluation, VaR, ...), the performance of product pricers can differ in a wide range, e.g. from a non-optimized single-threaded CPU program up to dedicated high-speed dataflow architectures or huge clusters.
The benchmark seeks to address the complete range, e.g. by providing several complex test batteries with different computational complexity.

The benchmark has two levels of input:

- Pricing task: a single pricing problem over a single underlying such as a unit of stock or commodity and an option product that depends upon this underlying.
- Pricing workload: a set of Pricing Tasks as defined above.

A use case of the benchmark is that a given implementation will be applied to a workload or option pricing task, and will be found to meet a particular accuracy level (whether through design or luck). The performance characteristics of the implementation for that workload or task at that accuracy band would then be reported.

The parameters provided are derived from ...

`TODO: specify data sources - whether historical or stochastic`

Underlyings
-----------

The underlyings are defined in terms of the following models:

- [Black Scholes] [1]
- [Black Scholes with Jump Diffusion] [2]
- [Heston] [3]

`TODO: More authoratative references needed`

Ranges of the walk parameters should reflect typical
underlyings observed in the market - a good approach
would be to pick a whole bunch of actual time-series
at different points in time (say 100 underlyings over
10 year-long periods to give 1000 underlyings, or
3000 for a full fit with all thre models), then
do a maximum entropy fit. If this doesn't result in
any "hard" parameters, then we'd want to revisit that.

The benchmark's 3000 underlyings are fixed, tabulated, and the parameters are made available in this csv file `TODO: Insert link here.`. Each underlying is uniquely identifiable by an Underlying ID.

[1]: http://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model "Black Scholes"
[2]: http://www.quantstart.com/articles/Jump-Diffusion-Models-for-European-Options-Pricing-in-C "Black Scholes with Jump Diffusion"
[3]: http://en.wikipedia.org/wiki/Heston_model "Heston"



Options
-------

The option product is one of:

- [Single-barrier knockout or knockin] [1]
- [Double-barrier knockout] [2]
- [Lookback] [3]
- [Arithmetic Asian] [4]

`TODO: More authoratative references needed`

All options have Eurpopean excericse properties, however are continuously observed. This makes for interesting problems mathematically, and provides opportunities for algorithmic refinement.

The benchmark's 1000 options are fixed, tabulated, and the parameters are made available in this csv file `TODO: Insert link here.`. Each option is uniquely identifiable by an Option ID.

Two possible points of expansion:

* Considering the defined options with American or Bermudian exercise properties. For the Bermudian case, the excercise point considered should be once a day at midday, with 252 trading days per year.
* Defining products such as portfolios or basket options that are based upon the defined options. In this case, some degree of correlation should be specified between any options that share underlyings.

We plan to enhance the benchmark for more products later, e.g. to American / Bermudian options, products and models with relationships - products which depend on other products, models that are correlated (e.g. basket options, credit and forex swaps).

[1]: http://en.wikipedia.org/wiki/Barrier_option "Single-barrier knockout or knockin"
[2]: http://www.investopedia.com/terms/d/doublebarrieroption.asp "Double-barrier knockout"
[3]: http://en.wikipedia.org/wiki/Lookback_option "Lookback"
[4]: http://en.wikipedia.org/wiki/Asian_option "Arithmetic Asian"

TODO: refine:
The parameters are again inspired by real-world option
parameters, though in this case it is less clear how
to choose them. There is a reasonable argument for
choosing them equally spaced in some sense, rather
than driven by traded volume or something, as we
don't know what is important to different people.
It is crucial that the provided model parameters reflect realistic scenarios a) of day-to-day situations in different markets (e.g. liquid stock exchange, FOREX, …), but also critical corner cases that have shown to be hard to handle in the past. The data should therefore be legitimated carefully by one or more of the business partners (see below).


TODO: refine:
We need to ensure that prices end up in the "meaningful"
range, so that we don't get prices in the range which
could get rounded to zero, or cause problems with
relative error. I don't know how to define that
right now though :)
TODO from Gordon:
* Provide ranges of values for parameters, so that researchers could generate their own problems that are still "sensible". To simulate market pricing conditions, researchers could then also generate products on the fly from the ranges, and characterise how their systems cope with these sorts of problems.


Workloads
---------
A pricing task within the benchmark is formed from 10000 pairings of the defined underlyings and options that have non-zero values. Each task is defined by its unique Task ID, as well as Underlying ID and Option ID that comprises its pairing. A reference value is also provided. The pairings are fixed, and are made available in this CSV file `TODO: Insert link here.`.

Two categories of workloads are defined:

* Size-bound workloads:
    * Single task workloads. As there are 10000 tasks defined within the benchmark, there are 10000 single task workloads possible within the benchmark.
    * 100 task workloads. Each 100 tasks are bundeled into a single workload. `TODO: add further clarification as how the tasks should be bundeled`.
    * 10000 task workload. This is a single workload comprising all of the tasks defined within the benchmark.
    
* Underlying or Option Category workloads: Tasks which incorporate particular underlying or option type might be considered, e.g. all of the Heston underlyings or all of the Lookback Options. Furthermore, the combination of a particular option and underlying may also be considered, e.g. all of the tasks which are Asian options with Black Scholes underlyings.

A point of expansion is to create new tasks by consider underlying and option pairings beyond those defined within the framework. Options with non-zero values (verified using the reference implementations) are recommended so as to ensure that the pricing tasks are sufficiently complex.

Accuracy Levels
--------------

The primary accuracy metric is relative error, rather than absolute error, simply because it is more difficult to achieve and is more applicable in the financial domain.

There are three accuracy bands defined within the framework:

- Low: tol = 0.001 (1e-3)
- Standard: tol = 0.0001 (1e-5)
- High: tol = 0.0000001 (1e-7)

The intent is that the Low band is appropriate for low latency calculations, e.g. real-time risk, Standard is intended for more general risk analysis purposes, and High is really only of academic interest to show that a method can scale to high accuracies. `TODO: Should probably add a reference for these claims`

(In order for this to meaningful, that means that we
need to have reference prices for all tasks in the
workload that are accurate down to around 1e-8.
That may actually be infeasible, but it would be
interesting if it were a spur or a challenge to
people.)

Accuracy for a workload is defined in terms of RMSE. If there is a workload of _n_ items, and _e\_i_ and _o\_i_ are the observed and expected prices, then in order to meet a given accuracy band, __both__ criteria must be met:

1. tol >= sqrt( sum( ( (e_i-o_i)/e_i )^2, i=1..n) / n )
2. 4*tol >= max( (e_i-o_i)/e_i, i=1..n )

The second criterion is to avoid high variance
solutions which are good on average, given
that infrequent but high error solutions are
a bad thing in practise.

(My feeling is that there should be a way to
define this in a way that depends on $n$, but
I'm not sure of the maths right now. I'd have to do
some thinking, but it feels like the maximum allowed
error should grow as a function of $\sqrt{n}$, both for
statistical and numerical reasons.)

Results Reporting
===

Performance Metrics
-----------

Performance is measured in three ways:

- Throughput: average tasks per second
- Latency: maximum seconds per task
- Energy: average joules per task

We might as well also capture the achieved accuracy
statistics within the band as well, so two other fields
are:
- RMSE Error
- Worst Error

For the given work-load of 10K options, the latency
and throughput are measured for batches of:
- 1 task for each of 10K batches
- 100 tasks for each of 100 batches.
- 10K tasks in a single batch

Latency for a batch is measured from the point
that the first task in a batch enters the system, to the
point that the last task in a batch leaves the
system. The next batch cannot enter until the
previous batch has left.

Throughput is measured across all batches, from the
time that the first task of the first batch enters to the
time that the last task of the last batch leaves. As
before, the next batch still cannot enter until the
previous batch leaves. Energy is measured in the same
way, in terms of power consumption from the first
task entering till the last task exits.

Entry and exit of the task is arbitrarily defined
as ingress and egress over a network port, in order
to capture any pre or post processing needed.


Results
-------

So the reported results look like:


Accuracy XXXX
                           |  1/10K  | 100/100 |  10K/1  |
---------------------------+---------+---------+---------|
Throughput (Tasks/Second)  |         |         |         |
---------------------------+---------+---------+---------|
Latency    (Seconds/Task)  |         |         |         |
---------------------------+---------+---------+---------|
Energy     (Joules/Task)   |         |         |         |
---------------------------+---------+---------+---------|
RMSE Error                 |                             |
---------------------------+-----------------------------|
Worst Error                |                             |
---------------------------+-----------------------------+

(Presumably error doesn't vary with batch size - if it does,
it can be broken down.)


In addition to the main scoring, the two following aspects shall be included in the benchmark reports, either in textual form or as a second soft-score:

* Design Effort  
The time it takes to design or re-design a solver is a significant consideration as developers need to get working results quickly. Many applications are also frequently tweaked and modified.

* Portability  
Related to the previous aspect. How difficult is it to re-deploy an existing solution onto a different device of the same architecture / a new device of a next generation architecture / a completely different architecture? 

* Flexibility
TODO: discuss:
	* give penalty points for products that cannot be priced (formal)?
	* only text description?



Reference Implementation
====
The benchmark will consist of an automated evaluation framework with standard interfaces to arbitrary pricer implementations written in a high-level language.
TODO: refine / discuss:
- parameter inputs + result outputs
- JSON?
- where should time and latency be measured? or given by user?

The benchmark will contain an executable sequential classic Monte Carlo CPU pricer reference implementation.
Its goal is to make all the results reproducible and serve as a starting point for those who want to benchmark their own implementations.







Preliminary work
===

* The University of Kaiserslautern has already released a first version of a Heston benchmark for European double barrier option pricing ([www.uni-kl.de/benchmarking][1]) together with 12 predefined Heston parameter sets taken from literature. However, this version has some weaknesses:

   [1]: http://www.uni-kl.de/benchmarking

	1. The required accuracy of the result is not specified, so the result accuracy can freely be determined and therefore influences runtime and energy consumption and so decreases the comparability.

	2. There is no scoring for easy comparison.

	3. The benchmark is not challenging enough for high-performance clusters or pricing engines. 

* STAC industrial benchmarks for finance


Partners and Contributions
===

Possible contributors:

* Imperial College
	* implementation competences
	* benchmark construction know-how
	* implementation complexity studies of different algorithms

* University of Kaiserslautern
	* multiple implementations of option pricers based on the Heston model
	* Heston competences
	* interdisciplinary cooperation with finance mathematicians and computational stochastic group

* Maxeler
	* Stephen Weston: high finance competences

* SWIP
	* calibrated Heston parameters from real market data

* Fraunhofer ITWM
	* own Heston implementations
	* meaningful market data
	* contacts to many finance institutes

* J.P. Morgan
