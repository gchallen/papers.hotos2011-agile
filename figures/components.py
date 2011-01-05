import itertools

components = { 
  'P1':{'name':'ARM Cortex-M3',
        'key':'P1',
        'minPower':0.9,
        'maxPower':15.6},
  'P3':{'name':'ARM Cortex-A9',
        'key':'P3',
        'minPower':23.5,
        'maxPower':400},
  'M1':{'name':'32MB ISSI SDRAM',
        'key':'M1',
        'minPower':81,
        'maxPower':108},
  'M3':{'name':'1GB Micron "Slow" DDR2',
        'key':'M3',
        'minPower':322,
        'maxPower':482},
  'S1':{'name':'2GB MicroSD Card',
        'key':'S1',
        'minPower':20,
        'maxPower':100},
  'S2':{'name':'64GB OCZ SSD',
        'key':'S2',
        'minPower':200,
        'maxPower':1000},
  'R1':{'name':'250 kbps TI CC2540 BLE',
        'key':'R1',
        'minPower':6.6,
        'maxPower':66.3},
  'R3':{'name':'11 Mbps Marvell 88W8686 802.11bg',
        'key':'R3',
        'minPower':30.9,
        'maxPower':309.3},
}

def generateEnsembles(Ps, Ms, Ss, Rs):
  ensembles = []
  for componentEnsemble in itertools.product(Ps, Ms, Ss, Rs):
    componentEnsemble = [c for c in componentEnsemble if c != '']
    ensembleString = '.'.join(componentEnsemble)
    componentEnsemble = ensembleString.split('.')
    minPower = 0.0
    maxPower = 0.0
    for component in componentEnsemble:
      minPower += components[component]['minPower']
      maxPower += components[component]['maxPower']
    ensemble = {'key':ensembleString, 'minPower':minPower, 'maxPower':maxPower, 'components':componentEnsemble}
    ensembles.append(ensemble)
  return ensembles

def matchEnsemble(queryComponentSet, ensembles):
  for ensemble in ensembles:
    componentSet = set(ensemble['components'])
    if queryComponentSet == componentSet:
      return ensemble

def subsetEnsemble(queryComponentSet, ensembles):
  outputEnsembles = []
  for ensemble in ensembles:
    componentSet = set(ensemble['components'])
    if queryComponentSet.issubset(componentSet):
      outputEnsembles.append(ensemble)
  return outputEnsembles
