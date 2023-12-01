#!/usr/bin/env python
##############################################################################
#
# Usage example for the procedure PPXF, which implements the
# Penalized Pixel-Fitting (pPXF) method originally described in
# Cappellari M., & Emsellem E., 2004, PASP, 116, 138
#   http://ui.adsabs.harvard.edu/abs/2004PASP..116..138C
# upgraded in Cappellari M., 2017, MNRAS, 466, 798
#     http://adsabs.harvard.edu/abs/2017MNRAS.466..798C
# and with photometry in Cappellari M., 2023, MNRAS, 526, 3273C
#   https://ui.adsabs.harvard.edu/abs/2023MNRAS.526.3273C
#
# This example shows how to fit photometry and spectra together.
# It shows how to use three different SPS models: E-MILES, GALAXEV and fsps
#
# MODIFICATION HISTORY:
#   V1.0.0: Written
#       Michele Cappellari, Oxford, 16 March 2022
#   V1.1.0: Updated to use new util.synthetic_photometry.
#       MC, Oxford, 10 June 2022
#   V1.2.1: Changed to use synthetic_photometry() as a class.
#       Show how to match the photometry and the spectrum.
#       MC, Oxford, 13 September 2023
#   V1.3.0: Use the new `sps_util` instead of `miles_util`. 
#       MC, Oxford, 12 November 2023
#
##############################################################################

from time import perf_counter as clock
from os import path
from urllib import request

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

from ppxf.ppxf import ppxf
import ppxf.ppxf_util as util
import ppxf.sps_util as lib

##############################################################################

def ppxf_example_population_photometry(phot_fit=True, sps_name='fsps'):
    
    # ------------------- Read the observed galaxy spectrum --------------------

    # Read SDSS DR8 galaxy spectrum taken from here http://www.sdss3.org/dr8/
    # The spectrum is *already* log rebinned by the SDSS DR8
    # pipeline and my log_rebin() should not be used in this case.
    ppxf_dir = path.dirname(path.realpath(util.__file__))
    file = path.join(ppxf_dir, 'spectra', 'NGC3073_SDSS_DR8.fits')
    hdu = fits.open(file)[1]
    t = hdu.data
    redshift = float(hdu.header["Z"])  # SDSS redshift estimate

    galaxy = t['flux']/np.median(t['flux'])  # Normalize spectrum to avoid numerical issues
    wave = t['wavelength']

    # Restricts the fit to the region sampled by the high quality MILES spectra
    w = wave < 7500
    galaxy = galaxy[w]
    wave = wave[w]

    # The SDSS wavelengths are in vacuum, while the MILES ones are in air.
    # For a rigorous treatment, the SDSS vacuum wavelengths should be
    # converted into air wavelengths and the spectra should be resampled.
    # To avoid resampling, given that the wavelength dependence of the
    # correction is very weak, I approximate it with a constant factor.
    wave *= np.median(util.vac_to_air(wave)/wave)

    rms = 0.019  # rms scatter of the spectrum residuals
    noise = np.full_like(galaxy, rms)

    # Estimate the wavelength fitted range in the rest frame.
    # This is used to select the gas templates falling in the fitted range
    lam_range_gal = np.array([np.min(wave), np.max(wave)])/(1 + redshift)

    # --------------- Observed galaxy photometric fluxes -----------------------

    # Mean galaxy fluxes in the photometric bands [FUV, NUV, u, g, r, i, z, J, H, K]
    # (I invented the fluxes in this example for illustration)
    phot_galaxy = np.array([1.23e-16, 6.23e-17, 4.19e-17, 5.67e-17, 3.90e-17, 
                            2.93e-17, 2.30e-17, 1.30e-17, 7.83e-18, 3.49e-18])  # fluxes in erg/cm^2/s/A
    phot_noise = np.full_like(phot_galaxy, np.max(phot_galaxy)*0.03)  # 1sigma uncertainties of 3%

    # ------------------- Setup spectral templates -----------------------------

    # The velocity step was already chosen by the SDSS pipeline and I convert it to km/s
    c = 299792.458  # speed of light in km/s
    velscale = c*np.log(wave[1]/wave[0])  # eq.(8) of Cappellari (2017)
    FWHM_gal = 2.76  # SDSS has an approximate instrumental resolution FWHM of 2.76A.

    # Read SPS model file from my GitHub if not already in the ppxf package dir.
    # The SPS model files are also available here https://github.com/micappe/ppxf_data
    basename = f"spectra_{sps_name}_9.0.npz"
    filename = path.join(ppxf_dir, 'sps_models', basename)
    if not path.isfile(filename):
        url = "https://raw.githubusercontent.com/micappe/ppxf_data/main/" + basename
        request.urlretrieve(url, filename)

    # The templates are normalized to the V-band using norm_range. In this way,
    # the weights returned by pPXF represent V-band light fractions of each SSP.
    sps = lib.sps_lib(filename, velscale, FWHM_gal, norm_range=[5070, 5950])

    # The stellar templates are reshaped below into a 2-dim array with each
    # spectrum as a column; however, we save the original array dimensions,
    # which are needed to specify the regularization dimensions
    reg_dim = sps.templates.shape[1:]
    stars_templates = sps.templates.reshape(sps.templates.shape[0], -1)

    # Construct a set of Gaussian emission line templates. The `emission_lines`
    # function defines the most common lines, but additional lines can be
    # included by editing the function in the file ppxf_util.py.
    gas_templates, gas_names, line_wave = util.emission_lines(
        sps.ln_lam_temp, lam_range_gal, FWHM_gal)

    # Combines the stellar and gaseous templates into a single array. During
    # the pPXF fit they will be assigned a different kinematic COMPONENT value
    templates = np.column_stack([stars_templates, gas_templates])

    # ------------------- Setup photometric templates --------------------------

    if phot_fit:
        bands = ['galex1500', 'galex2500', 'SDSS/u', 'SDSS/g', 'SDSS/r', 
                 'SDSS/i', 'SDSS/z', '2MASS/J', '2MASS/H', '2MASS/K']

        # Scale photometry to match the spectrum as in Sec.6.4 of Cappellari (2023, MNRAS)
        # https://ui.adsabs.harvard.edu/abs/2023MNRAS.526.3273C

        # Compute synthetic photometry on SDSS galaxy spectrum, which is already in rest-frame
        print("\nSynthetic photometry on the observed galaxy spectrum")
        p2 = util.synthetic_photometry(galaxy, wave, bands, redshift=redshift)

        # Extract the bands that fall inside the galaxy spectrum.
        # Scale photometry to match the synthetic one from the SDSS spectrum
        d = p2.flux[p2.ok]
        m = phot_galaxy[p2.ok]    # p2.ok=True if band is in galaxy wavelength range
        scale = (d @ m)/(m @ m)   # eq.(34) of Cappellari (2023, MNRAS)
        phot_galaxy *= scale
        phot_noise *= scale

        # Compute the photometric templates in the observed bands
        print("\nSynthetic photometry on the SPS templates")
        p1 = util.synthetic_photometry(templates, sps.lam_temp, bands, redshift=redshift)
        phot = {"templates": p1.flux[p1.ok], "lam": p1.lam_eff[p1.ok],
                "galaxy": phot_galaxy[p1.ok], "noise": phot_noise[p1.ok]}
    else:
        phot = None

    # --------------------------------------------------------------------------

    vel = c*np.log(1 + redshift)  # eq.(8) of Cappellari (2017)
    start = [vel, 200.]  # (km/s), starting guess for [V, sigma]

    n_stars = stars_templates.shape[1]
    n_gas = len(gas_names)

    # I fit two kinematics components, one for the stars and one for the gas.
    # Assign component=0 to the stellar templates, component=1 to the gas.
    component = [0]*n_stars + [1]*n_gas
    gas_component = np.array(component) > 0  # gas_component=True for gas templates

    # Fit (V, sig) moments=2 for both the stars and the gas
    moments = [2, 2]

    # Adopt the same starting value for both the stars and the gas components
    start = [start, start]

    t = clock()
    print("\nStarting pPXF fit")
    pp = ppxf(templates, galaxy, noise, velscale, start, moments=moments,
              degree=-1, mdegree=8, lam=wave, lam_temp=sps.lam_temp,
              regul=1/rms, reg_dim=reg_dim, component=component, reddening=0.1,
              gas_component=gas_component, gas_names=gas_names, phot=phot)
    print(f"Elapsed time in pPXF: {(clock() - t):.2f}")

    light_weights = pp.weights[~gas_component]  # Exclude weights of the gas templates
    light_weights = light_weights.reshape(reg_dim)  # Reshape to (n_ages, n_metal)
    light_weights /= light_weights.sum()  # Normalize to light fractions

    # Given that the templates are normalized to the V-band, the pPXF weights
    # represent v-band light fractions, and the computed ages and metallicities
    # below are also light weighted in the V-band.
    sps.mean_age_metal(light_weights)

    # Plot fit results for stars and gas.
    plt.clf()

    if phot_fit:
        plt.subplot(311)
        pp.plot(spec=False, phot=True)
        plt.subplot(312)
        pp.plot(spec=True, phot=False, gas_clip=True)
        plt.subplot(313)
    else:
        plt.subplot(211)
        pp.plot()
        plt.subplot(212)

    sps.plot(light_weights)
    plt.tight_layout()


##############################################################################

if __name__ == '__main__':

    # pPXF can be used with any set of SPS population templates. However, I am
    # currently providing (with permission) ready-to-use template files for
    # three SPS. One can just uncomment one of the three models below. The
    # included files are only a subset of the SPS that can be produced with the
    # models, and one should use the relevant software to produce different
    # sets of SPS templates if needed.
    #
    # 1. If you use the fsps v3.2 (https://github.com/cconroy20/fsps) SPS
    #    model templates, please also cite Conroy et al. (2009)
    #    (https://ui.adsabs.harvard.edu/abs/2009ApJ...699..486C/) and 
    #    Conroy et al. (2010) (https://ui.adsabs.harvard.edu/abs/2010ApJ...712..833C/) 
    #    in your paper.
    #
    # 2. If you use the GALAXEV v2000 (http://www.bruzual.org/bc03/) SPS model
    #    templates, please also cite Bruzual & Charlot (2003)
    #    (https://ui.adsabs.harvard.edu/abs/2003MNRAS.344.1000B/) in your paper.
    #
    # 3. If you use the E-MILES (http://miles.iac.es/) SPS model templates,
    #    please also cite Vazdekis et al. (2016)
    #    (https://ui.adsabs.harvard.edu/abs/2016MNRAS.463.3409V/) in your paper. 
    #    WARNING: the E-MILES models do not include very young SPS and should
    #    not be used for highly star forming galaxies.  
    
    # sps_name = 'fsps'
    sps_name = 'galaxev'
    # sps_name = 'emiles'

    ppxf_example_population_photometry(phot_fit=True, sps_name=sps_name)
    plt.pause(5)
    