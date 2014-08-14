Problem domain
---------------

The benchmarks has two levels of input:
- Pricing task: a single pricing problem over an underlying and an option
- Pricing workload: a set of Pricing Tasks

A given implementation will be applied to a work-load,
and will be found to meet a particular accuracy level
(whether through design or luck). They can then report
the performance characteristics for that workload at
that accuracy band.

Underlyings
-----------

The underlying is one of:
 
 - Black Scholes
 - Jump Diffusion (BS)
 - Heston

Ranges of the walk parameters should reflect typical
underlyings observed in the market - a good approach
would be to pick a whole bunch of actual time-series
at different points in time (say 100 underlyings over
10 year-long periods to give 1000 underlyings, or
3000 for a full fit with all thre models), then
do a maximum entropy fit. If this doesn't result in
any "hard" parameters, then we'd want to revisit that.

The underlyings are fixed, tabulated, and made
available as a csv.

Options
-------

The option is one of:
 
 - Single-barrier knockout
 - Double-barrier knockout
 - Lookback
 - Arithmetic Asian
 
All options are continuously observed, as this makes
for the most interesting problem mathematically, and
provides the most incentive to do adaptation and multi-level
stuff.

The parameters are again inspired by real-world option
parameters, though in this case it is less clear how
to choose them. There is a reasonable argument for
choosing them equally spaced in some sense, rather
than driven by traded volume or something, as we
don't know what is important to different people.

We need to ensure that prices end up in the "meaningful"
range, so that we don't get prices in the range which
could get rounded to zero, or cause problems with
relative error. I don't know how to define that
right now though :)

Again, the underlyings are fixed, tabulated, and
then made available as a csv.

Workloads
---------

I'm going to arbitrarily pick some numbers: there are
3000 distinct underlyings, and 1000 distinct options.
The workload is formed of 10000 random pairings of
underlyings and options (subject to constraints on
getting a meaningful output). The random pairings are
fixed and part of the benchmark.

Accuracy
--------

The primary accuracy metric is relative error, rather
than absolute error, simply because it is more difficult
to achieve, and makes more sense in the application domain.

There are three accuracy bands:
- Low: tol=0.001 (1e-3)
- Standard: tol=0.0001 (1e-5)
- High: tol=0.0000001 (1e-7)

The intent is that Low is appropriate for quick and
dirty calculations, e.g. real-time risk, Standard is
fine for most day-to-day purposes, and High is really
only of academic interest to show that a method can
scale to high accuracies.

(In order for this to meaningful, that means that we
need to have reference prices for all tasks in the
workload that are accurate down to around 1e-8.
That may actually be infeasible, but it would be
interesting if it were a spur or a challenge to
people.)

Accuracy over a work-load is defined in terms of
RMSE. If there is a work-load of $n$ items, and
$e_i$ and $o_i$ are the observed and expected
prices, then in order to meet a given accuracy
band we must have _both_ of:

sqrt( sum( ((e_i-o_i)/e_i)^2, i=1..n) / n ) <= tol

and:

max( (e_i-o_i)/e_i, i=1..n ) <= 4*tol

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

Performance
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
