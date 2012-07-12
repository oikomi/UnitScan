#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,string


# read config file
cf = ConfigParser.ConfigParser()  
cf.read("config.cfg")  
log_level = cf.get("LOG", "LOG_LEVEL")  

print log_level