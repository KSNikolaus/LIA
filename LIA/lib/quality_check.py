# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 20:30:11 2018

@author: danielgodinez
"""
from __future__ import division
import numpy as np
from simulate import constant
   
def test_microlensing(timestamps, microlensing_mag, magerr, baseline, u_0, t_0, t_e, blend_ratio):
    """Test to ensure proper microlensing signal.
    This requires 7 measurements with a magnification of at least 1.34, inmposing
    additoinal magnification thresholds to ensure microlensing event doesn't 
    mimic a noisy constant.

    Parameters
    ----------
    timestamps : array
        Times at which to simulate the lightcurve.
    microlensing_mag : array
        Microlensing simulated magnitudes given the timestamps. 
    magerr : array
        Photometric error for each mag measurement.
    baseline : float
        Baseline magnitude of the event. 
    u_0 : float
        The source minimum impact parameter.
    t_0 : float
        The time of maximum magnification.
    t_E : float
        The timescale of the event in days.
    blend_ratio : float
        The blending coefficient.
        
    Returns
    -------
    condition : boolean
        Returns True if microlensing passes the quality test. 
    """
    mag = constant(timestamps, baseline)
    condition = False
    signal_indices = np.argwhere((timestamps > (t_0 - t_e)) & (timestamps < (t_0 + t_e))) 
    if len(signal_indices) >= 7:
        mean1 = np.mean(mag[signal_indices])
        mean2 = np.mean(microlensing_mag[signal_indices])
                
        signal_measurements = []
        for inx in signal_indices:
           value = (mag[inx] - microlensing_mag[inx]) / magerr[inx]
           signal_measurements.append(value)

        signal_measurements = np.array(signal_measurements)
        if (len(np.argwhere(signal_measurements >= 3)) > 0 and 
           mean2 < (mean1 - 0.05) and 
           len(np.argwhere(signal_measurements > 3)) >= 0.33*len(signal_measurements) and 
           (1.0/u_0) < blend_ratio):
               condition = True
               
    return condition  

def test_cv(timestamps, outburst_start_times, outburst_end_times, end_rise_times, end_high_times):
    """Test to ensure proper CV signal.
    This requires 7 measurements within ANY outburst, with at least one occurring within the rise or fall.

    Parameters
    ----------
    timestamps : array
        Times at which to simulate the lightcurve.
    outburst_start_times : array
        The start time of each outburst.
    outburst_end_times : array
        The end time of each outburst.
    end_rise_times : array
        The end time of each rise (start time of max amplitude).
    end_high_times : array
        The end time of each peak (end time of max amplitude).
        
    Returns
    -------
    condition : boolean
        Returns True if CV passes the quality test. 
    """
    signal_measurements = []
    rise_measurements = []
    fall_measurements = []
    condition = False
    for k in range(len(outburst_start_times)):
        inx = len(np.argwhere((timestamps >= outburst_start_times[k])&(timestamps <= outburst_end_times[k])))
        signal_measurements.append(inx)

        inx = len(np.argwhere((timestamps >= outburst_start_times[k])&(timestamps <= end_rise_times[k])))
        rise_measurements.append(inx)  

        inx = len(np.argwhere((timestamps >= end_high_times[k])&(timestamps <= outburst_end_times[k])))
        fall_measurements.append(inx) 

    for k in range(len(signal_measurements)):
        if signal_measurements[k] >= 7:
            if rise_measurements[k] or fall_measurements[k] >= 1:
                condition = True
                break 

    return condition 
