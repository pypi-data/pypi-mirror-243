###############################################################################
#
# Copyright (C) 2016-2023, Michele Cappellari
# E-mail: michele.cappellari_at_physics.ox.ac.uk
#
# This software is provided as is without any warranty whatsoever.
# Permission to use, for non-commercial purposes is granted.
# Permission to modify for personal or internal use is granted,
# provided this copyright and disclaimer are included unchanged
# at the beginning of the file. All other rights are reserved.
#
###############################################################################

from os import path
import numpy as np

from astropy import constants

from ppxf import ppxf_util as util

###############################################################################

class sps_lib:
    """
    This class is meant as an example that can be easily adapted by the users
    to deal with other spectral templates libraries, different IMFs or
    different chemical abundances.

    Input Parameters
    ----------------

    filename:
        Name of a Numpy np.savez() file containing the following arrays for a
        given SPS models library, like FSPS, Miles, GALEXEV, BPASS,...

        1. templates[npixels, n_ages, n_metals] in erg/cm^2/s/A
        2. lam[npixels] in Angstroms in common to all the spectra (can be non-uniform)
        3. fwhm[npixels] or scalar in Angstroms, for the instrumental line-spread function
        4. ages[n_ages] for the spectra along the 2nd dimension
        5. metals[n_metals] for the spectra along the 3nd dimension
        6. masses[n_ages, n_metals] mass of living stars + remnants for each SPS

        This file can be created with a command like::

            np.savez_compressed(filename, templates=templates, masses=masses, 
                                lam=lam, ages=ages, metals=metals, fwhm=fwhm)

    velscale:
        desired velocity scale for the output templates library in km/s 
        (e.g. 60). This is generally the same or an integer fraction of the 
        ``velscale`` of the galaxy spectrum used as input to ``ppxf``.
    FWHM_gal: 
        scalar with the constant resolution of the galaxy in Angstroms, or
        dictionary with the wavelength and instrumental resolution of every
        pixel of the galaxy spectrum in Angstroms ``{"lam":lam, "fwhm":fwhm}``.
        
        If ``FWHM_gal=None`` (default), no convolution is performed.

    Optional Keywords
    -----------------

    age_range: array_like with shape (2,)
        ``[age_min, age_max]`` optional age range (inclusive) in Gyr for the 
        MILES models. This can be useful e.g. to limit the age of the templates 
        to be younger than the age of the Universe at a given redshift.
    metal_range: array_like with shape (2,)
        ``[metal_min, metal_max]`` optional metallicity [M/H] range (inclusive) 
        for the MILES models (e.g.`` metal_range = [0, np.inf]`` to select only
        the spectra with Solar metallicity and above).
    norm_range: array_like with shape (2,)
        A two-elements vector specifying the wavelength range in Angstroms 
        within which to compute the templates normalization
        (e.g. ``norm_range=[5070, 5950]`` for the FWHM of the V-band).

        If ``norm_range=None`` (default), the templates are not normalized
        individually, but instead are all normalized by the same scalar, given
        by the median of all templates.

    norm_type: {'mean', 'max', 'lbol'} optional
        * 'mean': the templates are normalized to ``np.mean(template[band]) = 1``
          in the given ``norm_range`` wavelength range. When this keyword is
          used, ``ppxf`` will output light weights, and ``mean_age_metal()``
          will provide light-weighted stellar population quantities.
        * 'max':  the templates are normalized to ``np.max(template[band]) = 1``.
        * 'lbol':  the templates are normalized to ``lbol(template[band]) = 1``,
          where ``lbol`` is the integrated luminosity in the given wavelength
          range. If ``norm_range=[-np.inf, np.inf]`` and the templates extend
          over a wide wavelength range, the normalization approximates the
          true bolometric luminosity.

        One can use the output attribute ``.flux`` to convert light-normalized
        weights into mass weights, without repeating the ``ppxf`` fit.
        However, when using regularization in ``ppxf`` the results will not
        be identical. In fact, enforcing smoothness to the light-weights is
        not quite the same as enforcing it to the mass-weights.
    wave_range: array_like with shape (2,)
        A two-elements vector specifying the wavelength range in Angstroms for
        which to extract the stellar templates. Restricting the wavelength
        range of the templates to the range of the galaxy data is useful to
        save some computational time. By default ``wave_range=[3541, 1e4]``

    Output Parameters
    -----------------

    Stored as attributes of the ``sps_lib`` class:

    .ages_grid: array_like with shape (n_ages, n_metals)
        Age in Gyr of every template.
    .flux: array_like with shape (n_ages, n_metals)
        If ``norm_range is not None`` then ``.flux`` contains the mean flux
        in each template spectrum within ``norm_range`` before normalization.

        When using the ``norm_range`` keyword, the weights returned by 
        ``ppxf`` represent light contributed by each SPS population template.
        One can then use this ``.flux`` attribute to convert the light weights
        into fractional masses as follows::

            pp = ppxf(...)                                  # Perform the ppxf fit
            light_weights = pp.weights[~gas_component]      # Exclude gas templates weights
            light_weights = light_weights.reshape(reg_dim)  # Reshape to a 2D matrix
            mass_weights = light_weights/miles.flux         # Divide by .flux attribute
            mass_weights /= mass_weights.sum()              # Normalize to sum=1

    .templates: array_like with shape (npixels, n_ages, n_metals)
        Logarithmically sampled array with the spectral templates in Lsun/A.
    .lam_temp: array_like with shape (npixels,)
        Wavelength in Angstroms of every pixel of the output templates.
    .ln_lam_temp: array_like with shape (npixels,)
        Natural logarithm of `.lam_temp`.
    .metals_grid: array_like with shape (n_ages, n_metals)
        Metallicity [M/H] of every template.
    .n_ages: 
        Number of different ages.
    .n_metal: 
        Number of different metallicities.

    """

    def __init__(self, filename, velscale, fwhm_gal=None, age_range=None,
                 metal_range=None, norm_range=None, norm_type='mean', wave_range=None):

        assert norm_type in ['max', 'lbol', 'mean'], "`norm_type` must be in ['max', 'lbol', 'mean']"

        a = np.load(filename)
        spectra, masses, ages, metals, lam, fwhm_tem = \
            a["templates"], a["masses"], a["ages"], a["metals"], a["lam"], a["fwhm"]

        assert len(lam) == len(fwhm_tem) == len(spectra), \
            "`lam`, `fwhm` and `templates` must have the same length"
        assert masses.shape == spectra.shape[1:] == (ages.size, metals.size), \
            "must be masses.shape == spectra.shape[1:] == (ages.size, metals.size)"

        metal_grid, age_grid = np.meshgrid(metals, ages)

        if fwhm_gal is not None:

            if isinstance(fwhm_gal, dict):
                # Computes the spectral resolution of the galaxy at each pixel of
                # the templates. The resolution is interpolated from the galaxy
                # spectrum within its range, and constant beyond its range.
                fwhm_gal = np.interp(lam, fwhm_gal["lam"], fwhm_gal["fwhm"])

            fwhm_diff2 = (fwhm_gal**2 - fwhm_tem**2).clip(0)
            if np.any(fwhm_diff2 == 0):
                print("WARNING: the template's resolution dlam is larger than the galaxy's")
            sigma = np.sqrt(fwhm_diff2)/np.sqrt(4*np.log(4))
            spectra = util.varsmooth(lam, spectra, sigma)

        templates, ln_lam_temp = util.log_rebin(lam, spectra, velscale=velscale)[:2]
        lam_temp = np.exp(ln_lam_temp)

        if norm_range is None:
            flux = np.median(templates[templates > 0])  # Single factor for all templates
            flux = np.full(templates.shape[1:], flux)
        else:
            assert len(norm_range) == 2, 'norm_range must have two elements [lam_min, lam_max]'
            band = (norm_range[0] <= lam_temp) & (lam_temp <= norm_range[1])
            if norm_type == 'mean':
                flux = templates[band].mean(0)          # Different factor for every template
            elif norm_type == 'max':
                flux = templates[band].max(0)           # Different factor for every template
            elif norm_type == 'lbol':
                lbol = (templates[band].T @ np.gradient(lam_temp[band])).T  # Bolometric luminosity in Lsun
                flux = lbol*(templates[band].mean()/lbol.mean())            # Make overall mean level ~1
        templates /= flux

        if age_range is not None:
            w = (age_range[0] <= ages) & (ages <= age_range[1])
            templates = templates[:, w, :]
            age_grid = age_grid[w, :]
            metal_grid = metal_grid[w, :]
            flux = flux[w, :]
            masses = masses[w, :]

        if metal_range is not None:
            w = (metal_range[0] <= metals) & (metals <= metal_range[1])
            templates = templates[:, :, w]
            age_grid = age_grid[:, w]
            metal_grid = metal_grid[:, w]
            flux = flux[:, w]
            masses = masses[:, w]

        self.templates_full = templates
        self.ln_lam_temp_full = ln_lam_temp
        self.lam_temp_full = lam_temp
        if wave_range is not None:
            good_lam = (lam_temp >= wave_range[0]) & (lam_temp <= wave_range[1])
            lam_temp = lam_temp[good_lam]
            ln_lam_temp = ln_lam_temp[good_lam]
            templates = templates[good_lam]

        self.templates = templates
        self.ln_lam_temp = ln_lam_temp
        self.lam_temp = lam_temp
        self.age_grid = age_grid    # in Gyr
        self.metal_grid = metal_grid
        self.n_ages, self.n_metals = age_grid.shape
        self.flux = flux            # factor by which each template was divided
        self.mass_no_gas_grid = masses


###############################################################################

    def plot(self, weights, nodots=False, colorbar=True, **kwargs):

        assert weights.ndim == 2, "`weights` must be 2-dim"
        assert self.age_grid.shape == self.metal_grid.shape == weights.shape, \
            "Input weight dimensions do not match"

        xgrid = np.log10(self.age_grid) + 9
        ygrid = self.metal_grid
        util.plot_weights_2d(xgrid, ygrid, weights,
                             nodots=nodots, colorbar=colorbar, **kwargs)


##############################################################################

    def mean_age_metal(self, weights, quiet=False):

        assert weights.ndim == 2, "`weights` must be 2-dim"
        assert self.age_grid.shape == self.metal_grid.shape == weights.shape, \
            "Input weight dimensions do not match"

        lg_age_grid = np.log10(self.age_grid) + 9
        metal_grid = self.metal_grid

        # These are eq.(39) of Cappellari (2023)
        mean_lg_age = np.sum(weights*lg_age_grid)/np.sum(weights)
        mean_metal = np.sum(weights*metal_grid)/np.sum(weights)

        if not quiet:
            print(f'Weighted <lg_age> [yr]: {mean_lg_age:#.3g}')
            print(f'Weighted <[M/H]>: {mean_metal:#.3g}')

        return mean_lg_age, mean_metal
 

##############################################################################
#
# MODIFICATION HISTORY:
#   V1.0.0: Written. Michele Cappellari, Oxford, 1 December 2016
#   V1.0.1: Use path.realpath() to deal with symbolic links.
#       Thanks to Sam Vaughan (Oxford) for reporting problems.
#       MC, Garching, 11 January 2016
#   V1.0.2: Changed imports for pPXF as a package. MC, Oxford, 16 April 2018
#   V1.0.3: Removed dependency on cap_readcol. MC, Oxford, 10 May 2018

    def mass_to_light(self, weights, band="r", quiet=False):
        """
        ** IMPORTANT: This only works for E-MILES models **

        Computes the M/L in a chosen band, given the weights produced in output
        by pPXF. A Salpeter IMF is assumed (slope=1.3). The function assumes
        the galaxy redshift is negligible and the photometric bands are at
        their restframe wavelength. The returned M/L includes living stars and
        stellar remnants, but excludes the gas lost during stellar evolution.

        This procedure uses the photometric predictions
        from Vazdekis+12 and Ricciardelli+12
        http://adsabs.harvard.edu/abs/2012MNRAS.424..157V
        http://adsabs.harvard.edu/abs/2012MNRAS.424..172R
        I downloaded them from http://miles.iac.es/ in December 2016 and I
        included them in pPXF with permission.

        :param weights: pPXF output with dimensions weights[miles.n_ages, miles.n_metal]
        :param band: possible choices are "U", "B", "V", "R", "I", "J", "H", "K" for
            the Vega photometric system and "u", "g", "r", "i" for the SDSS AB system.
        :param quiet: set to True to suppress the printed output.
        :return: mass_to_light in the given band

        """
        assert self.age_grid.shape == self.metal_grid.shape == weights.shape, \
            "Input weight dimensions do not match"

        vega_bands = ["U", "B", "V", "R", "I", "J", "H", "K"]
        sdss_bands = ["u", "g", "r", "i"]
        vega_sun_mag = [5.600, 5.441, 4.820, 4.459, 4.148, 3.711, 3.392, 3.334]
        sdss_sun_mag = [6.55, 5.12, 4.68, 4.57]  # values provided by Elena Ricciardelli

        ppxf_dir = path.dirname(path.realpath(util.__file__))

        if band in vega_bands:
            k = vega_bands.index(band)
            sun_mag = vega_sun_mag[k]
            file2 = path.join(ppxf_dir, "sps_models", "Vazdekis2012_ssp_phot_Padova00_UN_v10.0.txt")
        elif band in sdss_bands:
            k = sdss_bands.index(band)
            sun_mag = sdss_sun_mag[k]
            file2 = path.join(ppxf_dir, "sps_models", "Vazdekis2012_ssp_sdss_miuscat_UN1.30_v9.txt")
        else:
            raise ValueError("Unsupported photometric band")

        file1 = path.join(ppxf_dir, "sps_models", "Vazdekis2012_ssp_mass_Padova00_UN_baseFe_v10.0.txt")
        slope1, MH1, Age1, m_no_gas = np.loadtxt(file1, usecols=[1, 2, 3, 5]).T

        slope2, MH2, Age2, mag = np.loadtxt(file2, usecols=[1, 2, 3, 4 + k]).T

        # The following loop is a brute force, but very safe and general,
        # way of matching the photometric quantities to the SSP spectra.
        # It does not assume the sorting and dimensions of the files
        mass_no_gas_grid = np.empty_like(weights)
        lum_grid = np.empty_like(weights)
        for j in range(self.n_ages):
            for k in range(self.n_metals):
                p1 = (np.abs(self.age_grid[j, k] - Age1) < 0.001) & \
                     (np.abs(self.metal_grid[j, k] - MH1) < 0.01) & \
                     (np.abs(1.30 - slope1) < 0.01)   # Salpeter IMF
                mass_no_gas_grid[j, k] = m_no_gas[p1]

                p2 = (np.abs(self.age_grid[j, k] - Age2) < 0.001) & \
                     (np.abs(self.metal_grid[j, k] - MH2) < 0.01) & \
                     (np.abs(1.30 - slope2) < 0.01)   # Salpeter IMF
                lum_grid[j, k] = 10**(-0.4*(mag[p2] - sun_mag))

        # This is eq.(2) in Cappellari+13
        # http://adsabs.harvard.edu/abs/2013MNRAS.432.1862C
        mlpop = np.sum(weights*mass_no_gas_grid)/np.sum(weights*lum_grid)

        if not quiet:
            print(f'(M*/L)_{band}: {mlpop:#.4g} (only valid for E-MILES SPS)')

        return mlpop


###############################################################################

def solar_mag(bands, redshift=0, system='AB'):
    """
    Computes the absolute magnitude of the Sun in the AB or Vega magnitude
    system in the given set of bands, optionally shifted to the given redshift.
    
    NB: The (1 + z) dimming factor is *not* applied.

    """        
    ppxf_dir = path.dirname(path.realpath(util.__file__))
    filename = path.join(ppxf_dir, 'sps_models', 'spectra_sun_vega.npz')
    a = np.load(filename)  # Spectrum in cgs/A
    flux_sun, lam = a["flux_sun"], a["lam"]

    if system == 'AB':
        c_as = constants.c.to('Angstrom/s').value   # speed of light
        flux_ref = 3631e-23*c_as/lam**2             # AB flux in cgs/A
    elif system == 'Vega':
        flux_ref = a["flux_vega"]

    velscale = 1000  # Don't need high resolution for photometry
    flux = np.column_stack([flux_sun, flux_ref])
    flux_new, ln_lam, velscale = util.log_rebin(lam, flux, velscale)

    p = util.synthetic_photometry(flux_new, np.exp(ln_lam), bands, redshift=redshift)
    sun_mag = -2.5*np.log10(np.divide(*p.flux.T))

    return sun_mag

##############################################################################
