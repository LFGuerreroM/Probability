import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

def plottrace(trace, burn = 500 ,fontsize=12,figsize=(8,14) , titles = None):
  fig, ax = plt.subplots(8, 2,figsize=figsize, gridspec_kw={'width_ratios': [1.6, 1]})  # ,sharex=True, sharey=True)
  param =['E_', 'fy_', 'esh_', 'eu_', 'C1_', 'Ey_', 'fu_','chol_stds']
  lt = ['-','--',':','-.']
  cm = plt.cm.tab20c(np.linspace(0,1,20))
  for i in range(len(param)):
    val = 1
    smin, smax = 10e10,0  
    for  chain in trace.chains:     
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
        ax[i,0].plot(x, y,lt[chain],color = cm[chain+val_i*4])
        if (smax-smin)<0.001:
          ax[i,0].set_xticks(np.linspace(smin, smax, 4)) 
        else:
          ax[i,0].set_xticks(np.linspace(smin, smax, 5)) 
        ax[i,1].plot(samples,lt[chain],linewidth=.7,alpha=.7,color = cm[chain+val_i*4])
    ax[i,0].get_yaxis().set_visible(False)
    ax[i,0].set_ylabel('Frequency',fontsize=fontsize)
    ax[i,1].set_ylabel('Sample value',fontsize=fontsize-2)
    ax[i,0].set_title('$'+titles[i]+'$',fontsize=fontsize)
    ax[i,1].set_title('$'+titles[i]+'$',fontsize=fontsize)
    ax[i,0].set_ylabel('Frequency',fontsize=fontsize)
    
  fig.tight_layout()
  fig.align_ylabels(ax[:, 1])
  return fig, ax

def version():
  print('ProbabilityLib version = 0.0.1')

def sca_matrix_plot(trace, sample = 1000, figsize=(9,9), fonsize=12):
  keys = ['E_', 'fy_', 'esh_', 'eu_', 'C1_', 'Ey_', 'fu_','chol_stds']
  dataframe = pm.trace_to_dataframe(trace,varnames = keys)[-sample:]
  dataframe.rename(columns={'E_': '$E [MPa]$', 'fy_':'$f_y[MPa]$', 'esh_':'$\epsilon_{sh}$',
                            'eu_':'$\epsilon_u$', 'C1_':'$C_1$', 'Ey_':'$E_y[MPa]$', 
                            'fu_':'$f_u[MPa]$','chol_stds__0':'$chol-\sigma_0$', 'chol_stds__1':'$chol-\sigma_1$', 'chol_stds__2':'$chol-\sigma_2$'},inplace=True)
  scatter_matrix(dataframe, figsize=figsize,grid=True,alpha=0.25)
  fig = plt.gcf()
  fig.align_labels() 
  return dataframe

def trace_to_df(trace,varnames = None, sample = 1000):
  if varnames is None:
    varnames = trace.varnames
  dataframe = pm.trace_to_dataframe(trace,varnames = varnames)[-sample:]
  dataframe.rename(columns={'E_': '$E [MPa]$', 'fy_':'$f_y[MPa]$', 'esh_':'$\epsilon_{sh}$',
                            'eu_':'$\epsilon_u$', 'C1_':'$C_1$', 'Ey_':'$E_y[MPa]$', 
                            'fu_':'$f_u[MPa]$','chol_stds__0':'$chol-\sigma_0$', 'chol_stds__1':'$chol-\sigma_1$', 'chol_stds__2':'$chol-\sigma_2$'},inplace=True)
  return dataframe
