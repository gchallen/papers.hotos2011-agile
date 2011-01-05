#!/usr/bin/env python

from components import components, generateEnsembles, subsetEnsemble;
import sys

Ps = ['P1','P3','P1.P3']
Ms = ['M1','M3','M1.M3']
Ss = ['','S1','S2','S1.S2']
Rs = ['','R1','R3','R1.R3']

componentSet = set('.'.join([c for c in Ps + Ms + Ss + Rs if c != '']).split('.'))
queryComponentSet = set('.'.join(sys.argv[1:]).split('.'))
if not queryComponentSet.issubset(componentSet):
  sys.exit(-1)

ensembles = generateEnsembles(Ps, Ms, Ss, Rs)
outputEnsembles = subsetEnsemble(queryComponentSet, ensembles)
outputEnsembles = sorted(outputEnsembles, key=lambda ensemble: len(ensemble['components']))
for ensemble in outputEnsembles:
  print ensemble['key'], ensemble['maxPower'], ensemble['minPower']
