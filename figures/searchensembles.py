#!/usr/bin/env python

from components import components, generateEnsembles;
import sys

Ps = ['P1','P3','P1.P3']
Ms = ['M1','M3','M1.M3']
Ss = ['','S1','S2','S1.S2']
Rs = ['','R1','R3','R1.R3']

power = float(sys.argv[1])
efficiencySkew = 0.0
mustHave = None

if len(sys.argv) > 2:
  efficiencySkew = float(sys.argv[2])
if len(sys.argv) > 3:
  mustHave = str(sys.argv[3])

ensembles = generateEnsembles(Ps, Ms, Ss, Rs)
outputEnsembles = []
for ensemble in ensembles:
  powerRange = ensemble['maxPower'] - ensemble['minPower']
  minPower = ensemble['minPower'] - (powerRange * efficiencySkew)
  if minPower < 0.0:
    minPower = 0.0
  maxPower = ensemble['maxPower'] + (powerRange * efficiencySkew)
  if (maxPower > power) and (power > minPower):
    if (mustHave == None) or mustHave in ensemble[components]:
      ensemble['efficiency'] = power / ensemble['maxPower']
      outputEnsembles.append(ensemble)

def ensembleSortKey(ensemble):
  return abs(1 - ensemble['efficiency'])

outputEnsembles = sorted(outputEnsembles, key=ensembleSortKey)
for ensemble in outputEnsembles:
  print ensemble['key'], ensemble['maxPower'], ensemble['minPower'], ensemble['efficiency']

