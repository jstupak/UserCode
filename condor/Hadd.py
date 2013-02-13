from os import environ

#inputPathBase='/uscms_data/d1/jstupak/chargedHiggs'
#inputPathBase=environ["PWD"]

#-----------------------------------------------------

import os
import re
import glob
import sys
from glob import glob
from LJMet.Com.Sample import allSamples
import os

if len(sys.argv)>1: inputDir=sys.argv[1]
else: raise Exception("No input directory specified")

outputDir = inputDir

################################################################

for dir in glob(inputDir+'/*'):
    dir=dir.split('/')[-1]
    if os.path.isdir(inputDir+'/'+dir):
        command='hadd -f '+outputDir+'/'+dir+'.root '+inputDir+'/'+dir+'/*.root'

        print command
        os.system(command)
        print

################################################################

"""
for sample in allSamples:
    
    if glob(inputDir+'/'+sample.name+'/*'+'root')>1: command='hadd -f -v 99 '+outputDir+'/'+sample.name+'.root '+inputDir+'/'+sample.name+'/*.root'
    else: command='ln -s '+inputDir+'/'+sample.name+'/*.root '+outputDir+'/'+sample.name+'.root'
    
    print command
    os.system(command)
    print 
"""
