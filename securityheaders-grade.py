# -*- coding: utf-8 -*-

import requests
import sys


if(len(sys.argv) < 2):
    print("Error, please specify the domain on which to run the check, e.g.: python", sys.argv[0] + " https://www.softozor.ch")
else:
    #print("Running test against: ", sys.argv[1])
    res = requests.get('https://securityheaders.com/?q='+sys.argv[1]+'&followRedirects=on')
    print(res.headers['X-Grade'])
