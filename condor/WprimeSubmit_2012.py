#!/usr/bin/python

import os
from datetime import datetime
from UserCode.JohnStupak.Sample import allSamples as theSamples
relBase = os.environ['CMSSW_BASE']

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Job config

submissionID='newEventSelTest'

doData=True
doBackground=True
doSignal=True

doNominal=True
doJES=False
doJER=False
doBTS=False

analysisOutputDir='/uscms_data/d1/jstupak/analysisOutputs'

pythonTempl=relBase+"/src/LJMet/Com/condor/wprime_cfg.templ.py"
condorJobTempl=relBase+"/src/LJMet/Com/condor/wprime.templ.job"
condorScriptTempl=relBase+"/src/LJMet/Com/condor/wprime.templ.csh"

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Analysis config

### What is the name of your FWLite Analyzer
FWLiteAnalyzer = 'ljmet'

### Selection to run
SELECTOR = "'WprimeSelector'"

### Use best top for neutrino pz solution?
USEBESTTOP = 'True'

### Triggers
MCTRIGGEREL = "'HLT_Ele27_WP80_v10'"
MCTRIGGERMU = "'HLT_IsoMu24_eta2p1_v13'"
DATATRIGGEREL = "'HLT_Ele27_WP80_v8','HLT_Ele27_WP80_v9','HLT_Ele27_WP80_v10','HLT_Ele27_WP80_v11'"
DATATRIGGERMU = "'HLT_IsoMu24_eta2p1_v11','HLT_IsoMu24_eta2p1_v12','HLT_IsoMu24_eta2p1_v13','HLT_IsoMu24_eta2p1_v14','HLT_IsoMu24_eta2p1_v15'"

### Lepton Selection
defaultMINTIGHTMUON = '0'
defaultMINTIGHTELECTRON = '0'
defaultMINLOOSEMUON = '0'
defaultMINLOOSEELECTRON = '0'
defaultMINTIGHTLEPTON = '1'
defaultMAXTIGHTLEPTON = '1'
defaultMINLOOSELEPTON = '0'
defaultMAXLOOSELEPTON = '0'

### Jet Selection
LEADINGJETPT = '50.0'

################################################################################################################################################

cTime=datetime.now()
date=str(cTime.year)+'_'+str(cTime.month)+'_'+str(cTime.day)

condorDir=analysisOutputDir+'/'+date
if submissionID: condorDir+='/'+submissionID

rc=os.system('mkdir -p '+condorDir)
#if rc!=0: raise Exception('condorDir already exists - '+condorDir)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def submitJobs(systematic=None):

    if systematic=='JESUP': JECUNCERTUP=True
    else: JECUNCERTUP=False
    if systematic=='JESDOWN': JECUNCERTDOWN=True
    else: JECUNCERTDOWN=False
    if systematic=='JERUP': JERUNCERTUP=True
    else: JERUNCERTUP=False
    if systematic=='JERDOWN': JERUNCERTDOWN=True
    else: JERUNCERTDOWN=False
    if systematic=='BTAGUP': BTAGUNCERTUP=True
    else: BTAGUNCERTUP=False
    if systematic=='BTAGDOWN': BTAGUNCERTDOWN=True
    else: BTAGUNCERTDOWN=False
        
    print '#################################################'
    print 'Condor Job Submission'
    print
    print 'Condor Work Area:',condorDir
    print 'Python File Template:',pythonTempl
    print 'Condor Job File Template:',condorJobTempl
    print 'Condor Script Template:',condorScriptTempl
    print

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    for sample in theSamples:
        if (sample.isData and doData) or (sample.isBackground and doBackground) or (sample.isSignal and doSignal):
            print '-------------------------------------------------'
            if sample.isData and systematic: continue

            jobID=sample.name
            if systematic: jobID+='_'+systematic
            jobDir=condorDir+'/'+jobID
            os.system('mkdir '+jobDir)
            ISMCSAMPLE=str(sample.isMC)
            DOQCD=str(sample.doQCD)
            ISWJETS=str('WJets' in sample.name)
            if sample.isMC: MYJSON = "''"
            elif '13Jul2012' in sample.name: MYJSON = "'../data/json/Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt'"
            elif '06Aug2012' in sample.name: MYJSON = "'../data/json/Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON.txt'"
            elif '24Aug2012' in sample.name: MYJSON = "'../data/json/Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt'"
            elif 'Prompt2012C' in sample.name: MYJSON = "'../data/json/Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_v2.txt'"
            else: raise Exception("No valid JSon file")

            if sample.isBackground and sample.doQCD: SAMPLEWEIGHT=str(-1*sample.crossSection/sample.nEvents)
            else: SAMPLEWEIGHT=1

            MINTIGHTMUON=defaultMINTIGHTMUON
            MINTIGHTELECTRON=defaultMINTIGHTELECTRON
            MINLOOSEMUON=defaultMINLOOSEMUON
            MINLOOSEELECTRON=defaultMINLOOSEELECTRON
            MINTIGHTLEPTON=defaultMINTIGHTLEPTON
            MAXTIGHTLEPTON=defaultMAXTIGHTLEPTON
            MINLOOSELEPTON=defaultMINLOOSELEPTON
            MAXLOOSELEPTON=defaultMAXLOOSELEPTON
            TRIGGERCUT='True'
            TRIGGERCONSISTENT='True'
            if sample.doQCD:
                TRIGGERCUT='False'
                TRIGGERCONSISTENT='False'
                MINTIGHTLEPTON = '0'
                MAXTIGHTLEPTON = '0'
                MINLOOSELEPTON = '1'
                MAXLOOSELEPTON = '1'
                if 'SingleMu' in sample.name: MINLOOSEMUON='1'
                elif 'SingleElectron' in sample.name: MINLOOSEELECTRON='1'
            elif sample.isData:
                if 'SingleMu' in sample.name: MINTIGHTMUON='1'
                elif 'SingleElectron' in sample.name: MINTIGHTELECTRON='1'
                else: raise Exception("Invalid data stream")
                
            for fileNo in range(len(sample.inputList)):
                sample.inputList[fileNo]='dcap:///pnfs/cms/WAX/11'+sample.inputList[fileNo]

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
                pythonFile=fileNamesBase+'.py'
                condorJobFile=fileNamesBase+'.job'
                condorScriptFile=fileNamesBase+'.csh'

                multiSed(pythonTempl,pythonFile,[['DIRECTORY',jobDir],
                                                 ['PREFIX',jobID],
                                                 ['JOBID',jobNo],
                                                 ['SELECTOR',SELECTOR],
                                                 ['INFILES',files],
                                                 ['BTAGUNCERTUP',BTAGUNCERTUP],
                                                 ['BTAGUNCERTDOWN',BTAGUNCERTDOWN],
                                                 ['JECUNCERTUP',JECUNCERTUP],
                                                 ['JECUNCERTDOWN',JECUNCERTDOWN],
                                                 ['JERUNCERTUP',JERUNCERTUP],
                                                 ['JERUNCERTDOWN',JERUNCERTDOWN],
                                                 ['EVENTSTOPROCESS',"-1"],
                                                 ['ISMCSAMPLE',ISMCSAMPLE],
                                                 ['JSONFILE',MYJSON],
                                                 ['MCTRIGGEREL',MCTRIGGEREL],
                                                 ['MCTRIGGERMU',MCTRIGGERMU],
                                                 ['DATATRIGGEREL',DATATRIGGEREL],
                                                 ['DATATRIGGERMU',DATATRIGGERMU],
                                                 ['MINTIGHTMUON',MINTIGHTMUON],
                                                 ['MINTIGHTELECTRON',MINTIGHTELECTRON],
                                                 ['MINLOOSEMUON',MINLOOSEMUON],
                                                 ['MINLOOSEELECTRON',MINLOOSEELECTRON],
                                                 ['MINTIGHTLEPTON',MINTIGHTLEPTON],
                                                 ['MAXTIGHTLEPTON',MAXTIGHTLEPTON],
                                                 ['MINLOOSELEPTON',MINLOOSELEPTON],
                                                 ['MAXLOOSELEPTON',MAXLOOSELEPTON],
                                                 ['LEADINGJETPT',LEADINGJETPT],
                                                 ['ISWJETS',ISWJETS],
                                                 ['DOQCD',DOQCD],
                                                 ['SAMPLEWEIGHT',SAMPLEWEIGHT],
                                                 ['TRIGGERCUT',TRIGGERCUT],
                                                 ['TRIGGERCONSISTENT',TRIGGERCONSISTENT],
                                                 ['USEBESTTOP',USEBESTTOP]])

                multiSed(condorJobTempl,condorJobFile,[['DIRECTORY',jobDir],
                                                       ['PREFIX',jobID],
                                                       ['JOBID',jobNo]])

                multiSed(condorScriptTempl,condorScriptFile,[['CMSSWBASE',relBase],
                                                             ['DIRECTORY',jobDir],
                                                             ['PREFIX',jobID],
                                                             ['JOBID',jobNo],
                                                             ['FWLITEANALYZER',FWLiteAnalyzer]])

                os.system('chmod u+x '+condorScriptFile)
                submitCommand='condor_submit '+condorJobFile
                print submitCommand
                os.system(submitCommand)

                jobNo+=1
                firstFile=lastFile+1
                lastFile=firstFile+sample.filesPerJob-1

    os.system('tar -czvf '+condorDir+'/backup.tar.gz --exclude="*.log" --exclude="*.root" --exclude="*.pdf" --exclude="*.eps" --exclude=".backup" '+relBase+'/src/LJMet/Com/*')

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

if doNominal: submitJobs()

systematics=[]
if doJES: systematics+=['JESUP','JESDOWN']
if doJER: systematics+=['JERUP','JERDOWN']
if doBTS: systematics+=['BTAGUP','BTAGDOWN']

for systematic in systematics: submitJobs(systematic)

