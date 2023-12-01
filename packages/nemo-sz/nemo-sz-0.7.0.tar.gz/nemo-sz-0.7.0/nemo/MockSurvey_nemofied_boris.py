"""

This module defines the MockSurvey class, used for mass function calculations, obtaining de-biased cluster
mass estimates, selection function calculations, and generating mock catalogs.

"""

import os
import sys
import numpy as np
import astropy.table as atpy
import pylab as plt
import subprocess
from astropy.cosmology import FlatLambdaCDM
on_rtd=os.environ.get('READTHEDOCS', None)
if on_rtd is None:
    import pyccl as ccl
from . import signals
from . import catalogs
from . import maps
import pickle
from scipy import interpolate
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline as _spline
from scipy import stats
from astLib import *
import time

from classy_sz import Class

common_class_sz_settings = {
                   'mass function' : 'T08M200c', 
                   'hm_consistency': 0,
                   'concentration parameter' : 'B13',
                   'B':1.,

                   'N_ncdm' : 1,
                   'N_ur' : 2.0328,
                   'm_ncdm' : 0.0,
                   'T_ncdm' : 0.71611,
    
                   'z_min': 1.e-3, # chose a wide range 
                   'z_max': 3.05, # chose a wide range 
                   'redshift_epsrel': 1e-6,
                   'redshift_epsabs': 1e-100,  
    
                   'M_min': 1e13, # chose a wide range 
                   'M_max': 1e17, # chose a wide range 
                   'mass_epsrel':1e-6,
                   'mass_epsabs':1e-100,
   
                   'ndim_redshifts' :5000,
                   'ndim_masses' : 500,
                   'n_m_dndlnM' : 1000,
                   'n_z_dndlnM' : 1000,
                   'HMF_prescription_NCDM': 1,
                   'no_spline_in_tinker': 1,
    
    
                   'use_m500c_in_ym_relation' : 0,
                   'use_m200c_in_ym_relation' : 1,
                   'y_m_relation' : 1,
    
                   'output': 'dndlnM,m500c_to_m200c,m200c_to_m500c',
}


#------------------------------------------------------------------------------------------------------------
class MockSurvey(object):
    """An object that provides routines calculating cluster counts (using `CCL <https://ccl.readthedocs.io/en/latest/>`_) 
    and generating mock catalogs for a given set of cosmological and mass scaling relation parameters.
    The Tinker et al. (2008) halo mass function is used (hardcoded at present, but in principle this can
    easily be swapped for any halo mass function supported by CCL).
    
    Attributes:
        areaDeg2 (:obj:`float`): Survey area in square degrees.
        zBinEdges (:obj:`np.ndarray`): Defines the redshift bins for the cluster counts.
        z (:obj:`np.ndarray`): Centers of the redshift bins.
        log10M (:obj:`np.ndarray`): Centers of the log10 mass bins for the cluster counts
            (in MSun, with mass defined according to `delta` and `rhoType`).
        a (:obj:`np.ndarray`): Scale factor (1/(1+z)).
        delta (:obj:``float`): Overdensity parameter, used for mass definition (e.g., 200, 500).
        rhoType (:obj:`str`): Density definition, either 'matter' or 'critical', used for mass definition.
        mdef (:obj:`pyccl.halos.massdef.MassDef`): CCL mass definition object, defined by `delta` and `rhoType`.
        transferFunction (:obj:`str`): Transfer function to use, as understood by CCL (e.g., 'eisenstein_hu', 
            'boltzmann_camb').
        H0 (:obj:`float`): The Hubble constant at redshift 0, in km/s/Mpc.
        Om0 (:obj:`float`): Dimensionless total (dark + baryonic) matter density parameter at redshift 0.
        Ob0 (:obj:`float`): Dimensionless baryon matter density parameter at redshift 0.
        sigma8 (:obj:`float`): Defines the amplitude of the matter power spectrum.
        ns (:obj:`float`): Scalar spectral index of matter power spectrum.
        volumeMpc3 (:obj:`float`): Co-moving volume in Mpc3 for the given survey area and cosmological
            parameters.
        numberDensity (:obj:`np.ndarray`): Number density of clusters (per cubic Mpc) on the 
            (z, log10M) grid.
        clusterCount (:obj:`np.ndarray`): Cluster counts on the (z, log10M) grid.
        numClusters (:obj:`float`): Total number of clusters in the survey area above the minimum mass
            limit.
        numClustersByRedshift (:obj:`np.ndarray`): Number of clusters in the survey area above the
            minimum mass limit, as a function of redshift.
    
    """
    def __init__(self, minMass, maxMass, areaDeg2, zMin, zMax, H0, Om0, Ob0, sigma8, ns, zStep = 0.01,
                 numMassBins = 20000, enableDrawSample = False, delta = 500, rhoType = 'critical',
                 transferFunction = 'boltzmann_camb', massFunction = 'Tinker08',
                 c_m_relation = 'Bhattacharya13'):
        """Create a MockSurvey object, for performing calculations of cluster counts or generating mock
        catalogs. The Tinker et al. (2008) halo mass function is used (hardcoded at present, but in 
        principle this can easily be swapped for any halo mass function supported by CCL).
        
        Args:
            minMass (:obj:`float`): The minimum mass, in MSun. This should be set considerably lower than
                the actual survey completeness limit, otherwise completeness calculations will be wrong.
            areaDeg2 (:obj:`float`): Specifies the survey area in square degrees, which scales the
                resulting cluster counts accordingly.
            zMin (:obj:`float`): Minimum redshift for the (z, log10M) grid.
            zMax (:obj:`float`): Maximum redshift for the (z, log10M) grid.
            H0 (:obj:`float`): The Hubble constant at redshift 0, in km/s/Mpc.
            Om0 (:obj:`float`): Dimensionless total (dark + baryonic) matter density parameter at redshift 0.
            Ob0 (:obj:`float`): Dimensionless baryon matter density parameter at redshift 0.
            sigma8 (:obj:`float`): Defines the amplitude of the matter power spectrum.
            ns (:obj:`float`): Scalar spectral index of matter power spectrum.  
            zStep (:obj:`float`, optional): Sets the linear spacing between redshift bins.
            enableDrawSample (:obj:`bool`, optional): This needs to be set to True to enable use of the
                :func:`self.drawSample` function. Setting this to False avoids some overhead.
            delta (:obj:``float`): Overdensity parameter, used for mass definition (e.g., 200, 500).
            rhoType (:obj:`str`): Density definition, either 'matter' or 'critical', used for mass definition.
            transferFunction (:obj:`str`): Transfer function to use, as understood by CCL (e.g., 'eisenstein_hu', 
                'boltzmann_camb').
            massFunction (:obj:`str`): Name of the mass function to use, currently either 'Tinker08' or
                'Tinker10'. Mass function calculations are done by CCL.
            c_m_relation ('obj':`str`): Name of the concentration -- mass relation to assume, as understood by
                CCL (this may be used internally for conversion between mass definitions, as needed).

        """
        
        if areaDeg2 == 0:
            raise Exception("Cannot create a MockSurvey object with zero area")
        self.areaDeg2=areaDeg2
        self.areaSr=np.radians(np.sqrt(areaDeg2))**2
        self.fsky=self.areaSr/(4*np.pi)

        self.delta=delta
        self.rhoType=rhoType
        self.c_m_relation=c_m_relation
        self.mdef=ccl.halos.MassDef(self.delta, self.rhoType)
        self.transferFunction=transferFunction
        self.massFuncName=massFunction
        
        self.log10M=np.arange(np.log10(minMass), np.log10(maxMass), 0.001)
        
        class_sz_cosmo_params = {
        'Omega_b': Ob0,
        'Omega_cdm':  Om0-Ob0,
        'H0': H0,
        'sigma8': sigma8,
        'tau_reio':  0.0561, ## doesnt matter 
        'n_s': ns,
        }
        
        # tenToA0, B0, Mpivot, sigma_int = [scalingRelationDict['tenToA0'],
        #                                   scalingRelationDict['B0'],
        #                                   scalingRelationDict['Mpivot'],
        #                                   scalingRelationDict['sigma_int']]
        #
        # class_sz_ym_params = {
        # 'A_ym'  : tenToA0,
        # 'B_ym'  : B0,
        # 'C_ym' : 0.,
        # 'sigmaM_ym' : sigma_int,
        # 'm_pivot_ym_[Msun]' : Mpivot,
        # }
        # #BB


        self.cosmo = Class()
        self.cosmo.set(common_class_sz_settings)
        self.cosmo.set(class_sz_cosmo_params)
        # self.cosmo.set(class_sz_ym_params)
        self.cosmo.compute_class_szfast()
        

        zRange=np.arange(zMin, zMax+zStep, zStep)
        self.zBinEdges=zRange
        self.z=(zRange[:-1]+zRange[1:])/2.
        self.a=1./(1+self.z)
        nzs=self.z.shape[0]

        # NOTE: We use MSun, Boris/class-sz uses MSun/h, watch out for that
        self.log10M=np.linspace(np.log10(minMass), np.log10(maxMass), numMassBins)
        self.M=np.power(10, self.log10M)
        self.log10MBinEdges=np.linspace(self.log10M.min()-(self.log10M[1]-self.log10M[0])/2,
                                        self.log10M.max()+(self.log10M[1]-self.log10M[0])/2, len(self.log10M)+1)

        # Below is needed for Q calc when not using M500c definition (for now at least)
        if (self.delta == 500 and self.rhoType == 'critical') == False:
            self._M500cDef=ccl.halos.MassDef(500, "critical")
            self._transToM500c=ccl.halos.mass_translator(mass_in = self.mdef, mass_out = self._M500cDef,
                                                         concentration = self.c_m_relation)

        self.enableDrawSample=enableDrawSample
        self.update(H0, Om0, Ob0, sigma8, ns)
        print("done __init__")


    def update(self, H0, Om0, Ob0, sigma8, ns):
        """Recalculate cluster counts for the updated cosmological parameters given.

        Args:
            H0 (:obj:`float`): The Hubble constant at redshift 0, in km/s/Mpc.
            Om0 (:obj:`float`): Dimensionless total (dark + baryonic) matter density parameter at redshift 0.
            Ob0 (:obj:`float`): Dimensionless baryon matter density parameter at redshift 0.
            sigma8 (:obj:`float`): Defines the amplitude of the matter power spectrum.
            ns (:obj:`float`): Scalar spectral index of matter power spectrum.

        """

        print("in update")
        self._get_new_cosmo(H0, Om0, Ob0, sigma8, ns)

        self._doClusterCount()

        # CCL
        # For quick Q, fRel calc (these are in MockSurvey rather than SelFn as used by drawSample)
#         self.theta500Splines=[]
#         self.fRelSplines=[]
#         self.Ez=ccl.h_over_h0(self.cosmoModel,self.a)
#         self.Ez2=np.power(self.Ez, 2)
#         self.DAz=ccl.angular_diameter_distance(self.cosmoModel,self.a)
#         self.criticalDensity=ccl.physical_constants.RHO_CRITICAL*(self.Ez*self.cosmoModel['h'])**2
#         for k in range(len(self.z)):
#             # NOTE: Q fit uses theta500, as does fRel (hardcoded M500 - T relation in there)
#             # This bit here may not be strictly necessary, since we don't need to map on to binning
#             if self.delta == 500 and self.rhoType == "critical":
#                 interpLim_minLog10M500c=self.log10M.min()
#                 interpLim_maxLog10M500c=self.log10M.max()
#             else:
#                 interpLim_minLog10M500c=np.log10(self._transToM500c(self.cosmoModel, self.M.min(), self.a[k]))
#                 interpLim_maxLog10M500c=np.log10(self._transToM500c(self.cosmoModel, self.M.max(), self.a[k]))
#             zk=self.z[k]
#             interpPoints=100
#             fitM500s=np.power(10, np.linspace(interpLim_minLog10M500c, interpLim_maxLog10M500c, interpPoints))
#             fitTheta500s=np.zeros(len(fitM500s))
#             fitFRels=np.zeros(len(fitM500s))
#             criticalDensity=self.criticalDensity[k]
#             DA=self.DAz[k]
#             Ez=self.Ez[k]
#             R500Mpc=np.power((3*fitM500s)/(4*np.pi*500*criticalDensity), 1.0/3.0)
#             fitTheta500s=np.degrees(np.arctan(R500Mpc/DA))*60.0
#             fitFRels=signals.calcFRel(zk, fitM500s, Ez)
#             tckLog10MToTheta500=interpolate.splrep(np.log10(fitM500s), fitTheta500s)
#             tckLog10MToFRel=interpolate.splrep(np.log10(fitM500s), fitFRels)
#             self.theta500Splines.append(tckLog10MToTheta500)
#             self.fRelSplines.append(tckLog10MToFRel)
#
#         # Stuff to enable us to draw mock samples (see drawSample)
#         # Interpolators here need to be updated each time we change cosmology
#         if self.enableDrawSample == True:
#
#             # For drawing from overall z distribution
#             zSum=self.clusterCount.sum(axis = 1)
#             pz=np.cumsum(zSum)/self.numClusters
#             self.zRoller=_spline(pz, self.z, k = 3)
#
#             # For drawing from each log10M distribution at each point on z grid
#             # And quick fRel, Q calc using interpolation
#             # And we may as well have E(z), DA on the z grid also
#             self.log10MRollers=[]
#             for i in range(len(self.z)):
#                 ngtm=self._cumulativeNumberDensity(self.z[i])
#                 mask=ngtm > 0
#                 self.log10MRollers.append(_spline((ngtm[mask] / ngtm[0])[::-1], np.log10(self.M[mask][::-1]), k=3))


    def _get_new_cosmo(self, H0, Om0, Ob0, sigma8, ns):
        pass
        # # CCL
        # if ((self.H0 != H0) or (self.Om0 != Om0) or
        #     (self.Ob0 != Ob0) or (self.sigma8 != sigma8)):
        #     self.H0=H0
        #     self.Om0=Om0
        #     self.Ob0=Ob0
        #     self.sigma8=sigma8
        #     self.ns=ns
        #     self.cosmoModel=ccl.Cosmology(Omega_c=Om0-Ob0,
        #                                   Omega_b=Ob0,
        #                                   h=0.01*H0,
        #                                   sigma8=sigma8,
        #                                   n_s=ns,
        #                                   transfer_function=self.transferFunction)
        #     if self.massFuncName == 'Tinker10':
        #         self.mfunc=ccl.halos.MassFuncTinker10(mass_def = self.mdef)
        #     elif self.massFuncName == 'Tinker08':
        #         self.mfunc=ccl.halos.MassFuncTinker08(mass_def = self.mdef)


    def _doClusterCount(self):
        """Updates cluster count etc. after mass function object is updated.

        """

        print("in _doClusterCount")
        assert(self.areaSr == np.radians(np.sqrt(self.areaDeg2))**2)
        self.fsky=self.areaSr/(4*np.pi) # in case it was updated

        # CLASS-SZ
        # Still need to implement (maybe): self.volumeMpc3, self.numberDensity
        lnms=np.log(np.power(10,  self.log10M)*self.cosmo.h())
        dndmdz = np.zeros((self.log10M.shape[0], self.z.shape[0]))
        for (im,mm) in enumerate(lnms):
            dndmdz[im,:] = 4.*np.pi*self.fsky*np.vectorize(self.cosmo.get_volume_dVdzdOmega_at_z)(self.z)*np.vectorize(self.cosmo.get_dndlnM_at_z_and_M)(self.z,np.exp(mm))
        self.HMFRange=np.array([np.min(dndmdz),np.max(dndmdz)])
        dndz=np.trapz(dndmdz,x = lnms,axis = 0)
        self.numClusters=np.trapz(dndz, x = self.z)
        self.numClustersByRedshift=self.numClustersByRedshift=dndz*np.gradient(self.z)
        # I think below should be good to 0.1%
        norm=np.sum(dndmdz)/self.numClusters
        self.clusterCount=dndmdz/norm

        # # CCL
        # # Number density by z and total cluster count (in redshift shells)
        # zRange=self.zBinEdges
        # h = self.cosmoModel['h']
        # self.M=np.power(10, self.log10M) # in M_sun
        # norm_mfunc=1. / np.log(10)
        # numberDensity=[]
        # clusterCount=[]
        # totalVolumeMpc3=0.
        # for i in range(len(zRange)-1):
        #     zShellMin=zRange[i]
        #     zShellMax=zRange[i+1]
        #     zShellMid=(zShellMax+zShellMin)/2.
        #     dndlnM=self.mfunc(self.cosmoModel, self.M, 1./(1+zShellMid)) * norm_mfunc
        #     dndM = dndlnM / self.M
        #     n=dndM * np.gradient(self.M)
        #     numberDensity.append(n)
        #     shellVolumeMpc3=self._comovingVolume(zShellMax)-self._comovingVolume(zShellMin)
        #     shellVolumeMpc3=shellVolumeMpc3*(self.areaSr/(4*np.pi))
        #     totalVolumeMpc3+=shellVolumeMpc3
        #     clusterCount.append(n*shellVolumeMpc3)
        # numberDensity=np.array(numberDensity)
        # clusterCount=np.array(clusterCount)
        # self.volumeMpc3=totalVolumeMpc3
        # self.numberDensity=numberDensity
        # self.clusterCount=clusterCount
        # self.numClusters=np.sum(clusterCount)
        # self.numClustersByRedshift=np.sum(clusterCount, axis = 1)

    def drawSample(self, y0Noise, scalingRelationDict, QFit = None, wcs = None, photFilterLabel = None,\
                   tileName = None, SNRLimit = None, makeNames = False, z = None, numDraws = None,\
                   areaDeg2 = None, applySNRCut = False, applyPoissonScatter = True,\
                   applyIntrinsicScatter = True, applyNoiseScatter = True,\
                   applyRelativisticCorrection = True, verbose = False, biasModel = None):
        """Draw a cluster sample from the mass function, generating mock y0~ values (called `fixed_y_c` in
        Nemo catalogs) by applying the given scaling relation parameters, and then (optionally) applying
        a survey selection function.

        Args:
            y0Noise (:obj:`float` or :obj:`np.ndarray`): Either a single number (if using e.g., a survey
                average), an RMS table (with columns 'areaDeg2' and 'y0RMS'), or a noise map (2d array).
                A noise map must be provided here if you want the output catalog to contain RA, dec
                coordinates (in addition, a WCS object must also be provided - see below).
            scalingRelationDict (:obj:`dict`): A dictionary containing keys 'tenToA0', 'B0', 'Mpivot',
                'sigma_int' that describes the scaling relation between y0~ and mass (this is the
                format of `massOptions` in Nemo .yml config files).
            QFit (:obj:`nemo.signals.QFit`, optional): Object that handles the filter mismatch
                function, *Q*. If not given, the output catalog will not contain `fixed_y_c` columns,
                only `true_y_c` columns.
            wcs (:obj:`astWCS.WCS`, optional): WCS object corresponding to `y0Noise`, if `y0Noise` is
                as noise map (2d image array). Needed if you want the output catalog to contain RA, dec
                coordinates.
            photFilterLabel (:obj:`str`, optional): Name of the reference filter (as defined in the
                Nemo .yml config file) that is used to define y0~ (`fixed_y_c`) and the filter mismatch
                function, Q.
            tileName (:obj:`str`, optional): Name of the tile for which the sample will be generated.
            SNRLimit (:obj:`float`, optional): Signal-to-noise detection threshold used for the
                output catalog (corresponding to a cut on `fixed_SNR` in Nemo catalogs). Only applied
                if `applySNRCut` is also True (yes, this can be cleaned up).
            makeNames (:obj:`bool`, optional): If True, add names of the form MOCK CL JHHMM.m+/-DDMM
                to the output catalog.
            z (:obj:`float`, optional): If given produce a sample at the nearest z in the MockSurvey
                z grid. The default behaviour is to use the full redshift grid specified by `self.z`.
            numDraws (:obj:`int`, optional): If given, the number of draws to perform from the mass
                function, divided equally among the redshift bins. The default is to use the values
                contained in `self.numClustersByRedshift`.
            areaDeg2 (:obj:`float`, optional): If given, the cluster counts will be scaled to this
                area. Otherwise, they correspond to `self.areaDeg2`. This parameter will be ignored
                if `numDraws` is also given.
            applySNRCut (:obj:`bool`, optional): If True, cut the output catalog according to the
                `fixed_SNR` threshold set by `SNRLimit`.
            applyPoissonScatter (:obj:`bool`, optional): If True, add Poisson noise to the cluster
                counts (implemented by modifiying the number of draws from the mass function).
            applyIntrinsicScatter (:obj:`bool`, optional): If True, apply intrinsic scatter to the
                SZ measurements (`fixed_y_c`), as set by the `sigma_int` parameter in
                `scalingRelationDict`.
            applyNoiseScatter (:obj:`bool`, optional): If True, apply measurement noise, generated
                from the given noise level or noise map (`y0Noise`), to the output SZ measurements
                (`fixed_y_c`).
            applyRelativisticCorrection (:obj:`bool`, optional): If True, apply the relativistic
                correction.

        Returns:
            A catalog as an :obj:`astropy.table.Table` object, in the same format as produced by
            the main `nemo` script.

        Notes:
            If both `applyIntrinsicScatter`, `applyNoiseScatter` are set to False, then the output
            catalog `fixed_y_c` values will be exactly the same as `true_y_c`, although each object
            will still have an error bar listed in the output catalog, corresponding to its location
            in the noise map (if given).

        """

        # self.n_tot_obs = np.random.poisson(lam=th_ntot)

        # print('>>> ntot obs for this catalog: ', self.n_tot_obs)

        print("in drawSample()")
        import IPython
        IPython.embed()
        sys.exit()

        if numDraws is not None:
            numClusters=numDraws

        if applyPoissonScatter == True:
            numClusters=np.random.poisson(lam = self.numClusters)
        else:
            numClusters=int(round(self.numClusters))

        # If given y0Noise as RMSMap, draw coords (assuming clusters aren't clustered - which they are...)
        # NOTE: switched to using valid part of RMSMap here rather than areaMask - we need to fix the latter to same area
        # It isn't a significant issue though
        # This generates even density RA, dec coords on the whole sky taking into account the projection
        # Consequently, this is inefficient if fed individual tiles rather than a full sky noise map
        RMSMap=y0Noise
        xsList=[]
        ysList=[]
        maxCount=100000
        count=0
        while(len(xsList) < numClusters):
            count=count+1
            if count > maxCount:
                raise Exception("Failed to generate enough random coords in %d iterations" % (maxCount))
            theta=np.degrees(np.pi*2*np.random.uniform(0, 1, numClusters))
            phi=np.degrees(np.arccos(2*np.random.uniform(0, 1, numClusters)-1))-90
            xyCoords=np.array(wcs.wcs2pix(theta, phi))
            xs=np.array(np.round(xyCoords[:, 0]), dtype = int)
            ys=np.array(np.round(xyCoords[:, 1]), dtype = int)
            mask=np.logical_and(np.logical_and(xs >= 0, xs < RMSMap.shape[1]), np.logical_and(ys >= 0, ys < RMSMap.shape[0]))
            xs=xs[mask]
            ys=ys[mask]
            mask=RMSMap[ys, xs] > 0
            xsList=xsList+xs[mask].tolist()
            ysList=ysList+ys[mask].tolist()
        xs=np.array(xsList)[:numClusters]
        ys=np.array(ysList)[:numClusters]
        del xsList, ysList
        RADecCoords=wcs.pix2wcs(xs, ys)
        RADecCoords=np.array(RADecCoords)
        RAs=RADecCoords[:, 0]
        decs=RADecCoords[:, 1]
        y0Noise=RMSMap[ys, xs]

        # CLASS-SZ: draw zs and masses using rejection sampling (from Inigo Zubeldia)
        zs=np.zeros(y0Noise.shape)
        zErrs=np.zeros(y0Noise.shape)
        log10Ms=np.zeros(y0Noise.shape)
        for clusterIndex in range(numClusters):
            hmfEval=0.
            hmfSample=1.
            while hmfSample > hmfEval:
                ln10MSample=np.random.rand()*(self.log10M[-1]-self.log10M[0])+self.log10M[0]
                lnMhSample=np.log(10**ln10m_sample*self.cosmo.h())
                zSample=np.random.rand()*(self.z[-1]-self.z[0])+self.z[0]
                hmfSample=np.random.rand()*(self.hmf_range[-1]-self.hmf_range[0])+self.hmf_range[0]
                hmfEval=4.*np.pi*self.fsky*self.cosmo.get_volume_dVdzdOmega_at_z(z_sample)*self.cosmo.get_dndlnM_at_z_and_M(z_sample,np.exp(lnmh_sample))
            log10Ms[cluster_index] = ln10m_sample
            zs[cluster_index] = z_sample
        
        #
                   

        names=[]
        for RADeg, decDeg in zip(RAs, decs):
            names.append(catalogs.makeName(RADeg, decDeg, prefix = 'MOCK-CL'))
                
        
        
        M200c = np.power(10, log10Ms)
        true_y0s = np.vectorize(self.cosmo.get_y_at_m_and_z)(M200c*self.cosmo.h(),zs)
        
        tab = atpy.Table()
        
        tab.add_column(atpy.Column(names, 'name'))
        tab.add_column(atpy.Column(RAs, 'RADeg'))
        tab.add_column(atpy.Column(decs, 'decDeg'))
        tab.add_column(atpy.Column(np.power(10, log10Ms)/1e14, "true_M200c"))
        tab.add_column(atpy.Column(true_y0s/1e-4, 'true_y_c'))
        tab.add_column(atpy.Column(zs, 'redshift'))
        tab.add_column(atpy.Column(zErrs, 'redshiftErr'))
                

        return tab
