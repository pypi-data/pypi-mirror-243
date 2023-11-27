from extractor import extractor as ext

import os
import numpy
import zfit
import math
import pprint
import pytest
import utils_noroot as utnr
import rk.utilities as rkut

from logzero    import logger    as log
from np_reader  import np_reader as np_rdr
from mc_reader  import mc_reader as mc_rdr
from cs_reader  import cs_reader as cs_rdr
from rkex_model import model

#-----------------------------
def skip_test():
    try:
        uname = os.environ['USER']
    except:
        pytest.skip()

    if uname in ['angelc', 'campoverde']:
        return
#----------------------------------------------------
def check_close(value, target, abs_tol=1e-4):
    pas_val = math.isclose(value, target, abs_tol = abs_tol)
    if not pas_val:
        log.error(f'{value:.6f} != {target:.6f}')
        raise
#----------------------------------------------------
def test_simple():
    log.info('Running: test_simple')
    d_eff       = model.get_eff()
    d_yld       = {'d1' : 2e3, 'd2' : 2e3, 'd3' : 2e3, 'd4' : 2e3} 
    d_mcmu      = {'d1' :   (50, 49), 'd2' :   (51, 49), 'd3' :   (51, 48), 'd4' :   (52, 51)}
    d_mcsg      = {'d1' :    (2,  4), 'd2' :   (1, 1.8), 'd3' :     (2, 3), 'd4' :     (3, 4)} 

    mod         = model(preffix='simple', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    d_dat       = mod.get_data(d_nent=d_yld)
    d_mod       = mod.get_model()

    obj         = ext()
    obj.eff     = d_eff 
    obj.data    = d_dat
    obj.model   = d_mod 
    obj.plt_dir = 'tests/extractor/simple'

    result      = obj.get_fit_result()
    result.hesse()

    d_rk   = result.params['rk']
    rk_val = d_rk['value']
    rk_err = d_rk['hesse']['error']
#----------------------------------------------------
def test_efficiency():
    log.info('Running: test_efficiency')
    d_eff        = model.get_eff(kind='diff')
    d_yld        = {'d1' : 2e3, 'd2' : 2e3, 'd3' : 2e3, 'd4' : 2e3} 
    d_mcmu       = {'d1' :   (50, 49), 'd2' :   (51, 49), 'd3' :   (51, 48), 'd4' :   (52, 51)}
    d_mcsg       = {'d1' :    (2,  4), 'd2' :   (1, 1.8), 'd3' :     (2, 3), 'd4' :     (3, 4)} 

    mod          = model(preffix='efficiency', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    d_dat        = mod.get_data(d_nent=d_yld)
    d_mod        = mod.get_model()

    obj          = ext()
    obj.eff      = d_eff 
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.plt_dir  = 'tests/extractor/efficiency'

    result       = obj.get_fit_result()
    result.hesse()

    d_rk   = result.params['rk']
    rk_val = d_rk['value']
    rk_err = d_rk['hesse']['error']
#----------------------------------------------------
def test_constraint():
    log.info('Running: test_constraint')
    d_eff        = model.get_eff(kind='half')
    d_yld        = {'d1' : 2e3, 'd2' : 2e3, 'd3' : 2e3, 'd4' : 2e3} 
    d_mcmu       = {'d1' :   (50, 49), 'd2' :   (51, 49), 'd3' :   (51, 48), 'd4' :   (52, 51)}
    d_mcsg       = {'d1' :    (2,  4), 'd2' :   (1, 1.8), 'd3' :     (2, 3), 'd4' :     (3, 4)} 

    mod          = model(preffix='constraint', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    cvmat        = mod.get_cov(kind='diag_eq', c=0.001)
    d_dat        = mod.get_data(d_nent=d_yld)
    d_mod        = mod.get_model()

    obj          = ext()
    obj.eff      = d_eff 
    obj.cov      = cvmat
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.plt_dir  = 'tests/extractor/constraint'

    result       = obj.get_fit_result()

    result.hesse()

    d_rk   = result.params['rk']
    rk_val = d_rk['value']
    rk_err = d_rk['hesse']['error']
#----------------------------------------------------
def test_rjpsi():
    log.info('Running: test_rjpsi')
    d_eff        = model.get_eff(kind='half')
    d_yld        = {'d1' : 2e3, 'd2' : 2e3, 'd3' : 2e3, 'd4' : 2e3} 
    d_mcmu       = {'d1' :   (50, 49), 'd2' :   (51, 49), 'd3' :   (51, 48), 'd4' :   (52, 51)}
    d_mcsg       = {'d1' :    (2,  4), 'd2' :   (1, 1.8), 'd3' :     (2, 3), 'd4' :     (3, 4)} 

    mod          = model(preffix='rjpsi', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    cvmat        = mod.get_cov(kind='diag_eq', c=0.001)
    d_rjpsi      = mod.get_rjpsi(kind='eff_bias')
    d_dat        = mod.get_data(d_nent=d_yld)
    d_mod        = mod.get_model()

    obj          = ext()
    obj.rjpsi    = d_rjpsi
    obj.eff      = d_eff
    obj.cov      = cvmat
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.plt_dir  = 'tests/rk_extractor/rjpsi'

    result       = obj.get_fit_result()

    result.hesse()

    d_rk   = result.params['rk']
    rk_val = d_rk['value']
    rk_err = d_rk['hesse']['error']
#----------------------------------------------------
def test_real():
    skip_test()
    log.info('Running: test_real')

    rdr          = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache    = True
    cv_sys       = rdr.get_cov(kind='sys')
    cv_sta       = rdr.get_cov(kind='sta')
    d_eff        = rdr.get_eff()
    d_rjpsi      = rdr.get_rjpsi()
    d_byld       = rdr.get_byields()
    d_nent       = rkut.average_byields(d_byld, l_exclude=['TIS'])
    d_rare_yld   = rkut.reso_to_rare(d_nent, kind='jpsi')

    rdr          = mc_rdr(version='v4')
    rdr.cache    = False
    d_mcmu       = rdr.get_parameter(name='mu')
    d_mcsg       = rdr.get_parameter(name='sg')

    mod          = model(preffix='real', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    #mod.out_dir  = 'tests/extractor/real/model'
    d_mod        = mod.get_model()
    d_dat        = mod.get_data(d_nent=d_rare_yld)

    obj          = ext()
    obj.rjpsi    = d_rjpsi
    obj.eff      = d_eff
    obj.cov      = cv_sys + cv_sta
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.plt_dir  = 'tests/rk_extractor/real'
    result       = obj.get_fit_result()

    log.info(f'Calculating errors')
    result.hesse()
    result.freeze()
    utnr.dump_pickle(result, 'tests/rk_extractor/real/result.pkl')
#----------------------------------------------------
def test_real_const():
    skip_test()
    log.info('Running: test_const')

    rdr          = cs_rdr(version='v4', preffix='const')
    d_val, d_var = rdr.get_constraints()

    rdr          = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache    = True
    cv_sys       = rdr.get_cov(kind='sys')
    cv_sta       = rdr.get_cov(kind='sta')
    d_eff        = rdr.get_eff()
    d_rjpsi      = rdr.get_rjpsi()
    d_byld       = rdr.get_byields()
    d_nent       = rkut.average_byields(d_byld, l_exclude=['TIS'])
    d_rare_yld   = rkut.reso_to_rare(d_nent, kind='jpsi')

    rdr          = mc_rdr(version='v4')
    rdr.cache    = False
    d_mcmu       = rdr.get_parameter(name='mu')
    d_mcsg       = rdr.get_parameter(name='sg')

    mod          = model(preffix='const', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    d_mod        = mod.get_model()
    d_dat        = mod.get_data(d_nent=d_rare_yld)

    obj          = ext()
    obj.rjpsi    = d_rjpsi
    obj.eff      = d_eff
    obj.cov      = cv_sys + cv_sta
    obj.data     = d_dat
    obj.model    = d_mod 
    obj.const    = d_val, d_var
    obj.plt_dir  = 'tests/rk_extractor/const'
    result       = obj.get_fit_result()

    log.info(f'Calculating errors')
    result.hesse()
    result.freeze()
    utnr.dump_pickle(result, 'tests/rk_extractor/const/result.pkl')
#----------------------------------------------------
def test_real_const_dset():
    skip_test()
    log.info('Running: test_dset')

    rdr          = cs_rdr(version='v4', preffix='dset')
    rdr.cache_dir= 'tests/rk_extractor/real_const_dset/cs_reader'
    d_val, d_var = rdr.get_constraints()

    rdr          = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache    = True
    rdr.cache_dir= 'tests/rk_extractor/real_const_dset/np_reader'
    cv_sys       = rdr.get_cov(kind='sys')
    cv_sta       = rdr.get_cov(kind='sta')
    d_eff        = rdr.get_eff()
    d_rjpsi      = rdr.get_rjpsi()
    d_byld       = rdr.get_byields()
    d_nent       = rkut.average_byields(d_byld, l_exclude=['TIS'])
    d_rare_yld   = rkut.reso_to_rare(d_nent, kind='jpsi')

    rdr          = mc_rdr(version='v4')
    rdr.cache    = False
    rdr.cache_dir= 'tests/rk_extractor/real_const_dset/mc_reader'
    d_mcmu       = rdr.get_parameter(name='mu')
    d_mcsg       = rdr.get_parameter(name='sg')

    mod          = model(preffix='dset', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg)
    d_mod        = mod.get_model()
    d_dat        = mod.get_data(d_nent=d_rare_yld)

    obj          = ext(dset=['2018_TOS'])
    obj.cov      = cv_sys + cv_sta
    obj.const    = d_val, d_var
    obj.model    = d_mod 
    obj.eff      = d_eff
    obj.data     = d_dat
    obj.rjpsi    = d_rjpsi
    obj.plt_dir  = 'tests/rk_extractor/dset'
    result       = obj.get_fit_result()

    log.info(f'Calculating errors')
    result.hesse()
    result.freeze()
    utnr.dump_pickle(result, 'tests/rk_extractor/dset/result.pkl')
#----------------------------------------------------
def main():
    utnr.timer_on=True
    test_real_const_dset()
    test_real_const()
    test_real()
    test_simple()
    test_rjpsi()
    test_constraint()
    test_efficiency()
#----------------------------------------------------
if __name__ == '__main__':
    main()

