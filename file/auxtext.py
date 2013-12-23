#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AuxText:
    """Class for reading and writing in text files"""
    def readLines(self,fileName):
        """returns a array"""
        lines = []
        f = None
        try:
            f = open(fileName)
            for line in f:
                cleanLine = line.strip(" \n")
                if cleanLine != "":
                    lines.append(cleanLine.replace("\\0","\0"))
        except IOError,e:
            print e

        #finally:
            #if f!=None:
                #f.close()
        return lines
#class

if __name__ == "__main__":
    try:
        l = AuxText()
        ll = l.readLines("./config/execPayloads.txt")
        for li in ll:
            print li
    except SystemExit:
        pass
