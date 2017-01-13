# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:46:19 2017

@author: danielgodinez
"""

from stats_computation import RMS, meanMag, medianMag, minMag, maxMag, medianAbsDev, kurtosis, skewness, stetsonJ, stetsonK, vonNeumannRatio, above1, above3, above5, below1, below3, below5, compute_statistics
import numpy as np
import unittest

mag = np.array([18, 18.3, 18.1, 18, 18.4, 18.9, 19.2, 19.3, 19.5, 19.2, 18.8, 18.3, 18.6])
magerr = np.array([0.01, 0.01, 0.03, 0.09, 0.04, 0.1, 0.03, 0.13, 0.04, 0.06, 0.09, 0.1, 0.35])
mjd = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

def test_rms(value):
    value.assertEqual( RMS(mag), 18.661538461538463 )

def test_mean(value):
    value.assertEqual( meanMag(mag), 18.661538461538463 )

def test_median(value):
    value.assertEqual( medianMag(mag), 18.600000000000001)
    
def test_min(value):
    value.assertEqual( minMag(mag), 18.0)

def test_max(value):
    value.assertEqual( maxMag(mag), 19.5)
    
def test_medianAbsDev(value):
    value.assertEqual( medianAbsDev(mag), 0.5)
    
def test_kurtosis(value):
    value.assertEqual( kurtosis(mjd, mag), -1.0149598629254664 )
    
def test_skewness(value):
    value.assertEqual( skewness(mag), 0.1868991393928264 )

def test_stetsonJ(value):
    value.assertEqual( stetsonJ(mjd, mag, magerr), 159412.78061393721 )

def test_stetsonK(value):
    value.assertEqual( stetsonK(mjd, mag, magerr), 0.64699834923516031 )

def test_vonNeumannRatio(value):
    value.assertEqual( vonNeumannRatio(mag), 0.38896680691912117 )
    
def test_above1(value):
    value.assertEqual( above1(mag), 0.3076923076923077 )
    
def test_above3(value):
    value.assertEqual( above3(mag), 0.0 )
    
def test_above5(value):
    value.assertEqual( above5(mag), 0.0)
    
def test_below1(value):
    value.assertEqual( below1(mag), 0.6923076923076923 )

def test_below3(value):
    value.assertEqual( below3(mag), 1.0 )

def test_below5(value):
    value.assertEqual( below5(mag), 1.0 )

def test_compute_statistics(value):
    value.assertEqual( compute_statistics(mjd, mag, magerr), [18.661538461538463, 18.600000000000001, 18.661538461538463, 19.5, 18.0, 0.5, -1.0149598629254664, 0.1868991393928264, 159412.78061393721, 0.64699834923516031, 0.38896680691912117, 0.3076923076923077, 0.0, 0.0, 0.6923076923076923, 1.0, 1.0] )
    
unittest.main()
