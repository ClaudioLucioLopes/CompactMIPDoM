# Compact MIP-DoM

Dominance move (DoM) is a binary quality indicator that can be used in multi-objective and many-objective optimization to compare two solution sets obtained from different simulations. The DoM indicator can differentiate the sets for certain important features, such as convergence, spread, uniformity, and cardinality. DoM does not require any reference point or any representative Pareto solution set, and it has an intuitive and physical meaning, similar to the -indicator. It calculates the minimum total move of members of one set so that all elements in another set are to be dominated or identical to at least one member of the first set. 

This code is the implementation of our compact Mixed Integer Programming model to solve DoM, as describe in  

## Installation

As we need  mixed-integer solver, it is possible to use CBC or Gurobi.
CBC or Gurobi will work with [Python-MIP](https://www.python-mip.com/)
You can install [Python-MIP]
```
pip install mip --user
```

You can use CBC, it is our default solver: [CBC User’s Guide](https://coin-or.github.io/Cbc/)

You can install Gurobi, please, follow this link: [Installing Gurobi Solver](http://matthiaswalter.org/intpm/Gurobi-Python3-Howto.pdf)



## Usage

```python
import CompactMIPDoM as md
from numpy import genfromtxt

if __name__ == '__main__':
  P = genfromtxt('data/car1(A).txt', delimiter='\t')
  Q = genfromtxt('data/car1(B).txt', delimiter='\t')
  print(md.get_dom_mip_improved(P, Q, logprint=True, gapperc=1e-06))
  mip_dom_value, p_index, p_lines = md.get_dom_mip_improved(Q, P, logprint=True, gapperc=1e-06)
  assert (str(
    p_lines) == '[array([1.08769, 0.1    ]), array([1.039693, 0.40902 ]), array([0.966025, 0.55399 ]), array([0.866044, 0.68778 ]), array([0.68778, 0.80711]), array([0.55399 , 0.966025]), array([0.40902 , 1.039693]), array([0.1    , 1.08769])]')
  assert (mip_dom_value == 0.35159000004315755)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Citing This Work
You can cite this code as follows:

### Bibtex



## License
[MIT](https://choosealicense.com/licenses/mit/)