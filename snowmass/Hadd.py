from os import environ

import os
import sys
from glob import glob

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
