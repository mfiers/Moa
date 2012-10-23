"""
Moa script helper
"""

import os
import yaml

def getArgs():
    if not os.path.exists('.moa/template'):
        return {}
    with open('.moa/template') as F:
        templateData = yaml.load(F)
    filesets = templateData.get('filesets', {}).keys()

    rv = {}
    for a in os.environ.keys():
        if a[:4] != 'moa_': continue
        ky = a[4:]
        va = os.environ[a]
        if '_files' in ky and ky[:-6] in filesets:
            va = va.split()

        rv[ky] = va
    return rv
