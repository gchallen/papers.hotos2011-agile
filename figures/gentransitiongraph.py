#!/usr/bin/env python

from components import components, generateEnsembles, matchEnsemble;
import re,sys,numpy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable,host_subplot

from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times'],'size':'10'})
rc('text', usetex=True)

Ps = ['P1','P2','P1.P2']
Ms = ['M1','M2','M1.M2']
Ss = ['','S1','S2','S1.S2']
Rs = ['','R1','R2','R1.R2']

orderedComponents = ['P1', 'P2', 'M1', 'M2', 'S1', 'S2', 'R1', 'R2']

componentColors = {'P1':'#E69999',
                   'P2':'#E69999',
                   'M1':'#FFCC99',
                   'M2':'#FFCC99',
                   'S1':'#CCFFCC',
                   'S2':'#CCFFCC',
                   'R1':'#C2D1F0',
                   'R2':'#C2D1F0'}

componentLabels = {'P1':'Processor',
                   'P2':'Processor',
                   'M1':'Memory',
                   'M2':'Memory',
                   'S1':'Storage',
                   'S2':'Storage',
                   'R1':'Radio',
                   'R2':'Radio'}

ensembles = generateEnsembles(Ps, Ms, Ss, Rs)

traceStart = 0.0
traceEnd = 0.0
traceResolution = 0.01
startLength = 1.0
endLength = 1.0
barSpace = 0.1
labelHeightCutoff = 50.0 / 1000.0
arrowTopLength = 210.0 / 1000
arrowBottomLength = 150.0 / 1000

# 13 Dec 2010 : GWA : First pass: read from file.

transitionFile = open(sys.argv[1], 'r')
transitions = []
commentFormat = re.compile(r'^\#.*')
transitionFormat = re.compile(r'(\w+)=(.*)')

for line in transitionFile:
  line = line.strip()
  if line == '':
    continue
  if commentFormat.match(line):
    continue
  transition = {}
  transition['usage'] = {}
  chunks = line.split(',')
  for chunk in chunks:
    transitionMatch = transitionFormat.search(chunk)
    if transitionMatch == None:
      continue
    transitionKey = transitionMatch.group(1)
    if transitionKey == 'T':
      transition['startTime'] = float(transitionMatch.group(2))
      traceEnd = transition['startTime']
    elif transitionKey == 'I':
      transition['endInputPower'] = float(transitionMatch.group(2)) / 1000.0
    elif transitionKey == 'S':
      queryComponentSet = set(transitionMatch.group(2).split('.'))
      transition['endEnsemble'] = matchEnsemble(queryComponentSet, ensembles)
    elif transitionKey == 'O':
      transition['estimatedOutputPower'] = float(transitionMatch.group(2)) / 1000.0
    else:
      if transitionKey not in transition['endEnsemble']['components']:
        print >>sys.stderr, "Bad component key"
        sys.exit(-1)
      component = transitionKey
      componentUsage = transitionMatch.group(2)
      if (componentUsage == 'max'):
        transition['usage'][component] = components[component]['maxPower'] / 1000.0
      elif (componentUsage == 'min'):
        transition['usage'][component] = components[component]['minPower'] / 1000.0
      elif (componentUsage == 'rest'):
        transition['usage'][component] = 'rest'
      else:
        transition['usage'][component] = float(componentUsage) / 1000.0
  transitions.append(transition)

traceEnd += endLength

# 13 Dec 2010 : GWA : Second pass: complete array and sanity check.

usedComponents = []

transitionIndex = 0
for transition in transitions:
  inputPower = transition['endInputPower']
  currentPower = 0.0
  numberRest = 0
  for component in transition['usage'].keys():
    if transition['usage'][component] != 'rest':
      currentPower += transition['usage'][component]
    else:
      numberRest += 1
  
  if numberRest > 1:
    print >>sys.stderr, "Too many rest components"
    sys.exit(-1)
  if numberRest == 1:
    for component in transition['usage'].keys():
      if transition['usage'][component] == 'rest':
        transition['usage'][component] = inputPower - currentPower
  
  currentPower = 0.0
  for component in transition['usage'].keys():
    currentPower += transition['usage'][component]
  if currentPower > inputPower:
    print >>sys.stderr, "Drawing more than input allows"
    sys.exit(-1)

  if transitionIndex == 0:
    transition['startInputPower'] = None
    transition['startOutputPower'] = None
    transition['startEnsemble'] = None
    transition['startString'] = ''
  else:
    transition['startInputPower'] = transitions[transitionIndex - 1]['endInputPower']
    transition['startOutputPower'] = transitions[transitionIndex - 1]['endOutputPower']
    transition['startEnsemble'] = transitions[transitionIndex - 1]['endEnsemble']
    transition['startString'] = transition['startEnsemble']['key']

  if transitionIndex < len(transitions) - 1:
    transition['endTime'] = transitions[transitionIndex + 1]['startTime']
  else:
    transition['endTime'] = traceEnd

  transition['endString'] = transition['endEnsemble']['key']

  currentPower = 0.0
  for component in transition['usage'].keys():
    if transition['usage'][component] > 0.0:
      usedComponents.append(component)
      usedComponents = list(set(usedComponents))
    currentPower += transition['usage'][component]
  transition['endOutputPower'] = currentPower

  transitionIndex += 1

# 13 Dec 2010 : GWA : Helper functions.

orderedComponents = [c for c in orderedComponents if c in usedComponents]

def generatePowerPoints(transitions, XPoints):
  transitionIndex = 0
  YPoints = []
  currentPower = transitions[0]['endInputPower']
  for xpoint in XPoints:
    if xpoint >= transitions[transitionIndex]['endTime']:
      if transitionIndex < len(transitions) - 1:
        transitionIndex += 1
        currentPower = transitions[transitionIndex]['endInputPower']
    YPoints.append(currentPower)
  return YPoints

def generateComponentPoints(transitions, component, XPoints, currentYPoints):
  transitionIndex = 0
  YPoints = []
  if transitions[0]['usage'].has_key(component):
    currentPower = transitions[0]['usage'][component]
  else:
    currentPower = 0.0
  for xpoint in XPoints:
    if xpoint >= transitions[transitionIndex]['startTime']:
      if transitionIndex < len(transitions) - 1:
        transitionIndex += 1
        if transitions[transitionIndex]['usage'].has_key(component):
          currentPower = transitions[transitionIndex]['usage'][component]
        else:
          currentPower = 0.0
    YPoints.append(currentPower)
  if currentYPoints != None:
    if len(currentYPoints) != len(YPoints):
      print >>sys.stderr, "YPoints length mismatch"
    for i in range(len(currentYPoints)):
      YPoints[i] += currentYPoints[i]
  return YPoints

def drawEnsembleBars(axes, transition, left, width, orderedComponents, componentColors, doLabels):
  bottom = 0.0
  outputPowerPercentage = 100
  transitionComponentCount = len(transition['usage'])
  for component in orderedComponents:
    if not transition['usage'].has_key(component):
      continue
    height = transition['usage'][component]
    if doLabels:
      label = r'{\footnotesize\bf %s}' % componentLabels[component]
    else:
      label = '__nolabel__'
    componentPercentage = int(round((transition['usage'][component] / transition['endOutputPower']) * 100.0))
    if transitionComponentCount == 1:
      componentPercentage = outputPowerPercentage
    outputPowerPercentage -= componentPercentage
    axes.bar(left + barSpace, height, width - (2 * barSpace), bottom, color=componentColors[component], edgecolor='black', linewidth=0.5, label=label)
    textX = left + (width / 2)
    textY = bottom + (height / 2) - 0.01
    if height > labelHeightCutoff:
      axes.text(textX, textY,
                (r'{\footnotesize{\bf %s} (%d\%%)}' % (component,
                                                       componentPercentage)),
                horizontalalignment='center', verticalalignment='center')
    else:
      arrowX = textX
      if bottom == 0.0:
        arrowY = 0.0
        textY = arrowY - arrowBottomLength - 0.005
      else:
        arrowY = bottom + height
        textY = arrowY + arrowTopLength
      axes.annotate((r'{\footnotesize{\bf %s} (%d\%%)}' % (component,
                                                           componentPercentage)),
                    xy = (arrowX, arrowY), xycoords='data',
                    xytext = (textX, textY), textcoords='data',
                    va='center', ha='center', annotation_clip=False,
                    bbox=dict(boxstyle="square", fc="w",lw=0.1),
                    arrowprops=dict(arrowstyle="-|>",
                                    connectionstyle="arc3",
                                    lw=0.1,
                                    fc="w"))

    bottom += height
    transitionComponentCount -= 1

# 13 Dec 2010 : GWA : Generate graph.


XPoints = numpy.arange(traceStart, traceEnd, traceResolution)
figure = plt.figure()
transitionAx = host_subplot(111)
#transitionAx.plot(XPoints, generatePowerPoints(transitions, XPoints), color='black', lw=2.0, ls="--", label=r'{\footnotesize \textbf{Available Power}}')

for i,transition in enumerate(transitions):
  doLabels = False
  if i == 6:
    doLabels = True
  drawEnsembleBars(transitionAx, transition, transition['startTime'], transition['endTime'] - transition['startTime'], orderedComponents, componentColors, doLabels)
  doLabels = False

'''YPoints = None
for component in orderedComponents:
  YPoints = generateComponentPoints(transitions, component, XPoints, YPoints)
  transitionAx.plot(XPoints, YPoints)'''

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

divider = make_axes_locatable(transitionAx)
labelAx = divider.append_axes("top", size=0.15, pad=0.0)
labelAx.set_xticks([])
labelAx.set_yticks([])
labelAx.axis([0, traceEnd, 0, 1.0])
textY = 0.5
labelAx.text(0.5, textY,
             r'{\small \bf Idle}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(1.0, color='black', linewidth=0.5)
transitionAx.axvline(1.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(2.0, textY,
             r'{\small \bf Background}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(3.0, color='black', linewidth=0.5)
transitionAx.axvline(3.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(5.0, textY,
             r'{\small \bf Interactive}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(7.0, color='black', linewidth=0.5)
transitionAx.axvline(7.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(7.5, textY,
             r'{\footnotesize \bf Background}',
             horizontalalignment='center', verticalalignment='center')
labelAx.axvline(8.0, color='black', linewidth=0.5)
transitionAx.axvline(8.0, color='black', ls=':', linewidth=0.1, zorder=-1)
labelAx.text(8.5, textY,
             r'{\small \bf Idle}',
             horizontalalignment='center', verticalalignment='center')

figure.subplots_adjust(left=0.08,right=0.995,top=0.995,bottom=0.13)
figure.set_size_inches(6.5,2.5)
figure.savefig('transitiongraph.pdf')
