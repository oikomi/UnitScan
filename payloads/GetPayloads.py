#!/usr/bin/env python
# -*- coding: utf-8 -*-



from auxtext import AuxText


def loadPayloads():
    """This method loads the payloads for an attack from the specified file"""
    auxText = AuxText()
    print auxText.readLines('/home/unitscan/UnitScan/payloads/xssPayloads.txt')
    return auxText.readLines('/home/unitscan/UnitScan/payloads/xssPayloads.txt')

def getloads():
    return loadPayloads('xssPayloads.txt')




