import numpy
import zfit
import os
import matplotlib.pyplot as plt

from logzero     import logger  as log
from zutils.plot import plot    as zfp
from scipy.stats import poisson

#----------------------------------------------------
class model:
    def __init__(self, rk=1, preffix='', d_eff=None, d_mcmu=None, d_mcsg=None):
        self._obs    = zfit.Space('x', limits=(4800, 6000))
        self._rk     = rk
        self._preffix= preffix
        self._d_eff  = d_eff 
        self._d_mcmu = d_mcmu
        self._d_mcsg = d_mcsg

        zfit.settings.changed_warnings.hesse_name = False

        self._l_dset      = None
        self._d_mod       = None
        self._out_dir     = None
        self._initialized = False
    #----------------------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        same_keys = self._d_eff.keys() == self._d_mcmu.keys() == self._d_mcsg.keys()
        if not same_keys:
            log.error(f'Input dictionaries have different keys')
            raise ValueError

        self._l_dset = self._d_eff.keys()

        self._initialized = True
    #----------------------------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot create: {value}')
            raise

        self._out_dir = value
        log.debug(f'Using output directory: {self._out_dir}')
    #----------------------------------------------------
    def _get_data_simple(self, nentries, ds, chan):
        nentries = int(nentries)

        ind = 0 if chan == 'mm' else 1
        mu  = self._d_dtmu[ds][ind]
        sg  = self._d_dtsg[ds][ind]

        arr_sig = numpy.random.normal(size=nentries, loc=mu, scale=sg)
        arr_bkg = numpy.random.exponential(size=10 * nentries, scale=5000)
    
        arr_dat = numpy.concatenate([arr_sig, arr_bkg])
    
        return arr_dat
    #----------------------------------------------------
    def _get_peak_pars(self, preffix, mu_mc=None, sg_mc=None):
        sim_mu = zfit.param.ConstantParameter(f'sim_mu_{preffix}', mu_mc)
        sim_sg = zfit.param.ConstantParameter(f'sim_sg_{preffix}', sg_mc)

        dmu     = zfit.Parameter(f'dmu_{preffix}', 0., -50,  50)
        rsg     = zfit.Parameter(f'rsg_{preffix}', 1., 0.0, 2.0)

        dat_mu = zfit.ComposedParameter(f'dat_mu_{preffix}', 
                                        lambda d_par : d_par['dmu'] + d_par[f'sim_mu_{preffix}'], 
                                        {'dmu' : dmu, f'sim_mu_{preffix}' : sim_mu} )
        dat_sg = zfit.ComposedParameter(f'dat_sg_{preffix}', 
                                        lambda d_par : d_par['rsg'] * d_par[f'sim_sg_{preffix}'], 
                                        {'rsg' : rsg, f'sim_sg_{preffix}' : sim_sg} )

        return dat_mu, dat_sg
    #----------------------------------------------------
    def _get_gauss(self, preffix='', mu_mc=None, sg_mc=None):
        preffix= f'{preffix}_{self._preffix}'
        mu, sg = self._get_peak_pars(preffix, mu_mc=mu_mc, sg_mc=sg_mc)
        gauss  = zfit.pdf.Gauss(obs=self._obs, mu=mu, sigma=sg)
        nsg    = zfit.Parameter(f'nsg_{preffix}', 10, 0, 100000)
        esig   = gauss.create_extended(nsg)
    
        lb     = zfit.Parameter(f'lb_{preffix}', -0.0005,  -0.001, 0.00)
        exp    = zfit.pdf.Exponential(obs=self._obs, lam=lb)
        nbk    = zfit.Parameter(f'nbk_{preffix}', 10, 0, 100000)
        ebkg   = exp.create_extended(nbk)
    
        pdf    = zfit.pdf.SumPDF([esig, ebkg]) 
    
        return pdf 
    #----------------------------------------------------
    def _get_ds_model(self, ds):
        mu_mc_mm, mu_mc_ee = self._d_mcmu[ds]
        sg_mc_mm, sg_mc_ee = self._d_mcsg[ds]

        self._pdf_mm = self._get_gauss(preffix=f'mm_{ds}', mu_mc=mu_mc_mm, sg_mc=sg_mc_mm)
        self._pdf_ee = self._get_gauss(preffix=f'ee_{ds}', mu_mc=mu_mc_ee, sg_mc=sg_mc_ee)
    
        return self._pdf_mm, self._pdf_ee
    #----------------------------------------------------
    def _get_ds_data(self, nentries, ds):
        nentries_mm = poisson.rvs(nentries, size=1)[0]
        nentries_ee = poisson.rvs(nentries, size=1)[0]

        arr_mm      = self._get_data_simple(self._rk * nentries_mm, ds, 'mm')
        arr_ee      = self._get_data_simple(           nentries_ee, ds, 'ee')

        eff_mm, eff_ee = self._d_eff[ds]

        arr_flg_mm  = numpy.random.binomial(1, eff_mm, arr_mm.shape[0]) == 1
        arr_flg_ee  = numpy.random.binomial(1, eff_ee, arr_ee.shape[0]) == 1
    
        arr_mm      = arr_mm[arr_flg_mm] 
        arr_ee      = arr_ee[arr_flg_ee] 
        
        dst_mm = zfit.Data.from_numpy(obs=self._obs, array=arr_mm)
        dst_ee = zfit.Data.from_numpy(obs=self._obs, array=arr_ee)
    
        return dst_mm, dst_ee
    #----------------------------------------------------
    def _plot_model(self, key, mod):
        if self._out_dir is None:
            return

        plt_dir = f'{self._out_dir}/plots/models'
        os.makedirs(plt_dir, exist_ok=True)

        obj= zfp(data=mod.create_sampler(n=10000), model=mod)
        obj.plot(nbins=50, ext_text=key)

        log.info(f'Saving to: {plt_dir}/{key}.png')
        plt.savefig(f'{plt_dir}/{key}.png')
        plt.close('all')
    #----------------------------------------------------
    def _plot_data(self, key, dat):
        if self._out_dir is None:
            return

        plt_dir = f'{self._out_dir}/plots/data'
        os.makedirs(plt_dir, exist_ok=True)

        arr_dat = dat.value().numpy()

        plt.hist(arr_dat, bins=50)

        log.info(f'Saving to: {plt_dir}/{key}.png')
        plt.title(f'{key}; {dat.name}')
        plt.savefig(f'{plt_dir}/{key}.png')
        plt.close('all')
    #----------------------------------------------------
    def get_model(self):
        self._initialize()
        if self._d_mod is not None:
            return self._d_mod
    
        d_mod       = {}
        if self._d_eff is None:
            d_mod['d1'] = self._get_ds_model('d1')
            d_mod['d2'] = self._get_ds_model('d2')
            d_mod['d3'] = self._get_ds_model('d3')
            d_mod['d4'] = self._get_ds_model('d4')
        else:
            d_mod       = { ds : self._get_ds_model(ds) for ds in self._l_dset}

        for key, (mod_mm, mod_ee) in d_mod.items():
            self._plot_model(f'{key}_mm', mod_mm)
            self._plot_model(f'{key}_ee', mod_ee)
    
        self._d_mod = d_mod
    
        return self._d_mod
    #----------------------------------------------------
    def get_data(self, d_nent=None, rseed=3, d_dtmu=None, d_dtsg=None):
        self._initialize()

        self._d_dtmu = self._d_mcmu if d_dtmu is None else d_dtmu
        self._d_dtsg = self._d_mcsg if d_dtsg is None else d_dtsg
        if self._d_eff is None:
            log.error(f'No efficiencies found, cannot provide data')
            raise

        numpy.random.seed(seed=rseed)

        d_data     = {}
        dst_mm_tos = None
        for ds, (eff_mm, eff_ee) in self._d_eff.items():
            ds_only    = ds.split('_')[0]
            nentries   = d_nent[ds_only]
            log.debug(f'Dataset: {ds}[{nentries}]')

            dst_mm, dst_ee = self._get_ds_data(nentries, ds)
            if 'TIS' in ds:
                dst_mm     = dst_mm_tos
            else:
                dst_mm_tos = dst_mm

            log.debug(f'Electron data: {dst_ee.numpy().shape[0]}')
            log.debug(f'Muon data: {dst_mm.numpy().shape[0]}')

            d_data[ds]     = dst_mm, dst_ee

        for key, (dat_mm, dat_ee) in d_data.items():
            self._plot_data(f'{key}_mm', dat_mm)
            self._plot_data(f'{key}_ee', dat_ee)
    
        return d_data
    #----------------------------------------------------
    def get_cov(self, kind='diag_eq', c = 0.01):
        self._initialize()

        if   kind == 'diag_eq':
            mat = numpy.diag([c] * 8)
        elif kind == 'random':
            mat = numpy.random.rand(8, 8)
            numpy.fill_diagonal(mat, 1)
            mat = mat * c
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return mat 
    #----------------------------------------------------
    def get_rjpsi(self, kind='one'):
        self._initialize()
        d_rjpsi = {}
    
        if   kind == 'one':
            d_rjpsi['d1'] = 1 
            d_rjpsi['d2'] = 1 
            d_rjpsi['d3'] = 1 
            d_rjpsi['d4'] = 1 
        elif kind == 'eff_bias':
            d_rjpsi['d1'] = 0.83333333 
            d_rjpsi['d2'] = 0.83333333 
            d_rjpsi['d3'] = 0.83333333 
            d_rjpsi['d4'] = 0.83333333 
        else:
            log.error(f'Wrong kind: {kind}')
            raise
    
        return d_rjpsi
    #----------------------------------------------------
    @staticmethod
    def get_eff(kind='equal'):
        d_eff = {}
        if   kind == 'diff':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.5, 0.2)
            d_eff['d3'] = (0.7, 0.3)
            d_eff['d4'] = (0.8, 0.4)
        elif kind == 'half':
            d_eff['d1'] = (0.6, 0.3)
            d_eff['d2'] = (0.6, 0.3)
            d_eff['d3'] = (0.6, 0.3)
            d_eff['d4'] = (0.6, 0.3)
        elif kind == 'equal':
            d_eff['d1'] = (0.3, 0.3)
            d_eff['d2'] = (0.3, 0.3)
            d_eff['d3'] = (0.3, 0.3)
            d_eff['d4'] = (0.3, 0.3)
        elif kind == 'bias':
            d_eff['d1'] = (0.6, 0.25)
            d_eff['d2'] = (0.6, 0.25)
            d_eff['d3'] = (0.6, 0.25)
            d_eff['d4'] = (0.6, 0.25)
        else:
            log.error(f'Invalid kind: {kind}')
            raise
    
        return d_eff
#----------------------------------------------------

