RTTA
======================

Purpose
-------

The purpose of this package is to implement a very low latency
incremental technical analysis toolkit.  Most technical analysis
tool-kits work in a "batch mode" where you hand them a blob of data and
in a pandas series and they return a series with the computed data.
Incremental updates for these require O(n) work.  There is one tool,
[talipp](https://pypi.org/project/talipp/) that is designed to support
incremental updates, but it is implemented in pure python and is a
little more than an order of magnitude slower than rtta.  On a 5995WX
talipp's exponential moving average requires 465ns; rtta's requires
36ns.  A bare python function call requires 35ns, so we're about as
fast as fast can be.

Installation
------------

### From a repository checkout

Installation is still a little bit rough.  We use cython and compile
against numpy so you have to have both installed just to perform a pip
install from source.  In the coming days I'll upload binary packages
for everything, but for now here's how you build the package.

```bash
pip install -U numpy cython
git clone git@github.com:adamdeprince/rtta.git
cd rtta
pip install -U . 
```

We'll figure out how to make this pypi install-able in a few days. 
