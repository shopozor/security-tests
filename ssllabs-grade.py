# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:54:10 2019

@author: tm
"""


import os
from subprocess import Popen, PIPE
import sys
import re


if(len(sys.argv) < 2):
    print("Error, please specify the domain on which to run the check, e.g.: python", sys.argv[0] + " https://www.softozor.ch")    
else:
    try:
        ssllabs = os.environ['ssllabs-scan'];
        program = os.path.join(ssllabs, "ssllabs-scan")
        print(program)
        
        p = Popen([program, "--grade", "--json-flat", "--verbosity", "error", sys.argv[1]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        
        print("output=", output)
        print("err=", err)
        print("exit_code=", rc)
        
        if(rc == 0):
            my_data = output.decode('utf8').replace("'", '"')
            start = my_data.find("\n", my_data.find("HostName")) #skip hostname
            my_data = my_data[start:]
            my_data = my_data[my_data.find("\""):] #skip line returns at the start of the file
            my_data = my_data[:my_data.rfind("\"")+1]#skip line returns at the end of the file
            allMarks = re.findall("\".*\":\"(.?.?)\"", my_data)
            minMark = ord('A') # the smaller the value, the better, e.g. A=65, F=70
            for mark in allMarks:
                if len(mark) == 1 and ord(mark) > minMark:
                    minMark = ord(mark)
            print(chr(minMark))
        else:
            print("An error occurred during the ssllabs-scan processing:")
            print(output)
            print(err)
            
    except KeyError:
        print("environement key ssllabs-scan cannot be found. You need to download and build this project https://github.com/ssllabs/ssllabs-scan/ and then set an environment variable named ssllabs-scan that points to the directory where the ssllabs-scan binary was built.")
    