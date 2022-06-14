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

def prueba():
  print('Sirve')
  