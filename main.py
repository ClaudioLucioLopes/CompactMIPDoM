import CompactMIPDoM as md
from numpy import genfromtxt

if __name__ == '__main__':
    P = genfromtxt('data/car1(A).txt', delimiter='\t')
    Q = genfromtxt('data/car1(B).txt', delimiter='\t')
    print(md.get_dom_mip_improved(P, Q, logprint=True, gapperc=1e-06))
    mip_dom_value,p_index, p_lines = md.get_dom_mip_improved(Q, P, logprint=True, gapperc=1e-06)
    assert(str(p_lines)=='[array([1.08769, 0.1    ]), array([1.039693, 0.40902 ]), array([0.966025, 0.55399 ]), array([0.866044, 0.68778 ]), array([0.68778, 0.80711]), array([0.55399 , 0.966025]), array([0.40902 , 1.039693]), array([0.1    , 1.08769])]')
    assert(mip_dom_value==0.35159000004315755)