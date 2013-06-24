from ROOT import *
gROOT.SetBatch(1)
TH1.SetDefaultSumw2(True)
gStyle.SetOptStat(False)

from snowmassSamples import allSamples as samples
from tdrStyle import *
setTDRStyle()
import sys
from array import array
import os

DEBUG=False

if len(sys.argv)>1:
    inputDir=sys.argv[1]
else:
    inputDir='/uscms_data/d1/jstupak/2hdm/2013_6_6'

doLimitSetting=False
onlyDoCutTable=False
tableOutput='yields.txt'

pileup='No'
energy='14'
doSignals=['HZZ']
doSigmalMasses=[300,450,600]

#doCuts=['nL1']

doCuts=['Presel','LepTrig','LepTrig_nL4','LepTrig_nL4_nZ1p','LepTrig_nL4_nZ2']

"""
doCuts=['nL1','nL2','nL3','nL4p',
        'nB1','nB2','nB3','nB4p',
        'nT1','nT2p',
        
        'nL1_nB1','nL1_nB2','nL1_nB3','nL1_nB4p',
        'nL2_nB1','nL2_nB2','nL2_nB3','nL2_nB4p',
        'nL3_nB1','nL3_nB2','nL3_nB3','nL3_nB4p',
        'nL4p_nB1','nL4p_nB2','nL4p_nB3','nL4p_nB4p',

        'nL1_nT1','nL1_nT2p',
        'nL2_nT1','nL2_nT2p',
        'nL3_nT1','nL3_nT2p',
        'nL4p_nT1','nL4p_nT2p',

        'nV1','nV2p','nV1_nh1','nh2p']
"""
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

doShapeComparison=True
outputDir=inputDir+'/plots'

#1/fb
lumi=300.

signalMagFac=1

treeName='twoHiggsDoublet'

#---------------------------------------------------------------------------------------------------------------------------------------------

if not os.path.isdir(outputDir): os.system("mkdir -p "+outputDir)
output=TFile(outputDir+'/plots.root',"RECREATE")

s=[]
for sample in samples:
    include=False
    if sample.isBackground: include=True
    if sample.isSignal:
        for mass in doSigmalMasses:
            if str(mass) in sample.name:
                for signal in doSignals:
                    if signal in sample.name: include=True
    if include: s.append(sample)
samples=s

class TwoHiggsDoubletPlot:

    def __init__(self,name,distribution,bins=None,nBins=100,xMin=0,xMax=100,xTitle='',yLog=True,cutsID=None,extraCuts=None,channel=None):
        self.name=name; self.distribution=distribution; self.bins=bins; self.nBins=nBins; self.xMin=xMin; self.xMax=xMax; self.xTitle=xTitle; self.yLog=yLog; self.cutsID=cutsID; self.extraCuts=extraCuts; self.channel=channel;

        if self.cutsID: self.name+='_'+cutsID
        if self.channel: self.name+='_'+channel
        
        if self.bins:
            self.nBins=len(self.bins)-1
            self.xMin=self.bins[0]
            self.xMax=self.bins[-1]
        else:
            self.bins=[]
            for n in range(self.nBins+1):
                self.bins.append(self.xMin+n*(float(self.xMax-self.xMin)/self.nBins))
        self.bins=array('f',self.bins)
            
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Prepare(self):
        result={}

        self.cuts='1'

        if 'nL1p' in self.cutsID: self.cuts+=' && nElectron+nMuon>=1'
        elif 'nL1' in self.cutsID: self.cuts+=' && nElectron+nMuon==1'
        if 'nL2p' in self.cutsID: self.cuts+=' && nElectron+nMuon>=2'
        elif 'nL2' in self.cutsID: self.cuts+=' && nElectron+nMuon==2'
        if 'nL3p' in self.cutsID: self.cuts+=' && nElectron+nMuon>=3'
        elif 'nL3' in self.cutsID: self.cuts+=' && nElectron+nMuon==3'
        if 'nL4p' in self.cutsID: self.cuts+=' && nElectron+nMuon>=4'
        elif 'nL4' in self.cutsID: self.cuts+=' && nElectron+nMuon==4'

        if 'nB1p' in self.cutsID: self.cuts+=' && nBJet>=1'
        elif 'nB1' in self.cutsID: self.cuts+=' && nBJet==1'
        if 'nB2p' in self.cutsID: self.cuts+=' && nBJet>=2'
        elif 'nB2' in self.cutsID: self.cuts+=' && nBJet==2'
        if 'nB3p' in self.cutsID: self.cuts+=' && nBJet>=3'
        elif 'nB3' in self.cutsID: self.cuts+=' && nBJet==3'
        if 'nB4p' in self.cutsID: self.cuts+=' && nBJet>=4'
        elif 'nB4' in self.cutsID: self.cuts+=' && nBJet==4'
        
        if 'nT1p' in self.cutsID: self.cuts+=' && nTau>=1'
        elif 'nT1' in self.cutsID: self.cuts+=' && nTau==1'
        if 'nT2p' in self.cutsID: self.cuts+=' && nTau>=2'
        elif 'nT2' in self.cutsID: self.cuts+=' && nTau==2'

        if 'nV1p' in self.cutsID: self.cuts+=' && nW+nZ>=1'
        elif 'nV1' in self.cutsID: self.cuts+=' && nW+nZ==1'
        if 'nV2p' in self.cutsID: self.cuts+=' && nW+nZ>=2'
        elif 'nV2' in self.cutsID: self.cuts+=' && nW+nZ==2'

        if 'nZ1p' in self.cutsID: self.cuts+=' && nZ>=1'
        elif 'nZ1' in self.cutsID: self.cuts+=' && nZ==1'
        if 'nZ2p' in self.cutsID: self.cuts+=' && nZ>=2'
        elif 'nZ2' in self.cutsID: self.cuts+=' && nZ==2'
        
        if 'nh1p' in self.cutsID: self.cuts+=' && nh>=1'
        elif 'nh1' in self.cutsID: self.cuts+=' && nh==1'
        if 'nh2p' in self.cutsID: self.cuts+=' && nh>=2'
        elif 'nh2' in self.cutsID: self.cuts+=' && nh==2'
        
        if 'LepTrig' in self.cutsID: self.cuts+=' && ( passSingleLeptonTrigger==1 ||  passDiLeptonTrigger==1 )'
        
        global samples
        goodSamples=[]
        for sample in samples:
            if pileup+'PileUp' in sample.name:
                if (energy=='33' and energy in sample.name) or (energy=='14' and (energy in sample.name or '13' in sample.name)):
                    goodSamples.append(sample)
        samples=goodSamples

        #get histograms with proper normalization
        for sample in samples:
            sample.file=TFile(inputDir+'/'+sample.name+'.root')
            sample.tree=sample.file.Get(treeName)
            sample.nEvents=sample.tree.GetEntriesFast()
            hName=self.name+'__'+sample.name
            sample.h=TH1F(hName,";"+self.xTitle,self.nBins,self.bins)

            weight='eventWeight'
            nSelectedRaw=sample.tree.Draw(self.distribution+">>"+hName,weight+'*('+self.cuts+')','E GOFF')

            if not sample.crossSection:
                sample.setCrossSection(beta=0.7853981633974483, cosBetaMinusAlpha=-.5, twoHDMType=2)

            #print sample.crossSection
            if sample.h.Integral(0,self.nBins+1)!=0: sample.h.Scale(1000*lumi*sample.crossSection/sample.nEvents)
            result[sample.name]=sample.h.Integral(0,self.nBins+1) #for cutflow table
            
        #format histograms and draw plots
        output.cd()
        self.signals=[]
        self.backgroundStack=THStack()
        
        self.ewk=TH1F(self.name+'__ewk',';'+self.xTitle,self.nBins,self.bins)
        self.top=TH1F(self.name+'__top',';'+self.xTitle,self.nBins,self.bins)
        self.other=TH1F(self.name+'__other',';'+self.xTitle,self.nBins,self.bins)
        self.ewk.Sumw2()
        self.top.Sumw2()
        self.other.Sumw2()

        for sample in samples:
            if sample.isSignal:
                sample.h.Scale(signalMagFac)
                sample.h.SetLineColor(kBlack)
                sample.h.SetLineStyle(2+len(self.signals))
                self.signals.append(sample)
            elif sample.type=='top':
                self.top.Add(sample.h)
                print sample.name
            elif sample.type=='ewk': self.ewk.Add(sample.h)
            elif sample.isBackground: self.other.Add(sample.h)
            sample.h.SetLineWidth(2)
                        
        self.ewk.SetFillColor(ROOT.kGreen-3)
        self.ewk.SetLineColor(ROOT.kGreen-2)
        self.top.SetFillColor(ROOT.kRed-7)
        self.top.SetLineColor(ROOT.kRed-4)
        self.other.SetFillColor(ROOT.kBlue-3)
        self.other.SetLineColor(kBlue+2)

        self.backgroundStack.Add(self.other)
        self.backgroundStack.Add(self.ewk)
        self.backgroundStack.Add(self.top)

        self.background=self.backgroundStack.GetStack().Last().Clone(self.name+'__totalBackground')
        result['Total Background']=self.background.Integral(0,self.nBins+1)

        result['Total Signal']=0
        for signal in self.signals:
            result['Total Signal']+=signal.h.Integral(0,self.nBins+1)

        return result

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Draw(self):
        self.canvas=TCanvas(self.name,"",1000,800)
        if self.yLog: self.canvas.SetLogy()

        self.background.SetMaximum(2000*self.background.GetMaximum())
        self.background.SetMinimum(0.025)

        binWidth=round(self.background.GetBinWidth(1),5)
        if binWidth-round(binWidth)<.001*binWidth: binWidth=int(round(binWidth))
        yTitle="Events"
        if '[' in self.xTitle and ']' in self.xTitle: #get units from x axis title
            begin=self.xTitle.find('[')+1
            end=self.xTitle.find(']')
            yTitle+=' / '+str(binWidth)+' '+self.xTitle[begin:end]
        self.background.GetYaxis().SetTitle(yTitle)
            
        self.background.Draw("HIST") 
        self.backgroundStack.Draw("SAME HIST")
        for signal in self.signals:
            signal.h.Draw("SAME HIST")
        self.canvas.RedrawAxis()

        """
        for binNo in range(0,self.nBins+1):
            lumiUnc=0
            sigmaUnc=0
            statUnc=0
            for sample in samples:
                if sample.isBackground:
                    lumiUnc+=(sample.h.GetBinContent(binNo)*lumiFracUnc)**2
                    if sample.name=='WJets': sigmaFracUnc=wJetsSigmaFracUnc
                    elif sample.type=='top': sigmaFracUnc=ttbarSigmaFracUnc
                    else: sigmaFracUnc=otherSigmaFracUnc #WW, Z+Jets
                    sigmaUnc+=(sample.h.GetBinContent(binNo)*sigmaFracUnc)**2
                    statUnc+=sample.h.GetBinError(binNo)**2
            totalUnc=sqrt(lumiUnc+sigmaUnc+statUnc)
            self.uncBand.SetBinError(binNo,totalUnc)
            self.background.SetBinError(binNo,totalUnc)
        self.uncBand.SetFillStyle(3344)
        self.uncBand.SetFillColor(1)
        self.uncBand.SetLineColor(1)
        self.uncBand.SetMarkerSize(0)
        gStyle.SetHatchesLineWidth(1)
        self.uncBand.Draw("SAME E2")
        """
        
        legend=TLegend(0.65,0.65,0.90,0.90)
        legend.SetShadowColor(0);
        legend.SetFillColor(0);
        legend.SetLineColor(0);
        #legend.AddEntry(self.data,"Data")
        legend.AddEntry(self.top,"Top backgrounds", "f")
        legend.AddEntry(self.ewk,"EWK backgrounds","f")
        #legend.AddEntry(self.other,"Other backgrounds","f")
        for signal in self.signals:
            #mass=signal.GetName()[-3:]
            #legend.AddEntry(signal, "H^{#pm} x 20 (m="+mass+" GeV)", "l")
            legend.AddEntry(signal.h,signal.name,"l")
        #legend.AddEntry(self.uncBand , "Uncertainty" , "f")
        legend.Draw("SAME")
        
        prelimTex=TLatex()
        prelimTex.SetNDC()
        prelimTex.SetTextSize(0.04)
        prelimTex.SetTextAlign(31) # align right
        #lumi=lumi/1000.
        #lumi=round(lumi,2)
        prelimTex.DrawLatex(0.9, 0.95, str(lumi)+" fb^{-1} at #sqrt{s} = "+energy+" TeV");
        
        if self.cuts=="preselection" or self.cuts=='0p':
            bTagLabel="N_{b tags} #geq 0"

        """
        channelTex = TLatex()
        channelTex.SetNDC()
        channelTex.SetTextSize(0.08)
        channelTex.SetTextAlign(31)
        if self.channel=='el': text='e'
        elif self.channel=='mu': text='#mu'
        text+="+jets "+bTagLabel
        channelTex.DrawLatex(0.5, 0.83, text);
        """

        output.cd()
        self.canvas.Write()
        self.canvas.SaveAs(outputDir+'/'+self.name+'.pdf')
        self.canvas.SaveAs(outputDir+'/'+self.name+'.eps')

        for sample in samples:
            if sample.isSignal:
                sample.h.Scale(1./signalMagFac)
                if doLimitSetting: sample.h.Scale(1./sample.crossSection)
            
        self.ewk.Write()
        self.top.Write()
        self.other.Write()
        for sample in samples:
            if sample.isSignal or not doLimitSetting:
                sample.h.Write()
                
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        if doShapeComparison:
            if self.ewk.Integral(0,self.nBins+1)>0: self.ewk.Scale(1./self.ewk.Integral(0,self.nBins+1))
            self.ewk.SetFillColor(kWhite)
            if self.top.Integral(0,self.nBins+1)>0: self.top.Scale(1./self.top.Integral(0,self.nBins+1))
            self.top.SetFillColor(kWhite)
            if self.other.Integral(0,self.nBins+1)>0: self.other.Scale(1./self.other.Integral(0,self.nBins+1))
            self.other.SetFillColor(kWhite)
            for signal in self.signals:
                if signal.h.Integral(0,self.nBins+1)>0: signal.h.Scale(1./signal.h.Integral(0,self.nBins+1))
                signal.h.SetFillColor(kWhite)
            
            max=0
            for hist in [self.ewk,self.top,self.other]: #+self.signals:
                if hist.GetMaximum()>max: max=hist.GetMaximum()
            self.ewk.SetMaximum(1.1*max)
                        
            self.ewk.GetYaxis().SetTitle('Shape')

            self.canvas=TCanvas('shape_'+self.name,"",1000,800)
            self.ewk.Draw("HIST")
            self.top.Draw("SAME HIST")
            self.other.Draw("SAME HIST")
            for signal in self.signals: signal.h.Draw("SAME HIST")

            legend.Clear()
            legend.AddEntry(self.top,"Top backgrounds", "l")
            legend.AddEntry(self.ewk,"EWK backgrounds","l")
            #legend.AddEntry(self.other,"Other backgrounds","l")
            for signal in self.signals:
                #mass=signal.GetName()[-3:]
                legend.AddEntry(signal.h,signal.name,"l")
            legend.Draw("SAME")
            
            self.canvas.SaveAs(outputDir+'/shape_'+self.name+'.pdf')
            self.canvas.SaveAs(outputDir+'/shape_'+self.name+'.eps')

##################################################################################################################################################################
                                    
if __name__=='__main__':

    yields={}

    for cuts in doCuts:
        plots=[]
        if onlyDoCutTable:
            plots+=[TwoHiggsDoubletPlot(name='dummy',distribution='MET',nBins=1,xMin=0,xMax=9e9,cutsID=cuts)]
        else:        
            plots+=[#TwoHiggsDoubletPlot(name='MET',distribution='MET',nBins=25,xMin=0,xMax=500,xTitle='MET [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='ST',distribution='ST',nBins=100,xMin=0,xMax=2000,xTitle='S_{T} [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='HT',distribution='HT',nBins=60,xMin=0,xMax=1200,xTitle='H_{T} [GeV]',yLog=True,cutsID=cuts),

                    #TwoHiggsDoubletPlot(name='tau1_pT',distribution='tau1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(tau_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='bJet1_pT',distribution='bJet1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(b-jet_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='jet1_pT',distribution='jet1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(jet_{1}) [GeV]',yLog=True,cutsID=cuts),

                    #TwoHiggsDoubletPlot(name='tau2_pT',distribution='tau2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(tau_{2}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='bJet2_pT',distribution='bJet2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(b-jet_{2}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='jet2_pT',distribution='jet2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(jet_{2}) [GeV]',yLog=True,cutsID=cuts),

                    #TwoHiggsDoubletPlot(name='electron1_pT',distribution='electron1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(electron_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='electron2_pT',distribution='electron2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(electron_{2}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='electron3_pT',distribution='electron3_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(electron_{3}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='electron4_pT',distribution='electron4_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(electron_{4}) [GeV]',yLog=True,cutsID=cuts),
                    
                    #TwoHiggsDoubletPlot(name='muon1_pT',distribution='muon1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(muon_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='muon2_pT',distribution='muon2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(muon_{2}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='muon3_pT',distribution='muon3_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(muon_{3}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='muon4_pT',distribution='muon4_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(muon_{4}) [GeV]',yLog=True,cutsID=cuts),
                    
                    TwoHiggsDoubletPlot(name='lepton1_pT',distribution='lepton1_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(lepton_{1}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='lepton2_pT',distribution='lepton2_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(lepton_{2}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='lepton3_pT',distribution='lepton3_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(lepton_{3}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='lepton4_pT',distribution='lepton4_pT',nBins=40,xMin=0,xMax=400,xTitle='p_{T}(lepton_{4}) [GeV]',yLog=True,cutsID=cuts),

                    TwoHiggsDoubletPlot(name='nElectron',distribution='nElectron',nBins=8,xMin=-.5,xMax=7.5,xTitle='electron multiplicity',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='nMuon',distribution='nMuon',nBins=8,xMin=-.5,xMax=7.5,xTitle='muon multiplicity',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='nLepton',distribution='nElectron+nMuon',nBins=8,xMin=-.5,xMax=7.5,xTitle='lepton multiplicity',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='nZ',distribution='nZ',nBins=8,xMin=-.5,xMax=7.5,xTitle='Z boson multiplicity',yLog=True,cutsID=cuts),
                    
                    #TwoHiggsDoubletPlot(name='nTau',distribution='nTau',nBins=8,xMin=-.5,xMax=7.5,xTitle='tau multiplicity',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='nBJet',distribution='nBJet',nBins=8,xMin=-.5,xMax=7.5,xTitle='b-jet multiplicity',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='nJet',distribution='nJet',nBins=16,xMin=-.5,xMax=15.5,xTitle='jet multiplicity',yLog=True,cutsID=cuts),

                    #TwoHiggsDoubletPlot(name='mW1',distribution='W1_mass',nBins=50,xMin=50,xMax=150,xTitle='m(W_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='mh1',distribution='h1_mass',nBins=50,xMin=75,xMax=150,xTitle='m(h_{1}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='mH1',distribution='H1_mass',nBins=80,xMin=100,xMax=900,xTitle='m(H_{1}) [GeV]',yLog=True,cutsID=cuts),
                    #TwoHiggsDoubletPlot(name='mA1',distribution='A1_mass',nBins=50,xMin=300,xMax=700,xTitle='m(A_{1}) [GeV]',yLog=True,cutsID=cuts),
                    
                    TwoHiggsDoubletPlot(name='mZ1',distribution='Z1_mass',nBins=50,xMin=50,xMax=150,xTitle='m(Z_{1}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='mZ2',distribution='Z2_mass',nBins=50,xMin=50,xMax=150,xTitle='m(Z_{2}) [GeV]',yLog=True,cutsID=cuts),

                    TwoHiggsDoubletPlot(name='Z1_pT',distribution='Z1_pT',nBins=75,xMin=0,xMax=750,xTitle='p_{T}(Z_{1}) [GeV]',yLog=True,cutsID=cuts),
                    TwoHiggsDoubletPlot(name='Z2_pT',distribution='Z2_pT',nBins=75,xMin=0,xMax=750,xTitle='p_{T}(Z_{2}) [GeV]',yLog=True,cutsID=cuts),
                    ]

        for plot in plots:
            yields[cuts]=plot.Prepare()
            plot.Draw()

    sys.stdout = open(outputDir+'/'+tableOutput, "w")
    cWidth=15; nameWidth=30
    print "".ljust(nameWidth),
    for cuts in doCuts: print cuts.ljust(cWidth),
    print
    for sample in samples:
        if sample.isSignal: continue
        print sample.name.ljust(nameWidth),
        for cuts in doCuts:
            print str('%.3g'%yields[cuts][sample.name]).ljust(cWidth),
        print
    for sample in ['Total Background']:
        print sample.ljust(nameWidth),
        for cuts in doCuts:
            print str('%.3g'%yields[cuts][sample]).ljust(cWidth),
        print
    for sample in samples:
        if not sample.isSignal: continue
        print sample.name.ljust(nameWidth),
        for cuts in doCuts:
            print str('%.3g'%yields[cuts][sample.name]).ljust(cWidth),
        print

        print 'S/(sqrt(S+B)+(B*20%))'.ljust(nameWidth),
        for cuts in doCuts:
            try: val=yields[cuts][sample.name]/sqrt(yields[cuts][sample.name]+yields[cuts]['Total Background']+(.2*yields[cuts]['Total Background'])**2)
            except: val=float('Inf')
            print str('%.3g'%val).ljust(cWidth),
        print
        
    """    
    print 'S/B'.ljust(nameWidth),
    for cuts in doCuts:
        try: val=yields[cuts]['Total Signal']/yields[cuts]['Total Background']
        except: val=float('Inf')
        print str('%.3g'%val).ljust(cWidth),
    print
    print 'S/sqrt(S+B)'.ljust(nameWidth),
    for cuts in doCuts:
        try: val=yields[cuts]['Total Signal']/sqrt(yields[cuts]['Total Signal']+yields[cuts]['Total Background'])
        except: val=float('Inf')
        print str('%.3g'%val).ljust(cWidth),
    print
    print 'S/(sqrt(S+B)+(B*20%))'.ljust(nameWidth),
    for cuts in doCuts:
        try: val=yields[cuts]['Total Signal']/sqrt(yields[cuts]['Total Signal']+yields[cuts]['Total Background']+(.2*yields[cuts]['Total Background'])**2)
        except: val=float('Inf')
        print str('%.3g'%val).ljust(cWidth),
    print
    """
