import os
from copy import deepcopy
from ROOT import TChain, kRed, kBlue, kGreen, kBlack
relBase = os.environ['CMSSW_BASE']

class Sample:

    def __init__(self,name,sampleType=None,color=None,altName=None,crossSection=None,filesPerJob=20,nEvents=0,inputListFile=None):
        self.name=name; self.type=sampleType; self.color=color; self.altName=altName; self.filesPerJob=filesPerJob;
        self.crossSection=crossSection; self.nEvents=nEvents; self.inputListFile=inputListFile

        self.setType()
        self.setInputList()
        self.getSigma()
        #self.setColor()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setType(self):
        if type(self.type)!=type(''): return

        self.type=self.type.lower()

        self.isSignal=False; self.isBackground=False;
        if self.type in ['signal','sig']:
            self.isSignal=True
        elif self.type in ['background','bkgd','ewk','top']:
            self.isBackground=True
        else:
            raise Exception('Invalid Sample type')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setInputList(self):
        if not self.inputListFile: return

        self.inputList=[]
        for line in open(self.inputListFile):
            if '.root' in line: self.inputList+=[line.strip()]
    
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def clone(self,name):
        theClone=deepcopy(self)
        theClone.name=name
        return theClone

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def getNEvents(self,treeName):
        chain=TChain(treeName)
        for file in self.inputList:
            chain.Add(file)
        return chain.GetEntries()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    def getSigma(self):
        pass
    
################################################################################################################################################

allSamples=[]

#pileups=['No','50','140']
pileups=['No']

backgrounds=['WJETS_13TEV',
             'wjetsmad_33TEV',
             #'DIPHOTONS_13TEV',
             #'DIPHOTONS_33TEV',
             #'PHOTONJETS_13TEV',
             #'PHOTONJETS_33TEV',
             #'SSWWJETS_13TEV',
             #'SSWWJETS_33TEV',
             'TTBAR_13TEV',
             'TTBARJets_33TEV',
             'TTBARW_13TEV',
             'TTBARW_33TEV',
             'TTBARWW_13TEV',
             #'TTBARWW_33TEV',
             'TTBARZ_13TEV',
             'TTBARZ_33TEV',
             #'WGJETS_13TEV',
             #'WGJETS_33TEV',
             'WW_33TeV',
             'WWJETS_13TEV',
             'WWW_13TEV',
             'WWW_33TEV',
             'WWZ_13TEV',
             'WWZ_33TEV',
             'WZ_33TeV',
             #'WZ3LNUJETS_13TEV',
             #'WZ3LNUJETS_33TEV',
             'WZJETS_13TEV',
             'WZZ_13TEV',
             'WZZ_33TEV',
             #'ZGJETS_13TEV',
             #'ZGJETS_33TEV',
             'ZJETS_13TEV',
             'ZJETS_33TEV',
             #'ZZ4LJETS_13TEV',
             #'ZZ4LJETS_33TEV',
             'ZZJETS_13TEV',
             'ZZJETS_33TEV',
             'ZZZ_13TEV',
             'ZZZ_33TEV']

for pileup in pileups:
    for background in backgrounds:
        theName=name=background+'_'+pileup+'PileUp'

        for line in open(relBase+'/src/JohnStupak/snowmass/crossSections.txt'):
            if background in line:
                sigma=float(line.split('|')[3].strip())

        theInputFileList=relBase+'/src/JohnStupak/snowmass/'+background+'_'+pileup+'PileUp_files.txt'

        if 'TT' in background: theType='top'
        elif 'PHOTON' in background: theType='bkgd'
        else: theType='ewk'

        allSamples.append(Sample(name=theName,sampleType=theType,crossSection=sigma,filesPerJob=40,inputListFile=theInputFileList))
        
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

signals=['HWW_14TEV','HZZ_14TEV','AZh_14TEV_tata',
         #'AZh_14TEV_bb','AZh_14TEV_ww','AZh_14TEV_zz'
         ]
#masses=range(200,701,50)+range(700,1001,100)
masses=['500']

for pileup in pileups:
    for mass in masses:
        for signal in signals:
            theName=signal+'_'+mass+'_'+pileup+'PileUp'

            for line in open(relBase+'/src/JohnStupak/snowmass/crossSections.txt'):
                if signal+'_'+mass in line:
                    sigma=float(line.split('|')[3].strip())

            theInput='/eos/uscms/store/user/jstupak/snowmass/14TeV/Delphes-3.0.9/'+theName+'.root'
            theInputFileList=relBase+'/src/JohnStupak/snowmasss/ntuples/'+signal+'.txt'
            f=open(theInputFileList,'w')
            f.write(theInput)
            f.close()
            
            allSamples.append(Sample(name=theName,sampleType='signal',crossSection=sigma,filesPerJob=5,inputListFile=theInputFileList))

