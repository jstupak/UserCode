from sys import argv
from os import system
from glob import glob
from UserCode.JohnStupak.Sample import allSamples as theSamples

try: destination=argv[1]
except:
    print 'No destination specified'
    exit()

for sample in theSamples:
    nJobs=len(glob(destination+'/'+sample.name+'/'+sample.name+'_*.job'))
    nSuccesful=len(glob(sample.name+'_*.root'))

    if nSuccesful<nJobs: print 40*'!','\nProblem with sample:',sample.name,'\n'
    
    command='mv '+sample.name+'* '+destination+'/'+sample.name+'/'
    print command
    system(command)

    
