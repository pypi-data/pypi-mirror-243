<h1>TTiME</h1>
<h2>Tensor Trains in Mathematics and Engineering	</h2>

This package was developed as part of my master's thesis at the École Polytechnique Fédérale de Lausanne and the University of Tokyo.
It provides tools for handling and creating tensors in the Tensor Train (TT) format.
Additionally, it implements the method of low-rank Chebyshev interpolation, which allows for tensorized Chebyshev interpolation with small amounts of data.

The code in this package is based on the work published in the following three papers, which are also referenced throughout the code:

1. I. Oseledets. “Tensor-Train Decomposition”. In: SIAM Journal on Scientific Computing
33 (5 Jan. 2011), pp. 2295–2317. DOI: 10.1137/090752286
2. M. Steinlechner. “Riemannian Optimization for High-Dimensional Tensor Completion”.
In: SIAM Journal on Scientific Computing 38 (5 2016), A2611–S799. DOI: 10.1137/
15M1010506
3. K. Glau, D. Kressner, and F. Statti. “Low-Rank Tensor Approximation for Chebyshev
Interpolation in Parametric Option Pricing”. In: SIAM Journal on Financial Mathematics
11 (3 2020), pp. 897–927. DOI: 10.1137/19M1244172

To get going with the code, simply use 'pip install ttime' in a terminal and afterwards 'import ttime' in your Python file. For questions, please feel free to reach out to me at ttime.python@gmail.com