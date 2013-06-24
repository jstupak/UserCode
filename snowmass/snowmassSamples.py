import os
from copy import deepcopy
from ROOT import TChain, kRed, kBlue, kGreen, kBlack
from glob import glob
relBase = os.environ['CMSSW_BASE']

class Sample:

    def __init__(self,name,sampleType=None,color=None,altName=None,crossSection=None,filesPerJob=20,nEvents=0,inputListFile=None):
        self.name=name; self.type=sampleType; self.color=color; self.altName=altName; self.filesPerJob=filesPerJob;
        self.crossSection=crossSection; self.nEvents=nEvents; self.inputListFile=inputListFile

        self.setType()
        self.setInputList()
        self.setMass()
        #self.setColor()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setType(self):
        if type(self.type)!=type(''): return

        self.type=self.type.lower()

        self.isSignal=False; self.isBackground=False;
        if self.type in ['signal','sig']:
            self.isSignal=True
        elif self.type in ['background','bkgd','ewk','top','other']:
            self.isBackground=True
        else:
            raise Exception('Invalid Sample type')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setMass(self):
        if self.isSignal:
            self.mass=int(self.name.split('_')[-2])
        else: self.mass=None
            

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
    
    def setCrossSection(self, beta=0, cosBetaMinusAlpha=0, twoHDMType=1):
        self.crossSection=None

        if self.isSignal:
            particle=self.name[0]
            E=self.name.split('_')[1].split('T')[0]
            
            crossSectionFile=relBase+'/src/JohnStupak/snowmass/rawCrossSections/'+'gg_'+particle+'_'+str(E)+'TeV_T'+str(twoHDMType)+'_'+str(self.mass)+'.txt'

            for line in open(crossSectionFile):
                cBMA=float(line.split()[0])
                B=float(line.split()[1])
                if abs((beta-B)/beta)<.0001 and abs((cosBetaMinusAlpha-cBMA)/cosBetaMinusAlpha)<.000001:
                    self.crossSection=float(line.split()[2])
                    break
                
            if 'HWW' in self.name: finalState='WW'
            elif 'HZZ' in self.name: finalState='ZZ'
            else: finalState=self.name[1:3]

            BRFile=relBase+'/src/JohnStupak/snowmass/rawCrossSections/'+'BR_'+particle+'_'+finalState+'_T'+str(twoHDMType)+'_'+str(self.mass)+'.txt'
            
            try:
                for line in open(BRFile):
                    cBMA=float(line.split()[0])
                    B=float(line.split()[1])
                    if abs((beta-B)/beta)<.0001 and abs((cosBetaMinusAlpha-cBMA)/cosBetaMinusAlpha)<.000001:
                        br=float(line.split()[2])
                        if finalState=='ZZ' and 'fullyLeptonic' in self.name: br*=.03363738

                        self.crossSection*=br
                        break
            except: self.crossSection=0

        else:
            for line in open(relBase+'/src/JohnStupak/snowmass/crossSections.txt'):
                sampleName=line.split('|')[1].strip()
                if '_'.join(self.name.split('_')[0:2])==sampleName:
                    self.crossSection=float(line.split('|')[3].strip())
                    break

        if not self.crossSection: print "WARNING: Could not find cross section for sample",self.name
        
################################################################################################################################################

allSamples=[]

#pileups=['No','50','140']
pileups=['No']
"""
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
"""

backgrounds=[
    'B-4p-0-1-v1510_14TEV',
    'Bj-4p-0-300-v1510_14TEV',
    'Bj-4p-1100-1800-v1510_14TEV',
    'Bj-4p-1800-2700-v1510_14TEV',
    'Bj-4p-2700-3700-v1510_14TEV',
    'Bj-4p-300-600-v1510_14TEV',
    'Bj-4p-3700-100000-v1510_14TEV',
    'Bj-4p-600-1100-v1510_14TEV',
    'BB-4p-0-300-v1510_14TEV',
    'BB-4p-1300-2100-v1510_14TEV',
    'BB-4p-2100-100000-v1510_14TEV',
    'BB-4p-300-700-v1510_14TEV',
    'BB-4p-700-1300-v1510_14TEV',
    'BBB-4p-0-600-v1510_14TEV',
    'BBB-4p-1300-100000-v1510_14TEV',
    'BBB-4p-600-1300-v1510_14TEV',
    'Bjj-vbf-4p-0-700-v1510_14TEV',
    'Bjj-vbf-4p-1400-2300-v1510_14TEV',
    'Bjj-vbf-4p-2300-3400-v1510_14TEV',
    'Bjj-vbf-4p-3400-100000-v1510_14TEV',
    'Bjj-vbf-4p-700-1400-v1510_14TEV',
    'H-4p-0-300-v1510_14TEV',
    'H-4p-1500-100000-v1510_14TEV',
    'H-4p-300-800-v1510_14TEV',
    'H-4p-800-1500-v1510_14TEV',
    'LL-4p-0-100-v1510_14TEV',
    'LL-4p-100-200-v1510_14TEV',
    'LL-4p-1400-100000-v1510_14TEV',
    'LL-4p-200-500-v1510_14TEV',
    'LL-4p-500-900-v1510_14TEV',
    'LL-4p-900-1400-v1510_14TEV',
    'LLB-4p-0-400-v1510_14TEV',
    'LLB-4p-400-900-v1510_14TEV',
    'LLB-4p-900-100000-v1510_14TEV',
    'tB-4p-0-500-v1510_14TEV',
    'tB-4p-1500-2200-v1510_14TEV',
    'tB-4p-2200-100000-v1510_14TEV',
    'tB-4p-500-900-v1510_14TEV',
    'tB-4p-900-1500-v1510_14TEV',
    'tj-4p-0-500-v1510_14TEV',
    'tj-4p-1000-1600-v1510_14TEV',
    'tj-4p-1600-2400-v1510_14TEV',
    'tj-4p-2400-100000-v1510_14TEV',
    'tj-4p-500-1000-v1510_14TEV',
    'tt-4p-0-600-v1510_14TEV',
    'tt-4p-1100-1700-v1510_14TEV',
    'tt-4p-1700-2500-v1510_14TEV',
    'tt-4p-2500-100000-v1510_14TEV',
    'tt-4p-600-1100-v1510_14TEV',
    #'ttB-4p-0-900-v1510_14TEV',
    #'ttB-4p-1600-2500-v1510_14TEV',
    #'ttB-4p-2500-100000-v1510_14TEV',
    #'ttB-4p-900-1600-v1510_14TEV'
]
    

signals=['HWW_14TEV','HZZ_14TEV','HZZ4l_14TEV','AZh_14TEV_tata',
         'AZh_14TEV_bb','AZh_14TEV_ww','AZh_14TEV_zz'
         ]
masses=range(200,500,50)+range(500,1001,100)

for pileup in pileups:
    for mass in masses:
        mass=str(mass)
        for signal in signals:
            theName=signal+'_'+mass+'_'+pileup+'PileUp'

            inputFiles=glob('/uscms_data/d3/jstupak/delphes/output/'+signal+'_'+mass+'*'+pileup+'*root')
            theInputFileList=relBase+'/src/JohnStupak/snowmass/ntuples/'+theName+'.txt'
            f=open(theInputFileList,'w')
            for file in inputFiles:
                f.write(file+'\n')
            f.close()

            signal=Sample(name=theName,sampleType='signal',inputListFile=theInputFileList)
            allSamples.append(signal)
            
                    
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -                    

for pileup in pileups:
    for background in backgrounds:
        theName=name=background+'_'+pileup+'PileUp'

        theInputFileList=relBase+'/src/JohnStupak/snowmass/ntuples/'+background+'_'+pileup+'PileUp_files.txt'

        #if 'TT' in background: theType='top'
        #elif 'PHOTON' in background: theType='bkgd'
        #else: theType='ewk'

        if background[0]=='t': theType='top'
        elif background[0:3]=='Bjj' or background[0]=='H': theType='other'
        else: theType='ewk'

        allSamples.append(Sample(name=theName,sampleType=theType,filesPerJob=40,inputListFile=theInputFileList))
        

#  LocalWords:  isSignal
