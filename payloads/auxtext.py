

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
        #finally clause do not work with jyton
        #finally:
            #if f!=None:
                #f.close()
        return lines
#class