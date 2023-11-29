########################################################
# Started Logging At: 2020-04-09 14:35:43
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:35:47
########################################################
########################################################
# Started Logging At: 2020-04-09 14:39:18
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:39:19
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
########################################################
# Started Logging At: 2020-04-09 14:39:55
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:39:56
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
########################################################
# Started Logging At: 2020-04-09 14:43:05
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:43:06
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
cd ~/repos/pyspeckit
get_ipython().run_line_magic('pip', 'install -e .')
get_ipython().run_cell_magic('bash', '', 'cd ~/repos/pyspeckit\nwhich pip\npip install -e .\n')
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
########################################################
# Started Logging At: 2020-04-09 14:45:10
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:45:11
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
########################################################
# Started Logging At: 2020-04-09 14:45:27
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:45:28
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
from astropy import units as u
from astropy import constants
freq = 23*u.GHz
def tau_wrong(tkin, tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tkin)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
def tau_right(tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tex)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
tkin = np.linspace(5,40,101)*u.K
tex = np.linspace(5,40,100)*u.K
grid = np.array([[tau_wrong(tk,tx)/tau_right(tx) for tx in tex] for tk in tkin])
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.imshow(grid, cmap='hot', extent=[5,40,5,40])
pl.xlabel("Tex")
pl.ylabel("Tkin")
pl.colorbar()
pl.contour(tex, tkin, grid, levels=[0.75,1,1/0.75], colors=['w','w','k'])
#[Out]# <matplotlib.contour.QuadContourSet at 0x11fca6890>
def nunlnu_error(Tkin):
    return 1+np.exp(-constants.h * freq / (constants.k_B * Tkin))
pl.plot(tkin.value, nunlnu_error(tkin))
#[Out]# [<matplotlib.lines.Line2D at 0x11fc81a90>]
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
get_ipython().run_cell_magic('bash', '', 'cd ~/repos/pyradex\npip install -e .\n')
get_ipython().run_cell_magic('bash', '', 'cd ~/repos/pyradex\npython setup.py install_radex\n')
get_ipython().run_cell_magic('bash', '', 'cd ~/repos/pyradex\npython setup.py install_radex install_myradex build\n')
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
########################################################
# Started Logging At: 2020-04-09 14:50:13
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:50:14
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
from astropy import units as u
from astropy import constants
freq = 23*u.GHz
def tau_wrong(tkin, tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tkin)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
def tau_right(tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tex)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
tkin = np.linspace(5,40,101)*u.K
tex = np.linspace(5,40,100)*u.K
grid = np.array([[tau_wrong(tk,tx)/tau_right(tx) for tx in tex] for tk in tkin])
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.imshow(grid, cmap='hot', extent=[5,40,5,40])
pl.xlabel("Tex")
pl.ylabel("Tkin")
pl.colorbar()
pl.contour(tex, tkin, grid, levels=[0.75,1,1/0.75], colors=['w','w','k'])
#[Out]# <matplotlib.contour.QuadContourSet at 0x1297a5490>
def nunlnu_error(Tkin):
    return 1+np.exp(-constants.h * freq / (constants.k_B * Tkin))
pl.plot(tkin.value, nunlnu_error(tkin))
#[Out]# [<matplotlib.lines.Line2D at 0x129784590>]
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
########################################################
# Started Logging At: 2020-04-09 14:57:50
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:57:52
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
from astropy import units as u
from astropy import constants
freq = 23*u.GHz
def tau_wrong(tkin, tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tkin)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
def tau_right(tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tex)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
tkin = np.linspace(5,40,101)*u.K
tex = np.linspace(5,40,100)*u.K
grid = np.array([[tau_wrong(tk,tx)/tau_right(tx) for tx in tex] for tk in tkin])
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.imshow(grid, cmap='hot', extent=[5,40,5,40])
pl.xlabel("Tex")
pl.ylabel("Tkin")
pl.colorbar()
pl.contour(tex, tkin, grid, levels=[0.75,1,1/0.75], colors=['w','w','k'])
#[Out]# <matplotlib.contour.QuadContourSet at 0x122927ed0>
def nunlnu_error(Tkin):
    return 1+np.exp(-constants.h * freq / (constants.k_B * Tkin))
pl.plot(tkin.value, nunlnu_error(tkin))
#[Out]# [<matplotlib.lines.Line2D at 0x1228e67d0>]
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
########################################################
# Started Logging At: 2020-04-09 14:59:22
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:59:23
########################################################
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
########################################################
# Started Logging At: 2020-04-09 14:59:50
########################################################
########################################################
# # Started Logging At: 2020-04-09 14:59:51
########################################################
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
########################################################
# Started Logging At: 2020-04-09 15:00:00
########################################################
########################################################
# # Started Logging At: 2020-04-09 15:00:01
########################################################
# This is a test to show what happens if you add lines vs. computing a single optical depth per channel
from pyspeckit.spectrum.models.ammonia_constants import (line_names, freq_dict, aval_dict, ortho_dict,
                                voff_lines_dict, tau_wts_dict)
from astropy import constants
from astropy import units as u
import pylab as pl

linename = 'oneone'

xarr_v = (np.linspace(-25,25,1000)*u.km/u.s)
xarr = xarr_v.to(u.GHz, u.doppler_radio(freq_dict['oneone']*u.Hz))
tauprof = np.zeros(xarr.size)
true_prof = np.zeros(xarr.size)
width = 0.1
xoff_v = 0
ckms = constants.c.to(u.km/u.s).value

pl.figure(figsize=(12,12))
pl.clf()
for ii,tau_tot in enumerate((0.001, 0.1, 1, 10,)):
    tau_dict = {'oneone':tau_tot}

    voff_lines = np.array(voff_lines_dict[linename])
    tau_wts = np.array(tau_wts_dict[linename])

    lines = (1-voff_lines/ckms)*freq_dict[linename]/1e9
    tau_wts = tau_wts / (tau_wts).sum()
    nuwidth = np.abs(width/ckms*lines)
    nuoff = xoff_v/ckms*lines

    # tau array
    tauprof = np.zeros(len(xarr))
    for kk,nuo in enumerate(nuoff):
        tauprof_ = (tau_dict[linename] * tau_wts[kk] *
                    np.exp(-(xarr.value+nuo-lines[kk])**2 /
                           (2.0*nuwidth[kk]**2)))

        tauprof += tauprof_
        true_prof += (1-np.exp(-tauprof_))

    ax = pl.subplot(4,1,ii+1)
    ax.plot(xarr_v, 1 - np.exp(-tauprof), label=str(tau_tot), zorder=20, linewidth=1)
    ax.plot(xarr_v, true_prof, label=str(tau_tot), alpha=0.7, linewidth=2)
    ax.plot(xarr_v, true_prof-(1-np.exp(-tauprof)) - tau_tot/20, linewidth=1)
    pl.title(str(tau_tot))
from astropy import units as u
from astropy import constants
freq = 23*u.GHz
def tau_wrong(tkin, tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tkin)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
def tau_right(tex):
    return (1-np.exp(-constants.h * freq/(constants.k_B*tex)))/(1+np.exp(-constants.h * freq/(constants.k_B*tex)))
tkin = np.linspace(5,40,101)*u.K
tex = np.linspace(5,40,100)*u.K
grid = np.array([[tau_wrong(tk,tx)/tau_right(tx) for tx in tex] for tk in tkin])
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.imshow(grid, cmap='hot', extent=[5,40,5,40])
pl.xlabel("Tex")
pl.ylabel("Tkin")
pl.colorbar()
pl.contour(tex, tkin, grid, levels=[0.75,1,1/0.75], colors=['w','w','k'])
#[Out]# <matplotlib.contour.QuadContourSet at 0x121374fd0>
def nunlnu_error(Tkin):
    return 1+np.exp(-constants.h * freq / (constants.k_B * Tkin))
pl.plot(tkin.value, nunlnu_error(tkin))
#[Out]# [<matplotlib.lines.Line2D at 0x1213ef990>]
from pyradex import Radex
from astropy import constants, units as u
R = Radex(species='p-nh3', column=1e13, collider_densities={'pH2':1e4}, temperature=20)
tbl = R(collider_densities={'ph2': 1e4}, temperature=20, column=1e13)
tbl[8:10]
#[Out]# <Table length=2>
#[Out]#        Tex                tau         ...         T_B        
#[Out]#         K                             ...          K         
#[Out]#      float64            float64       ...       float64      
#[Out]# ----------------- ------------------- ... -------------------
#[Out]# 6.789360524825584 0.09294143095281081 ...   0.358064436431466
#[Out]# 6.533403488783305 0.02126727244093209 ... 0.07952035764858055
# we're comparing the upper states since these are the ones that are emitting photons
trot = (u.Quantity(tbl['upperstateenergy'][8]-tbl['upperstateenergy'][9], u.K) *
        np.log((tbl['upperlevelpop'][9] * R.upperlevel_statisticalweight[8]) /
               (tbl['upperlevelpop'][8] * R.upperlevel_statisticalweight[9]))**-1
        )
trot
#[Out]# <Quantity 17.77691406 K>
tbl['Tex'][8:10].mean()
#[Out]# 6.661382006804445
dT_oneone = -(constants.h * u.Quantity(tbl['frequency'][8], u.GHz)/constants.k_B).to(u.K)
print("delta-T for 1-1_upper - 1-1_lower: {0}".format(dT_oneone))
tex = (dT_oneone *
        np.log((tbl['upperlevelpop'][8] * R.upperlevel_statisticalweight[8]) /
               (tbl['lowerlevelpop'][8] * R.upperlevel_statisticalweight[8]))**-1
        )
print("Excitation temperature computed is {0} and should be {1}".format(tex.to(u.K), tbl['Tex'][8]))
T0=tbl['upperstateenergy'][9]-tbl['upperstateenergy'][8]
T0
#[Out]# 41.18
def tr_swift(tk, T0=T0):
    return tk*(1+tk/T0 * np.log(1+0.6*np.exp(-15.7/tk)))**-1
tr_swift(20, T0=-41.18)
#[Out]# 22.662533151044173
tr_swift(20, T0=41.18)
#[Out]# 17.897313974001626
tr_swift(20, T0=41.5)
#[Out]# 17.91183463497009
def trot_radex(column=1e13, density=1e4, tkin=20):
    tbl = R(collider_densities={'ph2': density}, temperature=tkin, column=column)
    trot = (u.Quantity(tbl['upperstateenergy'][8]-tbl['upperstateenergy'][9], u.K) *
        np.log((tbl['upperlevelpop'][9] * R.upperlevel_statisticalweight[8]) /
               (tbl['upperlevelpop'][8] * R.upperlevel_statisticalweight[9]))**-1
        )
    return trot
trot_radex(tkin=20)
#[Out]# <Quantity 17.77691406 K>
def tex_radex(column=1e13, density=1e4, tkin=20, lineno=8):
    """ used in tests below """
    tbl = R(collider_densities={'ph2': density}, temperature=tkin, column=column)
    return tbl[lineno]['Tex']
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
cols = np.logspace(12,15)
trots = [trot_radex(column=c).to(u.K).value for c in cols]
pl.semilogx(cols, trots)
pl.hlines(tr_swift(20), cols.min(), cols.max(), color='k')
pl.xlabel("Column")
pl.ylabel("$T_{rot} (2-2)/(1-1)$")
#[Out]# Text(0, 0.5, '$T_{rot} (2-2)/(1-1)$')
densities = np.logspace(3,9)
trots = [trot_radex(density=n).to(u.K).value for n in densities]
pl.semilogx(densities, trots)
pl.hlines(tr_swift(20), densities.min(), densities.max(), color='k')
pl.xlabel("Volume Density")
pl.ylabel("$T_{rot} (2-2)/(1-1)$")
#[Out]# Text(0, 0.5, '$T_{rot} (2-2)/(1-1)$')
temperatures = np.linspace(5,40)
trots = [trot_radex(tkin=t).to(u.K).value for t in temperatures]
pl.plot(temperatures, trots)
# wrong pl.plot(temperatures, tr_swift(temperatures, T0=-41.18), color='k')
pl.plot(temperatures, tr_swift(temperatures, T0=41.18), color='r')
pl.xlabel("Temperatures")
pl.ylabel("$T_{rot} (2-2)/(1-1)$")
#[Out]# Text(0, 0.5, '$T_{rot} (2-2)/(1-1)$')
temperatures = np.linspace(5,40,50)
trots = [trot_radex(tkin=t).to(u.K).value for t in temperatures]
pl.plot(temperatures, np.abs(trots-tr_swift(temperatures, T0=41.18))/trots)
pl.xlabel("Temperatures")
pl.ylabel("$(T_{rot}(\mathrm{RADEX}) - T_{rot}(\mathrm{Swift}))/T_{rot}(\mathrm{RADEX})$")
#[Out]# Text(0, 0.5, '$(T_{rot}(\\mathrm{RADEX}) - T_{rot}(\\mathrm{Swift}))/T_{rot}(\\mathrm{RADEX})$')
from pyspeckit.spectrum.models.tests import test_ammonia
from pyspeckit.spectrum.models import ammonia
tkin = 20*u.K
trot = trot_radex(tkin=tkin)
print(trot)
spc = test_ammonia.make_synthspec(lte=False, tkin=None, tex=6.66, trot=trot.value, lines=['oneone','twotwo'])
spc.specfit.Registry.add_fitter('cold_ammonia',ammonia.cold_ammonia_model(),6)
spc.specfit(fittype='cold_ammonia', guesses=[23, 5, 13.1, 1, 0.5, 0],
            fixed=[False,False,False,False,False,True])

print("For Tkin={1} -> Trot={2}, pyspeckit's cold_ammonia fitter got:\n{0}".format(spc.specfit.parinfo, tkin, trot))
spc.specfit(fittype='cold_ammonia', guesses=[22.80, 6.6, 13.1, 1, 0.5, 0],
            fixed=[False,False,False,False,False,True])
bestfit_coldammonia_temperature = spc.specfit.parinfo[0]
print("The best fit cold ammonia temperature is {0} for an input T_rot={1}".format(bestfit_coldammonia_temperature, trot))
tex11 = tex_radex(tkin=tkin, lineno=8)
tex22 = tex_radex(tkin=tkin, lineno=9)
print("tex11={0}, tex22={1} for tkin={2}, trot={3}".format(tex11,tex22,tkin,trot))
spc = test_ammonia.make_synthspec(lte=False, tkin=None,
                                  tex={'oneone':tex11, 'twotwo':tex22},
                                  trot=trot.value,
                                  lines=['oneone','twotwo'])
spc.specfit.Registry.add_fitter('cold_ammonia',ammonia.cold_ammonia_model(),6)
spc.specfit(fittype='cold_ammonia', guesses=[23, 5, 13.1, 1, 0.5, 0],
            fixed=[False,False,False,False,False,True])

print("For Tkin={1} -> Trot={2}, pyspeckit's cold_ammonia fitter got:\n{0}"
      .format(spc.specfit.parinfo, tkin, trot))
print("The best fit cold ammonia temperature is {0} for an input T_rot={1}"
      .format(bestfit_coldammonia_temperature, trot))
tkin = 20*u.K
trot = trot_radex(tkin=tkin)
dT0=41.18
print(tkin * (1 + (tkin.value/dT0)*np.log(1 + 0.6*np.exp(-15.7/tkin.value)))**-1)
print("tkin={0} trot={1} tex11={2} tex22={3}".format(tkin, trot, tex11, tex22))

spc = test_ammonia.make_synthspec(lte=False, tkin=None,
                                  tex={'oneone':tex11, 'twotwo':tex22},
                                  trot=trot.value,
                                  lines=['oneone','twotwo'])
spc_666 = test_ammonia.make_synthspec(lte=False, tkin=None,
                                      tex=6.66,
                                      trot=trot.value,
                                      lines=['oneone','twotwo'])
# this one is guaranteed different because tex = trot
spc_cold = test_ammonia.make_synthspec_cold(tkin=tkin.value,
                                            lines=['oneone','twotwo'])
spc[0].plotter(linewidth=3, alpha=0.5)
spc_666[0].plotter(axis=spc[0].plotter.axis, clear=False, color='r', linewidth=1, alpha=0.7)
spc_cold[0].plotter(axis=spc[0].plotter.axis, clear=False, color='b', linewidth=1, alpha=0.7)
spc[0].data.max(), spc_666[0].data.max()
#[Out]# (0.14522377315518076, 0.14324530551193299)
spc[1].plotter()
spc_666[1].plotter(axis=spc[1].plotter.axis, clear=False, color='r')
spc_cold[1].plotter(axis=spc[1].plotter.axis, clear=False, color='b')
temperatures = np.linspace(5,40)
trots = [trot_radex(tkin=t).to(u.K).value for t in temperatures]
tex11s = np.array([tex_radex(tkin=t, lineno=8) for t in temperatures])
tex22s = np.array([tex_radex(tkin=t, lineno=9) for t in temperatures])
pl.plot(trots, tex11s)
pl.plot(trots, tex22s)
#pl.plot(tr_swift(temperatures), color='k')
pl.ylabel("$T_{ex}$")
pl.xlabel("$T_{rot} (2-2)/(1-1)$")
#[Out]# Text(0.5, 0, '$T_{rot} (2-2)/(1-1)$')
temperatures = np.linspace(5,40)
trots = [trot_radex(tkin=t).to(u.K).value for t in temperatures]
tex11s = np.array([tex_radex(tkin=t, lineno=8) for t in temperatures])
tex22s = np.array([tex_radex(tkin=t, lineno=9) for t in temperatures])
pl.plot(trots, tex11s/tex22s)
#pl.plot(tr_swift(temperatures), color='k')
pl.ylabel("$T_{ex} (2-2)/(1-1)$")
pl.xlabel("$T_{rot} (2-2)/(1-1)$")
#[Out]# Text(0.5, 0, '$T_{rot} (2-2)/(1-1)$')
from pyspeckit.spectrum.models.tests import test_ammonia
test_ammonia.test_ammonia_parlimits()
test_ammonia.test_ammonia_parlimits_fails()
test_ammonia.test_cold_ammonia()
test_ammonia.test_self_fit()
temperatures = np.array((10,15,20,25,30,35,40))
recovered_tkin = {}
recovered_column = {}
for tkin in temperatures:

    tbl = R(collider_densities={'ph2': 1e4}, temperature=tkin, column=1e13)
    tex11 = tbl['Tex'][8]
    tex22 = tbl['Tex'][9]
    trot = (u.Quantity(tbl['upperstateenergy'][8]-tbl['upperstateenergy'][9], u.K) *
            np.log((tbl['upperlevelpop'][9] * R.upperlevel_statisticalweight[8]) /
                   (tbl['upperlevelpop'][8] * R.upperlevel_statisticalweight[9]))**-1
            )

    spc = test_ammonia.make_synthspec(lte=False, tkin=None,
                                      tex={'oneone':tex11, 'twotwo':tex22},
                                      trot=trot.value,
                                      lines=['oneone','twotwo'])
    spc.specfit.Registry.add_fitter('cold_ammonia',ammonia.cold_ammonia_model(),6)
    spc.specfit(fittype='cold_ammonia', guesses=[23, 5, 13.1, 1, 0.5, 0],
                fixed=[False,False,False,False,False,True])
    
    recovered_tkin[tkin] = spc.specfit.parinfo['tkin0'].value
    recovered_column[tkin] = spc.specfit.parinfo['ntot0'].value
pl.xlabel("$T_K$")
pl.ylabel("Fitted $T_K$ from cold_ammonia")
pl.plot(recovered_tkin.keys(), recovered_tkin.values(), 'o')
pl.plot(temperatures, temperatures)
