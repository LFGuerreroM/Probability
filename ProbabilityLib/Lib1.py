import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats
import pymc3 as pm
import pickle

def savetracePYMC(name, trace,ppc = None):
  datos = [trace,ppc]
  f = open(name+'.pckl','wb')
  pickle.dump(datos,f)
  f.close()

def loadtracePYMC(name):
  f = open(name+'.pckl','rb')
  datos = pickle.load(f)
  f.close()
  trace = datos[0]
  ppc = datos[1]
  return trace,ppc

def plot_posterior(trace, varnames = None,  burn = None, fontsize=12, figsize=None, ylabel='Probability'):
  if figsize==None:
    figsize = (8,14)
  if varnames is None:
    varnames = trace.varnames
  fig, ax = plt.subplots(len(varnames), 1,figsize=figsize, gridspec_kw={'width_ratios': [1]},constrained_layout=True,)  
  for i in range(len(varnames)):
    ax[i].hist(dataframe[varnames[i]], bins=50, density=True, alpha=0.5, color='black', label='Posterior')
    ax[i].set_ylabel('$'+ylabel+'$',fontsize=fontsize)
    ax[i].set_title('$'+varnames[i]+'$',fontsize=fontsize)
    ax[i].locator_params(tight=True, nbins=4) 
  fig.tight_layout(pad=0.4)
  fig.align_ylabels(ax[:, :])
  return fig, ax

def plottrace(trace, burn = 500 ,fontsize=12,figsize=None, plotsamples=True,chains=None,ylabel='Probability'):
  if figsize==None:
    figsize = (8,14)
  if plotsamples:
    nf = len(param)
    nc = 2
    wratios = [1.6, 1]
  else:
    nc = 4
    nf = 2
    wratios = [1, 1, 1, 1]
  if chains==None:
    chains=trace.chains
  fig, ax = plt.subplots(nf, nc,figsize=figsize, gridspec_kw={'width_ratios': wratios},constrained_layout=True,)  
  titles = ['E [MPa]', '\sigma_y [MPa]', '\epsilon_{sh}', '\epsilon_u', 'C_1', 'E_y [MPa]', '\sigma_u [MPa]','stds [MPa]']
  param =['E_', 'fy_', 'esh_', 'eu_', 'C1_', 'Ey_', 'fu_','chol_stds']
  lt = ['-','--',':','-.']
  cm = plt.cm.tab20c(np.linspace(0,1,20))
  fi = 0
  ci = -1
  for i in range(len(param)):
    val = 1
    smin, smax = 10e10,0  
    if plotsamples:
      fi = i
      ci = 0
    else:
      if i==4:
        fi = 1
        ci = -1
      ci = ci +1
    for  chain in chains:     
      samples = trace.get_values(varname=param[i],chains=chain,burn=burn) 
      if param[i]=='chol_stds':
        val = 3
        sam = samples    
      for val_i in range(val):
        if val>1:
          samples = sam.transpose()[val_i]
        smin2, smax2 = np.min(samples), np.max(samples)
        if smin2 < smin:
          smin = smin2
        if smax2 > smax:
          smax = smax2
        x = np.linspace(smin, smax, 80)
        y = stats.gaussian_kde(samples)(x)
        ax[fi,ci].plot(x, y,lt[chain],color = cm[chain+val_i*4])
        if (smax-smin)<0.001:
          ax[fi,ci].set_xticks(np.linspace(smin, smax, 4),fontsize=fontsize-2) 
        else:
          ax[fi,ci].set_xticks(np.linspace(smin, smax, 5),fontsize=fontsize-2) 
        if plotsamples:
          ax[fi,1].plot(samples,lt[chain],linewidth=.7,alpha=.7,color = cm[chain+val_i*4])
      ax[fi,ci].set_ylabel('$'+ylabel+'$',fontsize=fontsize,)

    ax[fi,ci].get_yaxis().set_visible(False)
    ax[fi,ci].set_title('$'+titles[i]+'$',fontsize=fontsize)
    ax[fi,ci].locator_params(tight=True, nbins=4) 
    if plotsamples:
      ax[fi,1].set_ylabel('Sample value',fontsize=fontsize-2)
      ax[fi,1].set_title('$'+titles[i]+'$',fontsize=fontsize)
    
  fig.tight_layout(pad=0.4)
  fig.align_ylabels(ax[:, :])
  
  return fig, ax

def version():
  print('ProbabilityLib version = 0.0.2a')



def trace_to_df(trace,varnames = None, sample = 1000):
  if varnames is None:
    varnames = trace.varnames
  dataframe = pm.trace_to_dataframe(trace,varnames = varnames)[-sample:]
  dataframe.rename(columns={'E_': '$E [MPa]$', 'fy_':'$f_y[MPa]$', 'esh_':'$\epsilon_{sh}$',
                            'eu_':'$\epsilon_u$', 'C1_':'$C_1$', 'Ey_':'$E_y[MPa]$', 
                            'fu_':'$f_u[MPa]$','chol_stds__0':'$chol-\sigma_0$', 'chol_stds__1':'$chol-\sigma_1$', 'chol_stds__2':'$chol-\sigma_2$'},inplace=True)
  return dataframe


def sca_matrix_plot(trace, sample = 1000, figsize=(9,9), fonsize=12):
  keys = ['E_', 'fy_', 'esh_', 'eu_', 'C1_', 'Ey_', 'fu_','chol_stds']
  dataframe = pm.trace_to_dataframe(trace,varnames = keys)[-sample:]
  dataframe.rename(columns={'E_': '$E [MPa]$', 'fy_':'$f_y[MPa]$', 'esh_':'$\epsilon_{sh}$',
                            'eu_':'$\epsilon_u$', 'C1_':'$C_1$', 'Ey_':'$E_y[MPa]$', 
                            'fu_':'$f_u[MPa]$','chol_stds__0':'$chol-\sigma_0$', 'chol_stds__1':'$chol-\sigma_1$', 'chol_stds__2':'$chol-\sigma_2$'},inplace=True)
  #scatter_matrix(dataframe, figsize=figsize,grid=True,alpha=0.25)
  fig = plt.gcf()
  fig.align_labels() 
  return dataframe