# -*- coding: utf-8 -*-
"""
Created on Thu July 28 20:30:11 2018

@author: danielgodinez
"""
import numpy as np
from scipy.interpolate import UnivariateSpline
from math import log

def create_noise(median, rms, degree=3):
    """Creates a noise model by fitting a one-dimensional smoothing 
    spline of degree k.

    Parameters
    ----------
    median : array
        Baseline magnitudes.
    rms : array
        Corresponding RMS per baseline. 
    k : int
        Degree of the smoothing spline. Default is a 
        cubic spline of degree 3.

    Returns
    -------
    fn : The kth degree spline fit. 
    """
    f = UnivariateSpline(median, rms, w=None, k=degree)
    return f

def add_noise(mag, fn, zp=24):
    """Adds noise to magnitudes given a noise function. 

    Parameters
    ----------
    mag : array
        Magnitude to add noise to. 
    fn : function
        Spline fit, must be defined using the create_noise function. 
    zp : Zeropoint
        Zeropoint of the instrument, default is 24.
        
    Returns
    -------
    mag : array
        The noise-added magnitudes. 
    magerr : array
        The corresponding magnitude errors.
    """    
    flux = 10**(-(mag-zp)/2.5)
    delta_fobs = flux*fn(mag)*(log(10)/2.5)
    f_obs = np.random.normal(flux, delta_fobs)

    mag_obs = zp - 2.5*np.log10(f_obs)
    magerr = (2.5/log(10))*(delta_fobs/f_obs)
        
    return np.array(mag_obs), np.array(magerr)

def add_gaussian_noise(mag,zp=24):
    """Adds noise to lightcurve given the magnitudes.

    Parameters
    ----------
    mag : array
        Mag array to add noise to. 
    zp : zeropoint
        Zeropoint of the instrument, default is 24.
    convert : boolean, optional 
    
    Returns
    -------
    noisy_mag : array
        The noise-added magnitude. 
    magerr : array
        The corresponding magnitude errors.
    """
    flux = 10**((mag-zp)/-2.5)
    
    noisy_flux= np.random.normal(flux, np.sqrt(flux))
    magerr = 2.5/(log(10)*np.sqrt(noisy_flux))
    
    noisy_mag = zp - 2.5*np.log10(noisy_flux)
    magerr=np.array(magerr)
    mag = np.array(mag)

    return np.array(noisy_mag), np.array(magerr)