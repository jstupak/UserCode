import os
from copy import deepcopy

class Sample:

    def __init__(self,name,sampleType=None,color=None,altName=None,crossSection=None,filesPerJob=20,nEvents=0,inputListFile=None,doQCD=False):
        self.name=name; self.type=sampleType; self.color=color; self.altName=altName; self.filesPerJob=filesPerJob;
        self.crossSection=crossSection; self.nEvents=nEvents; self.inputListFile=inputListFile; self.doQCD=doQCD;

        self.setType()
        self.setInputList()
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setType(self):
        if type(self.type)!=type(''): return

        self.type=self.type.lower()

        self.isData=False; self.isMC=False; self.isSignal=False; self.isBackground=False;
        if self.type=='data':
            self.isData=True
        elif self.type=='signal':
            self.isMC=True
            self.isSignal=True
        elif self.type=='ewk' or self.type=='electroweak' or self.type=='background':
            self.isMC=True
            self.isBackground=True
        else:
            raise Exception('Invalid Sample type')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setInputList(self):
        if not self.inputListFile: return
        
        self.inputList=[]
        for line in open(os.environ['CMSSW_BASE']+'/'+self.inputListFile):
            if '.root' in line: self.inputList+=[line.strip().strip(',')[1:-1]]

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
    
################################################################################################################################################

dataMuA=Sample('SingleMu_13Jul2012A',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012A_13Jul2012_v1_TLBSM_53x_v2_jsonfix_cff.txt')
dataMuA_recover=Sample('SingleMu_06Aug2012A',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012A_recover_06Aug2012_v1_TLBSM_53x_v2_cff.txt')
dataMuB=Sample('SingleMu_13Jul2012B',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012B_13Jul2012_v1_TLBSM_53x_v2_cff.txt')
dataMuC=Sample('SingleMu_24Aug2012C',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012C_24Aug2012_v1_TLBSM_53x_v2_cff.txt')
dataMuC_prompt=Sample('SingleMu_Prompt2012C1',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012C_PromptReco_v2_TLBSM_53x_v2_cff.txt')
dataMuC_prompt_ext=Sample('SingleMu_Prompt2012C2',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012C_PromptReco_v2_TLBSM_53x_v2_extension_v1_cff.txt')
dataMuC_recover=Sample('SingleMu_11Dec2012C',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_Run2012C_EcalRecover_11Dec2012_v1_TLBSM_53x_v2_cff.txt')
dataMuD_prompt=Sample('SingleMu_Prompt2012D1',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012D_PromptReco_v1_TLBSM_53x_v2_cff.txt')
dataMuD_prompt_ext=Sample('SingleMu_Prompt2012D2',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleMu_StoreResults_Run2012D_PromptReco_v1_TLBSM_53x_v2_extension_v2_cff.txt')

dataElA=Sample('SingleElectron_13Jul2012A',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012A_13Jul2012_v1_TLBSM_53x_v2_cff.txt')
dataElA_recover=Sample('SingleElectron_06Aug2012A',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012A_recover_06Aug2012_v1_TLBSM_53x_v2_cff.txt')
dataElB=Sample('SingleElectron_13Jul2012B',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012B_13Jul2012_v1_TLBSM_53x_v2_cff.txt')
dataElC=Sample('SingleElectron_24Aug2012C',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012C_24Aug2012_v1_TLBSM_53x_v2_cff.txt')
dataElC_prompt=Sample('SingleElectron_Prompt2012C1',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012C_PromptReco_v2_TLBSM_53x_v2_cff.txt')
dataElC_prompt_ext=Sample('SingleElectron_Prompt2012C2',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012C_PromptReco_v2_TLBSM_53x_v2_extension_v1_cff.txt')
dataElC_recover=Sample('SingleElectron_11Dec2012C',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_Run2012C_EcalRecover_11Dec2012_v1_TLBSM_53x_v2_cff.txt')
dataElD_prompt=Sample('SingleElectron_Prompt2012D1',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012D_PromptReco_v1_TLBSM_53x_v2_bugfix_cff.txt')
dataElD_prompt_ext=Sample('SingleElectron_Prompt2012D2',sampleType='data',filesPerJob=5,inputListFile='src/LJMet/Com/python/Samples_2012/SingleElectron_StoreResults_Run2012D_PromptReco_v1_TLBSM_53x_v2_extension_v1_cff.txt')

data=[dataMuA,dataMuA_recover,dataMuB,dataMuC,dataMuC_prompt,dataMuC_prompt_ext,dataMuC_recover,dataMuD_prompt,dataMuD_prompt_ext,dataElA,dataElA_recover,dataElB,dataElC,dataElC_prompt,dataElC_prompt_ext,dataElC_recover,dataElD_prompt,dataElD_prompt_ext]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

WJets=Sample('WJets',sampleType='ewk',altName='W+Jets',crossSection=37503.0,nEvents=76041475.0,inputListFile='src/LJMet/Com/python/Samples_2012/WJetsToLNu_TuneZ2Star_8TeV_madgraph_tarball_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_v2_TLBSM_53x_v2_cff.txt')
WW=Sample('WW',sampleType='ewk',crossSection=54.838,nEvents=10000431.0,inputListFile='src/LJMet/Com/python/Samples_2012/WW_TuneZ2star_8TeV_pythia6_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
TTbar_Madgraph=Sample('TTbar_Madgraph',sampleType='ewk',altName='TTbar',crossSection=234.0,nEvents=6923750.0,inputListFile='src/LJMet/Com/python/Samples_2012/TTJets_MassiveBinDECAY_TuneZ2star_8TeV_madgraph_tauola_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt') # approx NNLO
TTbar_Powheg=Sample('TTbar_Powheg',sampleType='ewk',altName='TTbar',crossSection=234.0,nEvents=21591169.0,inputListFile='src/LJMet/Com/python/Samples_2012/TT_CT10_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v2_TLBSM_53x_v2_cff.txt') # approx NNLO xsec
ZJets=Sample('ZJets_M50',sampleType='ewk',altName='Z+Jets',crossSection=3503.71,nEvents=30459503.0,inputListFile='src/LJMet/Com/python/Samples_2012/DYJetsToLL_M_50_TuneZ2Star_8TeV_madgraph_tarball_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
ZZ=Sample('ZZ',sampleType='ewk',crossSection=1,nEvents=9799908,inputListFile='src/LJMet/Com/python/Samples_2012/ZZ_TuneZ2star_8TeV_pythia6_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
T_tW=Sample('T_tW',sampleType='ewk',altName='T_tW',crossSection=11.1,nEvents=497658.0,inputListFile='src/LJMet/Com/python/Samples_2012/T_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Tbar_tW=Sample('Tbar_tW',sampleType='ewk',altName='Tbar_tW',crossSection=11.1,nEvents=493460.0,inputListFile='src/LJMet/Com/python/Samples_2012/Tbar_tW_channel_DR_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
T_t=Sample('T_t',sampleType='ewk',altName='T_t',crossSection=56.4,nEvents=3758227.0,inputListFile='src/LJMet/Com/python/Samples_2012/T_t_channel_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Tbar_t=Sample('Tbar_t',sampleType='ewk',altName='Tbar_t',crossSection=30.7,nEvents=1935072.0,inputListFile='src/LJMet/Com/python/Samples_2012/Tbar_t_channel_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
T_s=Sample('T_s',sampleType='ewk',altName='T_s',crossSection=3.79,nEvents=259961.0,inputListFile='src/LJMet/Com/python/Samples_2012/T_s_channel_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Tbar_s=Sample('Tbar_s',sampleType='ewk',altName='Tbar_s',crossSection=1.76,nEvents=139974.0,inputListFile='src/LJMet/Com/python/Samples_2012/Tbar_s_channel_TuneZ2star_8TeV_powheg_tauola_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')

EWK=[WJets,WW,TTbar_Madgraph,TTbar_Powheg,ZJets,ZZ,T_tW,Tbar_tW,T_t,Tbar_t,T_s,Tbar_s]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

QCD=[]
for sample in data+EWK:
    if 'ZZ' in sample.name or 'TTbar_Madgraph' in sample.name: continue
    QCDSample=sample.clone('QCD_'+sample.name)
    QCDSample.doQCD=True
    QCD.append(QCDSample)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

chargedHiggs200=Sample('chargedHiggs200',sampleType='signal',altName='H^{#pm} (m=200 GeV)',crossSection=.132*1.485,filesPerJob=10,nEvents=900000,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-200_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')
chargedHiggs300=Sample('chargedHiggs300',sampleType='signal',altName='H^{#pm} (m=300 GeV)',crossSection=1,filesPerJob=10,nEvents=900000,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-300_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')
#chargedHiggs400=Sample('chargedHiggs400',sampleType='signal',altName='H^{#pm} (m=400 GeV)',crossSection=1,filesPerJob=10,nEvents=,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-400_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')
chargedHiggs500=Sample('chargedHiggs500',sampleType='signal',altName='H^{#pm} (m=500 GeV)',crossSection=.017*1.695,filesPerJob=10,nEvents=900000,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-500_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')
chargedHiggs600=Sample('chargedHiggs600',sampleType='signal',altName='H^{#pm} (m=600 GeV)',crossSection=1,filesPerJob=10,nEvents=900000,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-600_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')
chargedHiggs700=Sample('chargedHiggs700',sampleType='signal',altName='H^{#pm} (m=700 GeV)',crossSection=1,filesPerJob=10,nEvents=900000,inputListFile='src/LJMet/Com/python/Samples_2012/ChargedHToTB_M-700_tanBeta30_8TeV_pythia6_tauola_Summer12_DR53X_PU_S10_START53_V7C_v1_TLBSM_53x_v2.txt')

signal=[chargedHiggs200,chargedHiggs300,chargedHiggs500,chargedHiggs600,chargedHiggs700]

"""
Wprime800Right =Sample('Wprime800Right' ,sampleType='signal',altName='W^{'}_{R} (m=800GeV)',crossSection=1.5352,filesPerJob=19,nEvents=920654,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_800_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
#Wprime900Right =Sample('Wprime900Right' ,sampleType='signal',altName='W^{'}_{R} (m=900GeV)',crossSection=0.9214,filesPerJob=20,nEvents=,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_900_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
#Wprime1000Right=Sample('Wprime1000Right',sampleType='signal',altName='W^{'}_{R} (m=1TeV)'  ,crossSection=0.5704,filesPerJob=20,nEvents=,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1000_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1100Right=Sample('Wprime1100Right',sampleType='signal',altName='W^{'}_{R} (m=1.1TeV)',crossSection=0.3623,filesPerJob=20,nEvents=831508,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1100_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1200Right=Sample('Wprime1200Right',sampleType='signal',altName='W^{'}_{R} (m=1.2TeV)',crossSection=0.2348,filesPerJob=20,nEvents=965528,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1200_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1300Right=Sample('Wprime1300Right',sampleType='signal',altName='W^{'}_{R} (m=1.3TeV)',crossSection=0.1548,filesPerJob=20,nEvents=881046,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1300_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1400Right=Sample('Wprime1400Right',sampleType='signal',altName='W^{'}_{R} (m=1.4TeV)',crossSection=0.1036,filesPerJob=20,nEvents=920262,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1400_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1500Right=Sample('Wprime1500Right',sampleType='signal',altName='W^{'}_{R} (m=1.5TeV)',crossSection=0.0701,filesPerJob=20,nEvents=907297,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1500_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1600Right=Sample('Wprime1600Right',sampleType='signal',altName='W^{'}_{R} (m=1.6TeV)',crossSection=0.048,filesPerJob=20,nEvents=892146,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1600_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1700Right=Sample('Wprime1700Right',sampleType='signal',altName='W^{'}_{R} (m=1.7TeV)',crossSection=0.0331,filesPerJob=20,nEvents=924438,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1700_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1800Right=Sample('Wprime1800Right',sampleType='signal',altName='W^{'}_{R} (m=1.8TeV)',crossSection=0.0231,filesPerJob=20,nEvents=841448,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1800_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime1900Right=Sample('Wprime1900Right',sampleType='signal',altName='W^{'}_{R} (m=1.9TeV)',crossSection=0.0162,filesPerJob=20,nEvents=835381.0,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_1900_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2000Right=Sample('Wprime2000Right',sampleType='signal',altName='W^{'}_{R} (m=2TeV)'  ,crossSection=0.0114,filesPerJob=20,nEvents=841836,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2000_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2100Right=Sample('Wprime2100Right',sampleType='signal',altName='W^{'}_{R} (m=2.1TeV)',crossSection=0.008,filesPerJob=20,nEvents=926108,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2100_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2200Right=Sample('Wprime2200Right',sampleType='signal',altName='W^{'}_{R} (m=2.2TeV)',crossSection=0.006,filesPerJob=20,nEvents=932785,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2200_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2300Right=Sample('Wprime2300Right',sampleType='signal',altName='W^{'}_{R} (m=2.3TeV)',crossSection=0.004,filesPerJob=20,nEvents=784768,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2300_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2400Right=Sample('Wprime2400Right',sampleType='signal',altName='W^{'}_{R} (m=2.4TeV)',crossSection=0.003,filesPerJob=20,nEvents=894786,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2400_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2500Right=Sample('Wprime2500Right',sampleType='signal',altName='W^{'}_{R} (m=2.5TeV)',crossSection=0.002,filesPerJob=20,nEvents=878643,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2500_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2600Right=Sample('Wprime2600Right',sampleType='signal',altName='W^{'}_{R} (m=2.6TeV)',crossSection=0.0017,filesPerJob=20,nEvents=944599,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2600_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2700Right=Sample('Wprime2700Right',sampleType='signal',altName='W^{'}_{R} (m=2.7TeV)',crossSection=0.0012,filesPerJob=20,nEvents=915158,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2700_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2800Right=Sample('Wprime2800Right',sampleType='signal',altName='W^{'}_{R} (m=2.8TeV)',crossSection=0.00094,filesPerJob=20,nEvents=835281,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2800_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime2900Right=Sample('Wprime2900Right',sampleType='signal',altName='W^{'}_{R} (m=2.9TeV)',crossSection=0.00072,filesPerJob=20,nEvents=910111,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_2900_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')
Wprime3000Right=Sample('Wprime3000Right',sampleType='signal',altName='W^{'}_{R} (m=3TeV)'  ,crossSection=0.00056,filesPerJob=20,nEvents=932601,inputListFile='src/LJMet/Com/python/Samples_2012/SingletopWprime_M_3000_right_TuneZ2star_8TeV_comphep_StoreResults_Summer12_DR53X_PU_S10_START53_V7A_v1_TLBSM_53x_v2_cff.txt')

signal=[Wprime800Right,Wprime1100Right,Wprime1200Right,Wprime1300Right,Wprime1400Right,Wprime1500Right,Wprime1600Right,Wprime1700Right,Wprime1800Right,Wprime1900Right,Wprime2000Right,Wprime2100Right,Wprime2200Right,Wprime2300Right,Wprime2400Right,Wprime2500Right,Wprime2600Right,Wprime2700Right,Wprime2800Right,Wprime2900Right,Wprime3000Right]
"""

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#allSamples=signal+QCD+EWK+data
#samplesForPlotting=[chargedHiggs200,chargedHiggs500]+QCD+[TTbar_Madgraph,T_t,Tbar_t,T_tW,Tbar_tW,T_s,Tbar_s,WJets,ZJets,WW]+data

allSamples=signal+EWK+data
samplesForPlotting=[chargedHiggs200,chargedHiggs500]+[TTbar_Madgraph,T_t,Tbar_t,T_tW,Tbar_tW,T_s,Tbar_s,WJets,ZJets,WW]+data

#-----------------------------------------------------------------------------------------------------------------------------------------------

#allSamples=[dataMuC_recover,dataElC_recover]
