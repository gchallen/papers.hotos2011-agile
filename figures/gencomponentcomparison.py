#!/usr/bin/env python

from components import components, generateEnsembles, matchEnsemble;
import re,sys,numpy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable,host_subplot

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times'],'size':'10'})
rc('text', usetex=True)

orderedComponents = ['P1', 'P2', 'M1', 'M2', 'S1', 'S2', 'R1', 'R2']

componentColors = {'P1':'#E69999',
                   'P2':'#E69999',
                   'M1':'#FFCC99',
                   'M2':'#FFCC99',
                   'S1':'#CCFFCC',
                   'S2':'#CCFFCC',
                   'R1':'#C2D1F0',
                   'R2':'#C2D1F0'}

barSpace = 0.1
barWidth = 1.0

figure = plt.figure()
componentAx = host_subplot(111)

for i,component in enumerate(orderedComponents):
  bottom = components[component]['minPower']
  height = components[component]['maxPower'] - components[component]['minPower']
  componentAx.bar(i + barSpace, height, barWidth - (2 * barSpace), bottom, color=componentColors[component], edgecolor='black', linewidth=0.5, label='__nolabel__')

handles, labels = transitionAx.get_legend_handles_labels()
handles = handles[0:1] + handles[1::][::-1]
labels = labels[0:1] + labels[1::][::-1]
transitionLegend = transitionAx.legend(handles, labels, loc='upper left', labelspacing=0.05)
transitionLegend.get_frame().set_linewidth(0.1)
transitionAx.axis([0, traceEnd, 0, 1.6])

transitionYTicks = numpy.arange(0.25, 1.75, 0.25)
transitionAx.set_yticks(transitionYTicks)
transitionAx.set_yticklabels([(r'{\normalsize %.2f}' % t) for t in transitionYTicks])
for Ygrid in transitionYTicks:
  transitionAx.axhline(Ygrid, color='black', ls=':', linewidth=0.1, zorder=-1)

transitionXTicks = numpy.arange(1, 9, 1)
transitionAx.set_xticks(transitionXTicks)
transitionAx.set_xticklabels([(r'{\normalsize %d}' % t) for t in transitionXTicks])

transitionAx.set_xlabel(r'{\bf Time}')
transitionAx.set_ylabel(r'{\bf Power (W)}')

divider = make_axes_locatable(componentAx)
labelAx = divider.append_axes("top", size=0.15, pad=0.0)
labelAx.set_xticks([])
labelAx.set_yticks([])
labelAx.axis([0, len(orderedComponents), 0, 1.0])
textY = 0.5
labelAx.text(1.0, textY,
             r'{\small \bf Idle}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(2.0, color='black', linewidth=0.5)
componentAx.axvline(2.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(3.0, textY,
             r'{\small \bf Background}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(4.0, color='black', linewidth=0.5)
componentAx.axvline(4.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(5.0, textY,
             r'{\small \bf Interactive}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(6.0, color='black', linewidth=0.5)
componentAx.axvline(6.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(7.0, textY,
             r'{\footnotesize \bf Background}',
             horizontalalignment='center', verticalalignment='center')

figure.subplots_adjust(left=0.08,right=0.995,top=0.995,bottom=0.13)
figure.set_size_inches(6.5,2.5)
figure.savefig('componentcomparison.pdf')
