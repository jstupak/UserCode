#!/usr/bin/python

import os, sys
from datetime import datetime
from snowmassSamples import allSamples as theSamples
relBase = os.environ['CMSSW_BASE']

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Job config

doBackground=True
doSignal=True

analysisOutputDir='/uscms_data/d1/jstupak/2hdm'

rootScriptTempl=relBase+"/src/JohnStupak/snowmass/runIt.templ.C"
condorJobTempl=relBase+"/src/JohnStupak/snowmass/twoHiggsDoublet.templ.job"
condorScriptTempl=relBase+"/src/JohnStupak/snowmass/twoHiggsDoublet.templ.csh"

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Analysis config

################################################################################################################################################

cTime=datetime.now()
date=str(cTime.year)+'_'+str(cTime.month)+'_'+str(cTime.day)

condorDir=analysisOutputDir+'/'+date

if len(sys.argv)==2:
    submissionID=sys.argv[1]
    condorDir+='/'+submissionID

rc=os.system('mkdir -p '+condorDir)
if rc!=0: raise Exception('condorDir already exists - '+condorDir)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def submitJobs():

    print '#################################################'
    print 'Condor Job Submission'
    print
    print 'Condor Work Area:',condorDir
    print 'Condor Job File Template:',condorJobTempl
    print 'Condor Script Template:',condorScriptTempl
    print

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for sample in theSamples:
        if (sample.isBackground and doBackground) or (sample.isSignal and doSignal):
            print '-------------------------------------------------'

            jobID=sample.name
            jobDir=condorDir+'/'+jobID
            os.system('mkdir '+jobDir)
                
            print 'Sample Name:',sample.name
            print 'Number Of Input Files:',len(sample.inputList)

            jobNo=1
            firstFile=0
            lastFile=firstFile+sample.filesPerJob-1
            while firstFile<len(sample.inputList):
                print '- - - - - - - - - - - - - - - - - - - - - - - - -'
                if lastFile>=len(sample.inputList): lastFile=len(sample.inputList)-1
                files=sample.inputList[firstFile:lastFile+1]

                fileNamesBase=jobDir+'/'+sample.name+'_'+str(jobNo)
                fileList=open(fileNamesBase+'.txt','w')
                for file in files:
                    fileList.write(file+'\n')
                fileList.close()

                rootScript=fileNamesBase+'.C'
                condorJobFile=fileNamesBase+'.job'
                condorScriptFile=fileNamesBase+'.csh'

                #multiSed(rootScriptTempl,rootScript,[['INPUTS',fileNamesBase+'.txt']])
                multiSed(condorJobTempl,condorJobFile,[['DIRECTORY',jobDir],
                                                       ['PREFIX',jobID],
                                                       ['JOBID',jobNo]])
                multiSed(condorScriptTempl,condorScriptFile,[['CMSSWBASE',relBase],
                                                             ['DIRECTORY',jobDir],
                                                             ['PREFIX',jobID],
                                                             ['JOBID',jobNo],
                                                             ['EXECUTABLE',rootScript],
                                                             ['INPUTS',fileNamesBase+'.txt']
                                                             ['OUTPUT',sample.name+'_'+str(jobNo)+'.root']])

                os.system('chmod u+x '+condorScriptFile)
                submitCommand='condor_submit '+condorJobFile
                print submitCommand
                os.system('cd '+jobDir+'; '+submitCommand+'; cd -')

                jobNo+=1
                firstFile=lastFile+1
                lastFile=firstFile+sample.filesPerJob-1

    os.system('tar -czvf '+condorDir+'/backup.tar.gz --exclude="*.log" --exclude="*.root" --exclude="*.pdf" --exclude="*.eps" --exclude=".backup" '+relBase+'/src/JohnStupak/snowmass/*')

################################################################################################################################################

def multiSed(oldFileName,newFileName,replacements):
    os.system('cp '+oldFileName+' '+newFileName)
    
    for replacement in replacements:
        if len(replacement)>2: raise Exception("Invalid argument to multiSed")
        old=replacement[0]
        new=str(replacement[1])
        
        command='sed "s#'+old+'#'+new+'#" '+newFileName+' --in-place'
        #print command
        os.system(command)

################################################################################################################################################
#NOW FINALLY DO THE SUBMISSION

submitJobs()
