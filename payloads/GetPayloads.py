#!/usr/bin/env python
# -*- coding: utf-8 -*-



from auxtext import AuxText


def loadPayloads(self,fileName):
    """This method loads the payloads for an attack from the specified file"""
    return self.auxText.readLines(fileName)