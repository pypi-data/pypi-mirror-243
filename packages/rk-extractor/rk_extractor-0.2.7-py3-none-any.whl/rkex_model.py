import numpy
import zfit
import re
import os
import matplotlib.pyplot as plt

from logzero     import logger  as log
from zutils.plot import plot    as zfp
from scipy.stats import poisson

#----------------------------------------------------
class model:
    def __init__(self, rk=1, preffix='', d_eff=None, d_mcmu=None, d_mcsg=None, d_dtmu=None, d_dtsg=None, d_nent=None):
        '''
        Parameters
        -----------------------
        d_mcmu (dict): Stores mean, measured in MC from resonant mode for muon and electron, e.g. {r1 : (5279, 5270)}
        d_mcsg (dict): Stores width, measured in MC from resonant mode for muon and electron, e.g. {r1 : (10, 20)}
        d_dtmu (dict): Stores mean, measured in data from resonant mode for muon and electron, e.g. {r1 : (5279, 5270)}, if not passed, use MC one
        d_dtsg (dict): Stores width, measured in data from resonant mode for muon and electron, e.g. {r1 : (10, 20)}, if not passed, use MC one
        d_nent (dict): Stores number of B -> llK entries, before selection, e.g. {r1 : 23235}
        '''
        self._obs    = zfit.Space('x', limits=(4800, 6000))
        self._rk     = rk
        self._preffix= preffix
        self._d_eff  = d_eff 
        self._d_mcmu = d_mcmu
        self._d_mcsg = d_mcsg
        self._d_dtmu = self._d_mcmu if d_dtmu is None else d_dtmu
        self._d_dtsg = self._d_mcsg if d_dtsg is None else d_dtsg
        self._d_nent = d_nent

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

        if self._d_eff is None:
            log.error(f'No efficiencies found, cannot provide data')
            raise

        if self._d_nent is None:
            log.error(f'No B-> Jpsi K yields found')
            raise

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
    def _get_peak_pars(self, preffix, mu=None, sg=None):
        mu_dt, mu_mc = mu
        sg_dt, sg_mc = sg

        sim_mu = zfit.param.ConstantParameter(f'sim_mu_{preffix}', mu_mc)
        sim_sg = zfit.param.ConstantParameter(f'sim_sg_{preffix}', sg_mc)

        dmu     = zfit.Parameter(f'dmu_{preffix}', mu_dt - mu_mc, -50,  50)
        rsg     = zfit.Parameter(f'rsg_{preffix}', sg_dt / sg_mc, 0.0, 3.0)

        dat_mu = zfit.ComposedParameter(f'dat_mu_{preffix}', 
                                        lambda d_par : d_par['dmu'] + d_par[f'sim_mu_{preffix}'], 
                                        {'dmu' : dmu, f'sim_mu_{preffix}' : sim_mu} )
        dat_sg = zfit.ComposedParameter(f'dat_sg_{preffix}', 
                                        lambda d_par : d_par['rsg'] * d_par[f'sim_sg_{preffix}'], 
                                        {'rsg' : rsg, f'sim_sg_{preffix}' : sim_sg} )

        return dat_mu, dat_sg
    #----------------------------------------------------
    def _get_pdf(self, preffix='', mu=None, sg=None, nent=None):
        preffix= f'{preffix}_{self._preffix}'
        mu, sg = self._get_peak_pars(preffix, mu=mu, sg=sg)

        gauss  = zfit.pdf.Gauss(obs=self._obs, mu=mu, sigma=sg)
        nsg    = zfit.Parameter(f'nsg_{preffix}', nent, 0, 100000)
        esig   = gauss.create_extended(nsg)
    
        lb     = zfit.Parameter(f'lb_{preffix}', -0.0005,  -0.001, 0.00)
        exp    = zfit.pdf.Exponential(obs=self._obs, lam=lb)
        nbk    = zfit.Parameter(f'nbk_{preffix}', 10 * nent, 0, 100000)
        ebkg   = exp.create_extended(nbk)
    
        pdf    = zfit.pdf.SumPDF([esig, ebkg]) 
    
        return pdf 
    #----------------------------------------------------
    def _get_ds_model(self, ds, nent_mm, nent_ee):
        mu_mc_mm, mu_mc_ee = self._d_mcmu[ds]
        sg_mc_mm, sg_mc_ee = self._d_mcsg[ds]

        mu_dt_mm, mu_dt_ee = self._d_dtmu[ds]
        sg_dt_mm, sg_dt_ee = self._d_dtsg[ds]

        mu_mm = mu_dt_mm, mu_mc_mm
        sg_mm = sg_dt_mm, sg_mc_mm

        mu_ee = mu_dt_ee, mu_mc_ee
        sg_ee = sg_dt_ee, sg_mc_ee

        self._pdf_mm = self._get_pdf(preffix=f'mm_{ds}', mu=mu_mm, sg=sg_mm, nent=nent_mm)
        self._pdf_ee = self._get_pdf(preffix=f'ee_{ds}', mu=mu_ee, sg=sg_ee, nent=nent_ee)
    
        return self._pdf_mm, self._pdf_ee
    #----------------------------------------------------
    def _plot_model(self, key, mod):
        if self._out_dir is None:
            return

        plt_dir = f'{self._out_dir}/plots/models'
        os.makedirs(plt_dir, exist_ok=True)

        obj= zfp(data=mod.create_sampler(), model=mod)
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
    def _get_selected_entries(self):
        d_nent_sel = {}

        for ds in self._l_dset:
            ds_only = ds.split('_')[0]
            nent    = self._d_nent[ds_only]

            eff_mm, eff_ee = self._d_eff[ds]
            d_nent_sel[ds] = self._rk * nent * eff_mm, nent * eff_ee 

        return d_nent_sel
    #----------------------------------------------------
    def get_model(self):
        '''
        Returns
        -----------------
        d_ent (dict): Returns a dictionary: {name : tup} where
            name (str)  : model identifier, e.g. r1_ETOS
            tup  (tuple): Tuple with muon and electron PDFs, e.g. pdf_mm, pdf_ee 

        For muon, TIS model is the TOS one.
        '''
        self._initialize()
        if self._d_mod is not None:
            return self._d_mod

        d_nent_sel = self._get_selected_entries()
        d_mod      = {}

        mod_mm_tos = None
        for ds, (nent_mm, nent_ee) in d_nent_sel.items():
            mod_mm, mod_ee = self._get_ds_model(ds, nent_mm, nent_ee)
            if 'TIS' in ds:
                mod_mm = mod_mm_tos
            else:
                mod_mm_tos = mod_mm

            d_mod[ds]      = mod_mm, mod_ee

            self._plot_model(f'{ds}_mm', mod_mm)
            self._plot_model(f'{ds}_ee', mod_ee)
    
        self._d_mod = d_mod
    
        return self._d_mod
    #----------------------------------------------------
    def _add_ck(self, d_par):
        regex='nsg_ee_([0-9a-z]+_(TIS|TOS)_.*)'
        d_par_ck = {}
        for var_name in d_par:
            mtch = re.match(regex, var_name)
            if not mtch:
                continue

            suffix = mtch.group(1)

            ee_yld_name = var_name
            mm_yld_name = var_name.replace('_ee_', '_mm_').replace('_TIS_', '_TOS_')

            ee_yld, _   = d_par[ee_yld_name]
            mm_yld, _   = d_par[mm_yld_name]

            d_par_ck[f'ck_{suffix}'] = (self._rk * ee_yld) / mm_yld

        d_par.update(d_par_ck)

        return d_par
    #----------------------------------------------------
    def get_prefit_pars(self):
        '''
        Used to get model parameters used to make the toy data
        '''
        self._initialize()

        d_model = self.get_model()

        d_par = {}
        for mod_mm, mod_ee in d_model.values():
            d_par_mm = { par.name : [ par.value().numpy(), 0] for par in mod_mm.get_params() }
            d_par_ee = { par.name : [ par.value().numpy(), 0] for par in mod_ee.get_params() }

            d_par.update(d_par_ee)
            d_par.update(d_par_mm)

        d_par['rk'] = [self._rk, 0]
        d_par       = self._add_ck(d_par)

        return d_par
    #----------------------------------------------------
    def get_data(self, rseed=3):
        '''
        Returns toy data from model

        Parameters:
        -----------------
        rseed  (int):  Random seed

        Returns:
        -----------------
        d_data (dict): Dictionary with dataset and tuple of zfit data objects paired, i.e. {r1_TOS : (pdf_mm, pdf_ee) }

        For muon, TIS dataset is the TOS one.
        '''
        self._initialize()

        d_model    = self.get_model()
        d_data     = {}
        dst_mm_tos = None
        for ds, (pdf_mm, pdf_ee) in d_model.items():
            dst_mm         = pdf_mm.create_sampler()
            dst_ee         = pdf_ee.create_sampler()

            if 'TIS' in ds:
                dst_mm = dst_mm_tos
            else:
                dst_mm_tos = dst_mm

            d_data[ds]     = dst_mm, dst_ee

            self._plot_data(f'{ds}_mm', dst_mm)
            self._plot_data(f'{ds}_ee', dst_ee)

            log.debug(f'Electron data: {dst_ee.numpy().shape[0]}')
            log.debug(f'Muon data: {dst_mm.numpy().shape[0]}')

        return d_data
    #----------------------------------------------------
    @staticmethod
    def get_cov(kind='diag_eq', c = 0.01):
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
    @staticmethod
    def get_rjpsi(kind='one'):
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

