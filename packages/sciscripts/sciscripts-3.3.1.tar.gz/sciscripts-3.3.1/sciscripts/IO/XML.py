# -*- coding: utf-8 -*-
"""

:Author: T. Malfatti <malfatti@disroot.org>

:Date: 20170704

:License: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>

:Homepage: https://gitlab.com/Malfatti/SciScripts

Functions for loading xml files as dictionaries.
"""

from copy import copy
from xml.etree import ElementTree

def Root2Dict(El):
    Dict = {}
    if El.getchildren():
        for SubEl in El:
            if SubEl.keys():
                if SubEl.get('name'):
                    if SubEl.tag not in Dict: Dict[SubEl.tag] = {}
                    Dict[SubEl.tag][SubEl.get('name')] = Root2Dict(SubEl)

                    Dict[SubEl.tag][SubEl.get('name')].update(
                        {K: SubEl.get(K) for K in SubEl.keys() if K != 'name'}
                    )

                else:
                    Dict[SubEl.tag] = Root2Dict(SubEl)
                    Dict[SubEl.tag].update(
                        {K: SubEl.get(K) for K in SubEl.keys() if K != 'name'}
                    )

            else:
                if SubEl.tag not in Dict: Dict[SubEl.tag] = Root2Dict(SubEl)
                else:
                    No = len([k for k in Dict if SubEl.tag in k])
                    Dict[SubEl.tag+'_'+str(No+1)] = Root2Dict(SubEl)

        return(Dict)
    else:
        if El.items(): return(dict(El.items()))
        else: return(El.text)


def dictify(r,root=True):
    """
    Taken from Erik Aronesty, 2015-06-18
    @ https://stackoverflow.com/a/30923963
    """
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d


def ReadTree(File):
    Tree = ElementTree.parse(File)
    Root = Tree.getroot()
    return(Tree, Root)

## Level 1
def Read(File):
    Root = ReadTree(File)[1]
    # Info = Root2Dict(Root)
    Info = dictify(Root)
    return(Info)

