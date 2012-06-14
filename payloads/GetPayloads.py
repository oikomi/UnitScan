#!/usr/bin/env python
# -*- coding: utf-8 -*-



from auxtext import AuxText


def loadPayloads(fileName):
    """This method loads the payloads for an attack from the specified file"""
    auxText = AuxText()
    print auxText.readLines(fileName)
    return auxText.readLines(fileName)

def getloads():
    return loadPayloads('xssPayloads.txt')


if __name__ == "__main__":
    getloads()


