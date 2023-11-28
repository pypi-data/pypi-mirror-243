from np_reader import np_reader as np_rdr
import pprint
import pytest
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
#-----------------------------
def test_simple():
    skip_test()
    rdr       = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache = True
    d_rjpsi   = rdr.get_rjpsi()
    d_eff     = rdr.get_eff()
    cov_sys   = rdr.get_cov(kind='sys')
    cov_sta   = rdr.get_cov(kind='sta')
    d_byld    = rdr.get_byields()
#-----------------------------
def test_tarball():
    skip_test()
    rdr           = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache     = True
    rdr.cache_dir = 'tests/np_reader/tarball'
    d_rjpsi       = rdr.get_rjpsi()
    d_eff         = rdr.get_eff()
    cov_sys       = rdr.get_cov(kind='sys')
    cov_sta       = rdr.get_cov(kind='sta')
    d_byld        = rdr.get_byields()
#-----------------------------
def test_cache():
    skip_test()
    rdr           = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache     = False 
    rdr.cache_dir = 'tests/np_reader/cache'
    d_rjpsi       = rdr.get_rjpsi()
    d_eff         = rdr.get_eff()
    cov_sys       = rdr.get_cov(kind='sys')
    cov_sta       = rdr.get_cov(kind='sta')
    d_byld        = rdr.get_byields()
#-----------------------------
def main():
    test_simple()
    test_tarball()
    test_cache()
#-----------------------------
if __name__ == '__main__':
    main()

