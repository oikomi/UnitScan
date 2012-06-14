import sys
import re
import socket
import getopt
import os
import HTMLParser
import urllib
import urllib2
import httplib2
from bs4 import BeautifulSoup
import pycurl
import StringIO
import re
from bs4 import BeautifulSoup
from htmlentitydefs import name2codepoint as n2cp

class lswww:
  def __init__(self):
    self.current_form_method = "get"
    self.c = pycurl.Curl()
    self.b = StringIO.StringIO()
    self.verbose = 3
    self.liens = []
    self.forms = []
    self.form_values = {}
    self.inform = 0
    self.current_form_url = ""
    self.uploads = []
    self.current_form_method = "get"


  def __substitute_entity(self, match):
    ent = match.group(2)
    if match.group(1) == "#":
      return unichr(int(ent))
    else:
      cp = n2cp.get(ent)

      if cp:
        return unichr(cp)
      else:
        return match.group()   
    
  def __findTagAttributes(self, tag):
    attDouble = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*"(.*?)"[ +|>]', tag)
    attSingle = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*\'(.*?)\'[ +|>]', tag)
    attNone   = re.findall('<\w*[ ]| *(.*?)[ ]*=[ ]*["|\']?(.*?)["|\']?[ +|>]', tag)
    attNone.extend(attSingle)
    attNone.extend(attDouble)
    return attNone
    
  def __decode_htmlentities(self, string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(self.__substitute_entity, string)[0]

    
  def feed(self, htmlSource):
    htmlSource = htmlSource.replace("\n", "")
    htmlSource = htmlSource.replace("\r", "")
    htmlSource = htmlSource.replace("\t", "")

    links = re.findall('<a.*?>', htmlSource)
    linkAttributes = []
    for link in links:
      linkAttributes.append(self.__findTagAttributes(link))

    #Finding all the forms: getting the text from "<form..." to "...</form>"
    #the array forms will contain all the forms of the page
    forms = re.findall('<form.*?>.*?</form>', htmlSource)
    formsAttributes = []
    for form in forms:
      formsAttributes.append(self.__findTagAttributes(form))

    #Processing the forms, obtaining the method and all the inputs
    #Also finding the method of the forms
    inputsInForms    = []
    textAreasInForms = []
    selectsInForms   = []
    for form in forms:
      inputsInForms   .append(re.findall('<input.*?>', form))
      textAreasInForms.append(re.findall('<textarea.*?>', form))
      selectsInForms  .append(re.findall('<select.*?>', form))

    #Extracting the attributes of the <input> tag as XML parser
    inputsAttributes = []
    for i in range(len(inputsInForms)):
      inputsAttributes.append([])
      for inputt in inputsInForms[i]:
        inputsAttributes[i].append(self.__findTagAttributes(inputt))

    selectsAttributes = []
    for i in range(len(selectsInForms)):
      selectsAttributes.append([])
      for select in selectsInForms[i]:
        selectsAttributes[i].append(self.__findTagAttributes(select))

    textAreasAttributes = []
    for i in range(len(textAreasInForms)):
      textAreasAttributes.append([])
      for textArea in textAreasInForms[i]:
        textAreasAttributes[i].append(self.__findTagAttributes(textArea))

    if(self.verbose == 2):
      #print "\n\n" + _("Forms")
      print "====="
      for i in range(len(forms)):
        print _("Form") + " " + str(i)
        tmpdict = {}
        for k, v in dict(formsAttributes[i]).items():
          tmpdict[k.lower()] = v
        print " * " + _("Method") + ":  " + self.__decode_htmlentities(tmpdict['action'])
        print " * " + _("Intputs") + ": "
        for j in range(len(inputsInForms[i])):
          print "    + " + inputsInForms[i][j]
          for att in inputsAttributes[i][j]:
            print "       - " + str(att)
        print " * " + _("Selects") + ": "
        for j in range(len(selectsInForms[i])):
          print "    + " + selectsInForms[i][j]
          for att in selectsAttributes[i][j]:
            print "       - " + str(att)
        print " * " + _("TextAreas")+": "
        for j in range(len(textAreasInForms[i])):
          print "    + " + textAreasInForms[i][j]
          for att in textAreasAttributes[i][j]:
            print "       - " + str(att)
      print "\n"+_("URLS")
      print "===="

    for i in range(len(links)):
      tmpdict = {}
      for k, v in dict(linkAttributes[i]).items():
        tmpdict[k.lower()] = v
      if "href" in tmpdict.keys():
        self.liens.append(self.__decode_htmlentities(tmpdict['href']))
        if(self.verbose == 3):
          print self.__decode_htmlentities(tmpdict['href'])

    for i in range(len(forms)):
      tmpdict = {}
      for k, v in dict(formsAttributes[i]).items():
        tmpdict[k.lower()] = v
      self.form_values = {}
      if "action" in tmpdict.keys():
        self.liens.append(self.__decode_htmlentities(tmpdict['action']))
        self.current_form_url = self.__decode_htmlentities(tmpdict['action'])

      # Forms use GET method by default
      self.current_form_method = "get"
      if "method" in tmpdict.keys():
        if tmpdict["method"].lower() == "post":
          self.current_form_method = "post"

      for j in range(len(inputsAttributes[i])):
        tmpdict = {}
        for k, v in dict(inputsAttributes[i][j]).items():
          tmpdict[k.lower()] = v
          if "type" not in tmpdict.keys():
            tmpdict["type"] = "text"
          if "name" in tmpdict.keys():
            if tmpdict['type'].lower() in \
              ['text', 'password', 'radio', 'checkbox', 'hidden',
                  'submit', 'search']:
              # use default value if present or set it to 'on'
              if "value" in tmpdict.keys():
                if tmpdict["value"] != "": val = tmpdict["value"]
                else: val = "on"
              else: val = "on"
              self.form_values.update(dict([(tmpdict['name'], val)]))
            if tmpdict['type'].lower() == "file":
              self.uploads.append(self.current_form_url)

      for j in range(len(textAreasAttributes[i])):
        tmpdict = {}
        for k, v in dict(textAreasAttributes[i][j]).items():
          tmpdict[k.lower()] = v
        if "name" in tmpdict.keys():
          self.form_values.update(dict([(tmpdict['name'], 'on')]))

      for j in range(len(selectsAttributes[i])):
        tmpdict = {}
        for k, v in dict(selectsAttributes[i][j]).items():
          tmpdict[k.lower()] = v
        if "name" in tmpdict.keys():
          self.form_values.update(dict([(tmpdict['name'], 'on')]))

      if self.current_form_method == "post":
        self.forms.append((self.current_form_url, self.form_values))
      else:
        l = ["=".join([k, v]) for k, v in self.form_values.items()]
        l.sort()
        self.liens.append(self.current_form_url.split("?")[0] + "?" + "&".join(l))
        
  def getContent(self,url):
    self.c.setopt(pycurl.URL,url)
    self.c.setopt(pycurl.WRITEFUNCTION, self.b.write)
    self.c.setopt(pycurl.MAXREDIRS, 5) 
    self.c.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
    self.c.perform()
    return self.b.getvalue()

ls=lswww()
uu = ls.getContent('http://history.sysu.edu.cn/archive/login.php')
ls.feed(uu)


        