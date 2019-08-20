#!/usr/bin/env python3
import numpy as np
from astropy.time import Time
from astropy.io import fits

def write_fits_file(fname, img, nfd, texp, gain, temp):
    # Image shape
    ny, nx = img.shape
    
    # FITS header
    hdr = fits.Header()
    hdr['DATE-OBS'] = "%s" % nfd
    hdr['MJD-OBS'] = Time(nfd, format="isot").mjd
    hdr['EXPTIME'] = texp
    hdr['GAIN'] = gain
    hdr['TEMP'] = temp
    hdr['CRPIX1'] = float(nx)/2.0
    hdr['CRPIX2'] = float(ny)/2.0
    hdr['CRVAL1'] = 0.0
    hdr['CRVAL2'] = 0.0
    hdr['CD1_1'] = 1.0/3600.0
    hdr['CD1_2'] = 0.0
    hdr['CD2_1'] = 0.0
    hdr['CD2_2'] = 1.0/3600.0
    hdr['CTYPE1'] = "RA---TAN"
    hdr['CTYPE2'] = "DEC--TAN"
    hdr['CUNIT1'] = "deg"
    hdr['CUNIT2'] = "deg"
    hdr['CRRES1'] = 0.0
    hdr['CRRES2'] = 0.0
    hdr['EQUINOX'] = 2000.0
    hdr['RADECSYS'] = "ICRS"
    
    # Write FITS file
    hdu = fits.PrimaryHDU(data=img,
                          header=hdr)
    hdu.writeto(fname, overwrite=True)

    return
