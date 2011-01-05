#!/usr/bin/env python

from components import components, generateEnsembles;
import re,sys,numpy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable,host_subplot

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times'],'size':'10'})
rc('text', usetex=True)

sidebarwidth = 0.8

Ps = ['P1','P2','P1.P2']
Ms = ['M1','M2','M1.M2']
Ss = ['','S1','S2','S1.S2']
Rs = ['','R1','R2','R1.R2']

ensembles = generateEnsembles(Ps, Ms, Ss, Rs)

def ensembleCmp(a,b):
  if a['maxPower'] != b['maxPower']:
    return cmp(a['maxPower'], b['maxPower'])
  else:
    return cmp(a['minPower'], b['minPower'])

ensembles = sorted(ensembles, cmp=ensembleCmp)

componentAxXticks = []
left = 0
for ensemble in ensembles:
  ensemble['left'] = left
  left += 1
Xmax = left

orderedComponents = ['P1', 'P2', 'M1', 'M2', 'S1', 'S2', 'R1', 'R2']
orderedComponents.reverse()
componentAxYticks = []
bottom = 0
for component in orderedComponents:
  components[component]['bottom'] = bottom
  componentAxYticks.append(bottom + 0.5)
  bottom += 1
componentAxYmax = bottom

figure = plt.figure()
powerAx = host_subplot(111)
Xgrids = range(12,144,12)

Ymax = 0.0
legendDone = False
for ensemble in ensembles:
  left = ensemble['left']
  bottom = ensemble['minPower'] / 1000.0
  top = ensemble['maxPower'] / 1000.0
  height = top - bottom
  secondbottom = top - ((1.0 - sidebarwidth) * height)
  secondheight = top - secondbottom
  height = height - secondheight
  if ensemble['maxPower'] > Ymax:
    powerAxYmax = ensemble['maxPower'] / 1000.0
  if not legendDone:
    secondlabel = r'{\footnotesize \textbf{Efficient} Ensemble Power Range}'
    label = r'{\footnotesize \textbf{Total} Ensemble Power Range}'
    legendDone = True
  else:
    secondlabel = label = '__nolabel__'
  powerAx.bar(left, secondheight, 1, secondbottom, color='blue', edgecolor='blue', linewidth=0.1, label=secondlabel)
  powerAx.bar(left, height, 1, bottom, color='#C2D1F0', edgecolor='#C2D1F0', linewidth=0.1, label=label)

powerAx.set_xticks([])
powerAxYticks = numpy.arange(0.5,3.0,0.5)
powerAx.set_yticks(powerAxYticks)
powerAx.set_yticklabels([(r'{\small %s}' % p) for p in powerAxYticks])
powerLegend = powerAx.legend(loc='upper left')
powerLegend.get_frame().set_linewidth(0.1)
for Xgrid in Xgrids:
  powerAx.axvline(Xgrid, color='black', ls='--', linewidth=0.1)
powerAx.axis([0, Xmax, 0, 2.5])
powerAx.set_ylabel(r'{\bf \small Power (W)}')

statesAx = powerAx.twinx()
statesAxYticks = numpy.arange(0.25,2.5,0.25)
statesAxYlabels = []
for Ygrid in statesAxYticks:
  count = 0
  for ensemble in ensembles:
    if ((ensemble['maxPower'] / 1000.0) > Ygrid) and (Ygrid > (ensemble['minPower'] / 1000.0)):
      count += 1
  statesAxYlabels.append(count)
statesAx.set_yticks(statesAxYticks)
statesAx.set_yticklabels([(r'{\small %d}' % l) for l in statesAxYlabels])
statesAx.axis([0, Xmax, 0, 2.5])

statesAx.set_yticks(statesAxYticks)
for Ygrid in statesAxYticks:
  statesAx.axhline(Ygrid, color='black', ls=':', linewidth=0.1)
statesAx.set_ylabel(r'{\bf \small Total Possible Ensembles}')

divider = make_axes_locatable(powerAx)
componentAx = divider.append_axes("bottom", size=0.75, pad=0.0, sharex=powerAx)

for ensemble in ensembles:
  left = ensemble['left']
  for component in ensemble['components']:
    bottom = components[component]['bottom']
    componentAx.bar(left, 1, 1, bottom, color='0.50', edgecolor='0.50', linewidth=0.1)

componentAx.set_xticks([])
componentAx.set_yticks(componentAxYticks)
componentAx.set_yticklabels([(r'{\scriptsize %s}' % o) for o in orderedComponents])
for Xgrid in Xgrids:
  componentAx.axvline(Xgrid, color='black', linewidth=0.1)
for Ygrid in componentAxYticks:
  componentAx.axhline(Ygrid - 0.5, color='black', linewidth=0.1)
componentAx.axis([0, Xmax, 0, componentAxYmax])
for tick in componentAx.get_yticklines():
  tick.set_visible(False)
componentAx.set_xlabel(r'{\bf \small Component Ensemble}')
componentAx.set_ylabel(r'{\bf \small Component}')

figure.subplots_adjust(left=0.07,right=0.93,top=0.98,bottom=0.08)
figure.set_size_inches(6.5,2.5)
figure.savefig('componentgraph.pdf')
