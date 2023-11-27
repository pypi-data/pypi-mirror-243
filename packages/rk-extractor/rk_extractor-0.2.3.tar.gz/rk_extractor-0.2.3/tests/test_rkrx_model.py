from rkex_model import model
from mc_reader  import mc_reader as mc_rdr
from np_reader  import np_reader as np_rdr

import rk.utilities as rkut
import pytest
import pprint
import os

#-----------------------------
def skip_test():
    try:
        uname = os.environ['USER']
    except:
        pytest.skip()

    if uname in ['angelc', 'campoverde']:
        return

    pytest.skip()
#----------------------
def test_simple():
    d_eff = {'d1' : (0.5, 0.4), 'd2' : (0.4, 0.3), 'd3' : (0.3, 0.2), 'd4' : (0.2, 0.1)}
    d_nent= {'d1' :        1e4, 'd2' :        1e4, 'd3' :        1e4, 'd4' :        1e4}
    d_mcmu= {'d1' :   (50, 49), 'd2' :   (51, 49), 'd3' :   (51, 48), 'd4' :   (52, 51)}
    d_mcsg= {'d1' :    (2,  4), 'd2' :   (1, 1.8), 'd3' :     (2, 3), 'd4' :     (3, 4)}

    mod         = model(preffix='simple', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    mod.out_dir = 'tests/rkex_model/simple' 
    d_dat       = mod.get_data(d_nent=d_nent)
    d_mod       = mod.get_model()
#----------------------
def test_real():
    skip_test()

    rdr           = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache     = True 
    rdr.cache_dir = 'tests/np_reader/cache'
    d_eff         = rdr.get_eff()
    d_byld        = rdr.get_byields()
    d_byld_avg    = rkut.average_byields(d_byld, l_exclude=['TIS'])
    d_rare_yld    = rkut.reso_to_rare(d_byld_avg, kind='jpsi')

    rdr           = mc_rdr(version='v4')
    rdr.cache     = False 
    d_mcmu        = rdr.get_parameter(name='mu')
    d_mcsg        = rdr.get_parameter(name='sg')

    mod           = model(preffix='real', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    mod.out_dir   = 'tests/rkex_model/real' 
    d_dat         = mod.get_data(d_nent=d_rare_yld)
    d_mod         = mod.get_model()
#----------------------
def main():
    test_real()
    test_simple()
#----------------------
if __name__ == '__main__':
    main()

