from ROOT import *
gROOT.SetBatch(1)
from LJMet.Com.Sample import samplesForPlotting as samples
from LJMet.Com.Sample import signalForPlotting as signalsForPlotting
from LJMet.Com.Sample import signal as signals
from tdrStyle import *
from sys import argv
from array import array
import os
setTDRStyle()
gStyle.SetOptStat(False)

DEBUG=False

if len(argv)>1:
    inputDir=argv[1]
else:
    inputDir='/uscms_data/d1/jstupak/chargedHiggs/2013_2_18'

doCutTable=False
getWhfCorrections=False
doLimitSetting=False

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

doCuts=['0','1','2','3','4p']
#doCuts=['preselection','0','1','2','1p','2p','3p']
#doCuts=['preselection','0','1','2','1p','2p','3p','final']

doChannels=['el','mu']
#doChannels=['el']
#doChannels=['mu']

doShapeComparison=True

#3x3 matrix (W+light,W+heavy,ttbar)
residualSF_Wj=0.937195062637
residualSF_Wc=1.11306285858
residualSF_Wb=residualSF_Wc
residualSF_ttbar=1.07874298096

#These currently do nothing, just thinking ahead
doJES=False
doJER=False
doBTS=False
    
outputDir=inputDir+'/plots'

#H+- Cuts
sharedSelectionCuts='jet_0_pt_ChargedHiggsCalc > 50 && jet_1_pt_ChargedHiggsCalc > 30'
elSelectionCuts='elec_1_pt_ChargedHiggsCalc > 30 && abs(elec_1_eta_ChargedHiggsCalc) < 2.5 && elec_1_RelIso_ChargedHiggsCalc < 0.1  && corr_met_ChargedHiggsCalc > 20 && Muon_DeltaR_LjetsTopoCalcNew > 0.3'
muSelectionCuts='muon_1_pt_ChargedHiggsCalc > 26 && abs(muon_1_eta_ChargedHiggsCalc) < 2.1 && muon_1_RelIso_ChargedHiggsCalc < 0.12 && corr_met_ChargedHiggsCalc > 20 && Muon_DeltaR_LjetsTopoCalcNew > 0.3'

finalCuts='BestTop_Pt_LjetsTopoCalcNew > 85 && Jet1Jet2_Pt_LjetsTopoCalcNew > 140 && 130 < BestTop_LjetsTopoCalcNew && BestTop_LjetsTopoCalcNew < 210'

"""
#Wprime Cuts
sharedSelectionCuts='jet_0_pt_ChargedHiggsCalc > 120 && jet_1_pt_ChargedHiggsCalc > 40'
elSelectionCuts='elec_1_pt_ChargedHiggsCalc > 50 && abs(elec_1_eta_ChargedHiggsCalc) < 2.5 && elec_1_RelIso_ChargedHiggsCalc < 0.1  && corr_met_ChargedHiggsCalc > 20 && Muon_DeltaR_LjetsTopoCalcNew > 0.3'
muSelectionCuts='muon_1_pt_ChargedHiggsCalc > 50 && abs(muon_1_eta_ChargedHiggsCalc) < 2.1 && muon_1_RelIso_ChargedHiggsCalc < 0.12 && corr_met_ChargedHiggsCalc > 20 && Muon_DeltaR_LjetsTopoCalcNew > 0.3'

finalCuts='BestTop_Pt_LjetsTopoCalcNew > 85 && Jet1Jet2_Pt_LjetsTopoCalcNew > 140 && 130 < BestTop_LjetsTopoCalcNew && BestTop_LjetsTopoCalcNew < 210'
"""
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

elLumi=19624
muLumi=19624

treeName='ljmet'

SHyFT_Wj=1
SHyFT_Wc=1.66
SHyFT_Wb=1.21

lumiFracUnc = 0.022
ttbarSigmaFracUnc = 0.15
wJetsSigmaFracUnc = 0.20
otherSigmaFracUnc = 0.20
                
#---------------------------------------------------------------------------------------------------------------------------------------------

if doLimitSetting:
    doChannels=['el','mu']
    getWhfCorrections=False
    doCutTable=False
    for signal in signals:
        inSamples=False
        for sample in samples:
            if signal.name==sample.name: inSamples=True
        if not inSamples: samples.append(signal)
    samples=sorted(samples,key=lambda sample: sample.name)
    
if getWhfCorrections:
    doCuts=['preselection','0','1']
    doChannels=['mu']
    doCutTable=False
    doLimitSetting=False
    residualSF_Wj = 1
    residualSF_Wc = 1
    residualSF_Wb = 1
    residualSF_ttbar = 1
    
if doCutTable:
    getWhfCorrections=False
    doLimitSetting=False

#---------------------------------------------------------------------------------------------------------------------------------------------

SFWj=SHyFT_Wj*residualSF_Wj
SFWc=SHyFT_Wc*residualSF_Wc
SFWb=SHyFT_Wb*residualSF_Wb

if not os.path.isdir(outputDir): os.system("mkdir -p "+outputDir)
output=TFile(outputDir+'/plots.root',"RECREATE")

class ChargedHiggsPlot:

    def __init__(self,name,distribution,bins=None,nBins=100,xMin=0,xMax=100,xTitle='',yLog=True,cuts="0",extraCuts=None,channel='el'):
        self.name=name; self.distribution=distribution; self.bins=bins; self.nBins=nBins; self.xMin=xMin; self.xMax=xMax; self.xTitle=xTitle; self.yLog=yLog; self.cuts=cuts; self.extraCuts=extraCuts; self.channel=channel;

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
        
        cuts=sharedSelectionCuts
        if self.channel=='el': cuts+='&&'+elSelectionCuts
        elif self.channel=='mu': cuts+='&&'+muSelectionCuts

        if self.cuts=="preselection" or self.cuts=='0p':
            bTagCut='1'
        elif self.cuts=="0":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==0)'
        elif self.cuts=="1":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==1)'
        elif self.cuts=="1p" or self.cuts=="final":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)>=1)'
        elif self.cuts=="2":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==2)'
        elif self.cuts=="2p":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)>=2)'
        elif self.cuts=="3":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==3)'
        elif self.cuts=="3p":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)>=3)'
        elif self.cuts=="4":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==4)'
        elif self.cuts=="4p":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)>=4)'
        elif self.cuts=="5":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)==5)'
        elif self.cuts=="5p":
            bTagCut='((jet_0_tag_ChargedHiggsCalc + jet_1_tag_ChargedHiggsCalc + jet_2_tag_ChargedHiggsCalc + jet_3_tag_ChargedHiggsCalc + jet_4_tag_ChargedHiggsCalc + jet_5_tag_ChargedHiggsCalc)>=5)'
                                                
        if self.cuts=='final':
            cuts+='&& '+finalCuts

        if self.extraCuts: cuts+='&& '+self.extraCuts

        #make name unique
        self.name+='_nB'+self.cuts+'_'+self.channel

        if (self.channel == 'el'): self.lumi=elLumi
        elif (self.channel == 'mu'): self.lumi=muLumi

        #get histograms with proper normalization
        for sample in samples:
            #skip electron (muon) data for muon (electron) channel
            if (self.channel=='el' and 'SingleMu' in sample.name) or (self.channel=='mu' and 'SingleEl' in sample.name): continue
            
            sample.file=TFile(inputDir+'/'+sample.name+'.root')

            sample.tree=sample.file.Get(treeName)
            hName=self.name+'__'+sample.name
            sample.h=TH1F(hName,";"+self.xTitle,self.nBins,self.bins)

            weight='1'
            if sample.isMC:
                weight+='* weight_PU_ABCD_PileUpCalc'
                if (self.channel == 'el'):
                    weight+='* weight_ElectronEff_53x_ChargedHiggsCalc'
                    weight+='* (0.973*(abs(elec_1_eta_ChargedHiggsCalc)<1.5) + 1.02*(abs(elec_1_eta_ChargedHiggsCalc)>1.5&&abs(elec_1_eta_ChargedHiggsCalc)<2.5))'
                elif (self.channel == 'mu'): weight+='* weight_MuonEff_ChargedHiggsCalc'

            if sample.name=='WJets':
                self.Wlight=sample.h.Clone(self.name+'_light')
                self.Wc=sample.h.Clone(self.name+'_c')
                self.Wb=sample.h.Clone(self.name+'_b')
                            
                sample.tree.Draw(self.distribution+">>"+self.name+'_light',weight+'*'+str(SFWj)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_ChargedHiggsCalc==0 && n_Cjets_ChargedHiggsCalc==0)','E GOFF')
                sample.tree.Draw(self.distribution+">>"+self.name+'_c',weight+'*'+str(SFWc)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_ChargedHiggsCalc==0 && n_Cjets_ChargedHiggsCalc>0)','E GOFF')
                sample.tree.Draw(self.distribution+">>"+self.name+'_b',weight+'*'+str(SFWb)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_ChargedHiggsCalc>0)','E GOFF')

                sample.h.Add(self.Wlight)
                sample.h.Add(self.Wc)
                sample.h.Add(self.Wb)
                #Wnorm=sample.h.Integral(0,self.nBins+1)
                
                #get shape from untagged sample
                #sample.tree.Draw(self.distribution+">>"+self.name,weight+'*'+str(SFWj)+'*('+cuts+'&& n_Bjets_ChargedHiggsCalc==0 && n_Cjets_ChargedHiggsCalc==0)','E GOFF')
                #sample.tree.Draw(self.distribution+">>+"+self.name,weight+'*'+str(SFWc)+'*('+cuts+'&& n_Bjets_ChargedHiggsCalc==0 && n_Cjets_ChargedHiggsCalc>0)','E GOFF')
                #sample.tree.Draw(self.distribution+">>+"+self.name,weight+'*'+str(SFWb)+'*('+cuts+'&& n_Bjets_ChargedHiggsCalc>0)','E GOFF')
                #sample.h.Scale(Wnorm/sample.h.Integral(0,self.nBins+1)) #normalize to tagged integral
                
                self.Wlight.Scale(self.lumi*sample.crossSection/sample.nEvents)
                self.Wc.Scale(self.lumi*sample.crossSection/sample.nEvents)
                self.Wb.Scale(self.lumi*sample.crossSection/sample.nEvents)
                result['W+light']=self.Wlight.Integral(0,self.nBins+1)
                result['W+c']=self.Wc.Integral(0,self.nBins+1)
                result['W+b']=self.Wb.Integral(0,self.nBins+1)
                                                                
            else: 
                nSelectedRaw=sample.tree.Draw(self.distribution+">>"+hName,weight+'*('+cuts+'&&'+bTagCut+')','E GOFF')
                if 'TTbar' in sample.name:
                    sample.h.Scale(residualSF_ttbar)
                    self.ttbar=sample.h.Clone(self.name+'_ttbar')
                    self.ttbar.Scale(self.lumi*sample.crossSection/sample.nEvents)

            if sample.isMC and sample.h.Integral(0,self.nBins+1)!=0: sample.h.Scale(self.lumi*sample.crossSection/sample.nEvents)

            if DEBUG: #for event comparison
                if 'TTbar_Powheg' in sample.name and self.channel=='el':
                    sample.tree.SetScanField(0)
                    print '\n',sample.name,'   ',self.channel
                    sample.tree.Scan('run_CommonCalc:lumi_CommonCalc:event_CommonCalc:corr_met_ChargedHiggsCalc:jet_0_pt_ChargedHiggsCalc:jet_1_pt_ChargedHiggsCalc:elec_1_pt_ChargedHiggsCalc:elec_1_eta_ChargedHiggsCalc:elec_1_RelIso_ChargedHiggsCalc:muon_1_pt_ChargedHiggsCalc:muon_1_eta_ChargedHiggsCalc:muon_1_RelIso_ChargedHiggsCalc','('+cuts+'&&'+bTagCut+')')
                    
            result[sample.name]=sample.h.Integral(0,self.nBins+1) #for cutflow table

        #format histograms and draw plots
        output.cd()
        self.signals=[]
        self.backgroundStack=THStack()
        
        self.ewk=TH1F(self.name+'__ewk',';'+self.xTitle,self.nBins,self.bins)
        self.top=TH1F(self.name+'__top',';'+self.xTitle,self.nBins,self.bins)
        self.data=TH1F(self.name+'__DATA',';'+self.xTitle,self.nBins,self.bins)
        self.ewk.Sumw2()
        self.top.Sumw2()
        self.data.SetMarkerStyle(20)
        for sample in samples:
            if (self.channel=='el' and 'SingleMu' in sample.name) or (self.channel=='mu' and 'SingleEl' in sample.name): continue
            elif sample.isSignal:
                sample.h.Scale(20)
                sample.h.SetLineColor(1)
                sample.h.SetLineStyle(2+len(self.signals))
                self.signals+=[sample.h]
            elif sample.isBackground:
                if sample.name[0]=='T': self.top.Add(sample.h)
                else: self.ewk.Add(sample.h)
            elif sample.isData:
                self.data.Add(sample.h)
            sample.h.SetLineWidth(2)
                        
        self.ewk.SetFillColor(ROOT.kGreen-3)
        self.ewk.SetLineColor(ROOT.kGreen-2)
        self.top.SetFillColor(ROOT.kRed-7)
        self.top.SetLineColor(ROOT.kRed-4)

        self.backgroundStack.Add(self.ewk)
        self.backgroundStack.Add(self.top)

        self.background=self.backgroundStack.GetStack().Last().Clone(self.name+'_background')
        result['Total Background']=self.background.Integral(0,self.nBins+1)
        result['Data']=self.data.Integral(0,self.nBins+1)

        return result

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Draw(self):
        gStyle.SetErrorX(0.5)

        self.canvas=TCanvas(self.name,"",1000,800)

        yDiv=0.35
        self.uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
        self.uPad.SetTopMargin(0.07)
        self.uPad.SetBottomMargin(0)
        self.uPad.SetRightMargin(.05)
        self.uPad.SetLeftMargin(.18)
        self.uPad.Draw()
                                    
        self.lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
        self.lPad.SetTopMargin(0)
        self.lPad.SetBottomMargin(.4)
        self.lPad.SetRightMargin(.05)
        self.lPad.SetLeftMargin(.18)
        self.lPad.SetGridy()
        self.lPad.Draw()
                
        self.data.SetMaximum(2*self.data.GetMaximum())
        self.data.SetMinimum(0.025)

        binWidth=round(self.data.GetBinWidth(1),5)
        if binWidth-round(binWidth)<.001*binWidth: binWidth=int(round(binWidth))
        yTitle="Events"
        if '[' in self.xTitle and ']' in self.xTitle: #get units from x axis title
            begin=self.xTitle.find('[')+1
            end=self.xTitle.find(']')
            yTitle+=' / '+str(binWidth)+' '+self.xTitle[begin:end]
        self.data.GetYaxis().SetTitle(yTitle)
            
        self.formatUpperHist(self.data)

        self.uPad.cd()
        self.data.Draw("E1 X0") #draw data first because its easier to format a TH1 than a THStack
        self.backgroundStack.Draw("SAME HIST")
        for signal in self.signals:
            for s in signalsForPlotting:
                if s.name in signal.GetName(): signal.Draw("SAME HIST")
        self.data.Draw("SAME E1 X0") #redraw data so its not hidden
        self.uPad.RedrawAxis()

        #calculate stat+sys uncertainty
        self.uncBand=self.background.Clone("unc")
        for binNo in range(0,self.nBins+1):
            lumiUnc=0
            sigmaUnc=0
            statUnc=0
            for sample in samples:
                if sample.isBackground:
                    lumiUnc+=(sample.h.GetBinContent(binNo)*lumiFracUnc)**2
                    if sample.name=='WJets': sigmaFracUnc=wJetsSigmaFracUnc
                    elif sample.name[0]=='T': sigmaFracUnc=ttbarSigmaFracUnc
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
        
        legend=TLegend(0.55,0.55,0.90,0.90)
        legend.SetShadowColor(0);
        legend.SetFillColor(0);
        legend.SetLineColor(0);
        legend.AddEntry(self.data,"Data")
        legend.AddEntry(self.top,"t#bar{t} + Single-Top", "f")
        legend.AddEntry(self.ewk,"W#rightarrowl#nu + Z/#gamma*#rightarrowl^{+}l^{-} + VV" , "f")
        for signal in self.signals:
            mass=signal.GetName()[-3:]
            for s in signalsForPlotting:
                if s.name in signal.GetName(): legend.AddEntry(signal, "H^{#pm} x 20 (m="+mass+" GeV)", "l")
        legend.AddEntry(self.uncBand , "Uncertainty" , "f")
        legend.Draw("SAME")
        
        prelimTex=TLatex()
        prelimTex.SetNDC()
        prelimTex.SetTextSize(0.04)
        prelimTex.SetTextAlign(31) # align right
        lumi=self.lumi/1000.
        lumi=round(lumi,2)
        prelimTex.DrawLatex(0.9, 0.95, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");
        
        if self.cuts=="preselection" or self.cuts=='0p':
            bTagLabel="N_{b tags} #geq 0"
        elif self.cuts=="0":
            bTagLabel="N_{b tags} = 0"
        elif self.cuts=="1":
            bTagLabel="N_{b tags} = 1"
        elif self.cuts=="1p":
            bTagLabel="N_{b tags} #geq 1"
        elif self.cuts=="2":
            bTagLabel="N_{b tags} = 2"
        elif self.cuts=="2p":
            bTagLabel="N_{b tags} #geq 2"
        elif self.cuts=="3":
            bTagLabel="N_{b tags} = 3"
        elif self.cuts=="3p":
            bTagLabel="N_{b tags} #geq 3"
        elif self.cuts=="4":
            bTagLabel="N_{b tags} = 4"
        elif self.cuts=="4p":
            bTagLabel="N_{b tags} #geq 4"
        elif self.cuts=="5":
            bTagLabel="N_{b tags} = 5"
        elif self.cuts=="5p":
            bTagLabel="N_{b tags} #geq 5"
        elif self.cuts=="final":
            bTagLabel="N_{b tags} #geq 1"

            
        channelTex = TLatex()
        channelTex.SetNDC()
        channelTex.SetTextSize(0.08)
        channelTex.SetTextAlign(31)
        if self.channel=='el': text='e'
        elif self.channel=='mu': text='#mu'
        text+="+jets "+bTagLabel
        channelTex.DrawLatex(0.5, 0.83, text);

        self.lPad.cd()
        self.pull=self.data.Clone("pull")
        for binNo in range(0,self.nBins+1):
            if self.background.GetBinError(binNo)!=0:
                self.pull.SetBinContent(binNo,(self.data.GetBinContent(binNo)-self.background.GetBinContent(binNo))/self.background.GetBinError(binNo))
        self.pull.SetMaximum(3)
        self.pull.SetMinimum(-3)
        self.pull.SetFillColor(2)
        self.pull.SetLineColor(2)
        self.formatLowerHist(self.pull)
        self.pull.GetYaxis().SetTitle('#sigma(Data-MC)')
        self.pull.Draw("HIST")

        output.cd()
        self.canvas.Write()
        self.canvas.SaveAs(outputDir+'/'+self.name+'.pdf')
        self.canvas.SaveAs(outputDir+'/'+self.name+'.eps')

        for sample in samples:
            if sample.isSignal:
                sample.h.Scale(1./20)
                if doLimitSetting:
                    sample.h.Scale(1./sample.crossSection)

        if not doLimitSetting:
            self.Wlight.Write()
            self.Wc.Write()
            self.Wb.Write()
            self.ttbar.Write()
        
        self.data.Write()
        self.ewk.Write()
        self.top.Write()
        for sample in samples:
            if sample.isSignal or not doLimitSetting:
                try: sample.h.Write()
                except: pass
                
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        if doShapeComparison:
            if self.ewk.Integral(0,self.nBins+1)>0: self.ewk.Scale(1./self.ewk.Integral(0,self.nBins+1))
            self.ewk.SetFillColor(kWhite)
            if self.top.Integral(0,self.nBins+1)>0: self.top.Scale(1./self.top.Integral(0,self.nBins+1))
            self.top.SetFillColor(kWhite)
            for signal in self.signals:
                if signal.Integral(0,self.nBins+1)>0: signal.Scale(1./signal.Integral(0,self.nBins+1))
                signal.SetFillColor(kWhite)
            
            max=0
            for hist in [self.ewk,self.top]+self.signals:
                if hist.GetMaximum()>max: max=hist.GetMaximum()
            self.ewk.SetMaximum(1.1*max)
                        
            #self.formatUpperHist(self.ewk);
            self.ewk.GetYaxis().SetTitle('Shape')
            
            ewkEff=self.ewk.Clone('ewkEff')
            #self.formatLowerHist(ewkEff)
            ewkEff.GetYaxis().SetTitle('1-Integral')
            ewkEff.SetMinimum(.8)
            ewkEff.SetMaximum(1)
            
            topEff=self.top.Clone('topEff')
            signalEffs=[]
            for signal in self.signals: signalEffs.append(signal.Clone('signalEff'+str(len(signalEffs)))); 

            for binNo in range(1,self.nBins+1):
                ewkEff.SetBinContent(binNo,1-self.ewk.Integral(0,binNo))
                topEff.SetBinContent(binNo,1-self.top.Integral(0,binNo))
                for signal,signalEff in zip(self.signals,signalEffs): signalEff.SetBinContent(binNo,1-signal.Integral(0,binNo))

            self.canvas=TCanvas('shape_'+self.name,"",1000,800)
            #self.uPad.cd()
            self.ewk.Draw()
            self.top.Draw("SAME")
            for signal in self.signals: signal.Draw("SAME")

            legend.Clear()
            legend.AddEntry(self.top,"t#bar{t} + Single-Top", "l")
            legend.AddEntry(self.ewk,"W#rightarrowl#nu + Z/#gamma*#rightarrowl^{+}l^{-} + VV" , "l")
            for signal in self.signals:
                mass=signal.GetName()[-3:]
                for s in signalsForPlotting:
                    if s.name in signal.GetName(): legend.AddEntry(signal, "H^{#pm} (m="+mass+" GeV)", "l")
            legend.Draw("SAME")

            #self.lPad.cd()
            #ewkEff.Draw("C")
            #topEff.Draw("SAME C")
            #for signalEff in signalEffs: signalEff.Draw("SAME C")
            
            self.canvas.SaveAs(outputDir+'/shape_'+self.name+'.pdf')
            self.canvas.SaveAs(outputDir+'/shape_'+self.name+'.eps')

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
 
    def formatUpperHist(self,histogram):
        histogram.GetXaxis().SetLabelSize(0)

        histogram.GetYaxis().CenterTitle()
        histogram.GetYaxis().SetLabelSize(0.08)
        histogram.GetYaxis().SetTitleSize(0.12)
        histogram.GetYaxis().SetTitleOffset(.75)
                
        if self.yLog:
            self.uPad.SetLogy()
            histogram.SetMaximum(500*histogram.GetMaximum())
            
    #---------------------------------------------------------------------------------------------------------------------------------------------------------

    def formatLowerHist(self,histogram):
        histogram.GetXaxis().SetLabelSize(.15)
        histogram.GetXaxis().SetTitleSize(0.18)
        histogram.GetXaxis().SetTitleOffset(0.95)
        histogram.GetXaxis().SetTitle(self.xTitle)

        histogram.GetYaxis().SetLabelSize(0.125)
        histogram.GetYaxis().SetTitleSize(0.1)
        histogram.GetYaxis().SetTitleOffset(.55)
        histogram.GetYaxis().SetNdivisions(5);
        
##################################################################################################################################################################
                                    
if __name__=='__main__':

    yields={}
    plots=[]
    for cuts in doCuts:
        yields[cuts]={}
        if doCutTable:
            plots+=[ChargedHiggsPlot(name='electron0_pt',distribution='elec_1_pt_ChargedHiggsCalc',nBins=100,xMin=0,xMax=7000,xTitle='electron p_{T} [GeV]',yLog=True,cuts=cuts,channel='el'),
                    ChargedHiggsPlot(name='muon0_pt',distribution='muon_1_pt_ChargedHiggsCalc',nBins=100,xMin=0,xMax=7000,xTitle='muon p_{T} [GeV]',yLog=True,cuts=cuts,channel='mu')
                    ]

        elif getWhfCorrections:
            plots+=[ChargedHiggsPlot(name='muon0_pt',distribution='muon_1_pt_ChargedHiggsCalc',nBins=100,xMin=0,xMax=7000,xTitle='muon p_{T} [GeV]',yLog=True,cuts=cuts,channel='mu')]

        else:
            plots+=[#ChargedHiggsPlot(name='electron0_pt',distribution='elec_1_pt_ChargedHiggsCalc',nBins=70,xMin=0,xMax=700,xTitle='electron p_{T} [GeV]',yLog=True,cuts=cuts,channel='el'),
                    #ChargedHiggsPlot(name='electron0_eta',distribution='elec_1_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='electron #eta',yLog=False,cuts=cuts,channel='el'),
                    #ChargedHiggsPlot(name='electron0_RelIso',distribution='elec_1_RelIso_ChargedHiggsCalc',nBins=30,xMin=0,xMax=0.15,xTitle='electron Rel. Isolation',yLog=True,cuts=cuts,channel='el'),

                    #ChargedHiggsPlot(name='muon0_pt',distribution='muon_1_pt_ChargedHiggsCalc',nBins=70,xMin=6,xMax=706,xTitle='muon p_{T} [GeV]',yLog=True,cuts=cuts,channel='mu'),
                    #ChargedHiggsPlot(name='muon0_eta',distribution='muon_1_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='muon #eta',yLog=False,cuts=cuts,channel='mu'),
                    #ChargedHiggsPlot(name='muon0_RelIso',distribution='muon_1_RelIso_ChargedHiggsCalc',nBins=30,xMin=0,xMax=0.15,xTitle='muon Rel. Isolation',yLog=True,cuts=cuts,channel='mu')
                    ]


            for channel in doChannels:
                plots+=[###ChargedHiggsPlot(name='BestJetJet2W_M',distribution='BestJetJet2W_M_LjetsTopoCalcNew',nBins=68,xMin=100,xMax=3500,xTitle='M(tb) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        ###ChargedHiggsPlot(name='Jet1Jet2W_M',distribution='Jet1Jet2W_M_LjetsTopoCalcNew',nBins=68,xMin=100,xMax=3500,xTitle='M(tb) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='corr_met',distribution='corr_met_ChargedHiggsCalc',nBins=70,xMin=0,xMax=700,xTitle='E_{T}^{miss} [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet0_pt',distribution='jet_0_pt_ChargedHiggsCalc',nBins=100,xMin=0,xMax=1000,xTitle='p_{T} (jet1) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet0_eta',distribution='jet_0_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet1)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet1_pt',distribution='jet_1_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet2) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet1_eta',distribution='jet_1_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet2)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet2_pt',distribution='jet_2_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet3) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet2_eta',distribution='jet_2_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet3)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet3_pt',distribution='jet_3_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet4) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet3_eta',distribution='jet_3_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet4)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet4_pt',distribution='jet_4_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet5) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet4_eta',distribution='jet_4_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet5)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet5_pt',distribution='jet_5_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet6) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet5_eta',distribution='jet_5_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet6)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet6_pt',distribution='jet_6_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet7) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet6_eta',distribution='jet_6_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet7)',yLog=False,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet7_pt',distribution='jet_7_pt_ChargedHiggsCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet8) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='PFjet7_eta',distribution='jet_7_eta_ChargedHiggsCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet8)',yLog=False,cuts=cuts,channel=channel),
                        
                        ###ChargedHiggsPlot(name='TopMass_Best',distribution='BestTop_LjetsTopoCalcNew',nBins=100,xMin=0,xMax=1000,xTitle='M(best jet,W) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        ###ChargedHiggsPlot(name='TopPt_Best',distribution='BestTop_Pt_LjetsTopoCalcNew',nBins=150,xMin=0,xMax=1500,xTitle='p_{T}(best jet,W) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='Pt_Jet1Jet2',distribution='Jet1Jet2_Pt_LjetsTopoCalcNew',nBins=150,xMin=0,xMax=1500,xTitle='p_{T}(jet1,jet2) [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='HT',distribution='Ht_LjetsTopoCalcNew',nBins=125,xMin=0,xMax=2500,xTitle='H_{T} [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='ST',distribution='jet_0_pt_ChargedHiggsCalc+jet_1_pt_ChargedHiggsCalc+((elec_1_pt_ChargedHiggsCalc>0)*elec_1_pt_ChargedHiggsCalc)+((muon_1_pt_ChargedHiggsCalc>0)*muon_1_pt_ChargedHiggsCalc)+corr_met_ChargedHiggsCalc',nBins=150,xMin=0,xMax=3000,xTitle='S_{T} [GeV]',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='nPV',distribution='nPV_ChargedHiggsCalc',nBins=50,xMin=0,xMax=50,xTitle='# Vertices',yLog=True,cuts=cuts,channel=channel),
                        #ChargedHiggsPlot(name='Nj',distribution='nSelJets_CommonCalc',nBins=7,xMin=1.5,xMax=8.5,xTitle='N_{jets}',yLog=True,cuts=cuts,channel=channel)
                        ]
                
    if not yields.has_key('preselection'): yields['preselection']={}
    if (not doCutTable) and (not getWhfCorrections) and (not doLimitSetting):
        for channel in doChannels:
            plots+=[ChargedHiggsPlot(name='Nb',distribution='(jet_0_tag_ChargedHiggsCalc==1)+(jet_1_tag_ChargedHiggsCalc==1)+(jet_2_tag_ChargedHiggsCalc==1)+(jet_3_tag_ChargedHiggsCalc==1)+(jet_4_tag_ChargedHiggsCalc==1)+(jet_5_tag_ChargedHiggsCalc==1)+(jet_6_tag_ChargedHiggsCalc==1)+(jet_7_tag_ChargedHiggsCalc==1)+(jet_8_tag_ChargedHiggsCalc==1)+(jet_9_tag_ChargedHiggsCalc==1)',nBins=7,xMin=-0.5,xMax=6.5,xTitle='N_{b-jets}',yLog=True,cuts='preselection',channel=channel),

                    #for top pT reweighting
                    ChargedHiggsPlot(name='TopPt_Best',distribution='BestTop_Pt_LjetsTopoCalcNew',nBins=150,xMin=0,xMax=1500,xTitle='p_{T}(best jet,W) [GeV]',yLog=True,cuts='2p',channel=channel,extraCuts='jet_2_pt_ChargedHiggsCalc>30 && jet_3_pt_ChargedHiggsCalc>30 && 400<BestJetJet2W_M_LjetsTopoCalcNew && BestJetJet2W_M_LjetsTopoCalcNew<750')
                    ]
                        
                        
    for plot in plots:
        y=plot.Prepare()
        try: yields[plot.cuts][plot.channel]=y
        except: pass
        plot.Draw()

    cWidth=15; nameWidth=30
    for channel in doChannels:
        print ("CHANNEL:"+channel).ljust(nameWidth+(2*cWidth+1)),"N_b"
        print "".ljust(nameWidth),
        for cuts in doCuts: print cuts.ljust(cWidth),
        print
        for sample in ['Data','W+light','W+c','W+b']:
            print sample.ljust(nameWidth),
            for cuts in doCuts:
                print str(int(round(yields[cuts][channel][sample]))).ljust(cWidth),
                #print str(yields[cuts][channel][sample]).ljust(cWidth),
            print
        for sample in samples:
            if (channel=='el' and 'SingleMu' in sample.name) or (channel=='mu' and 'SingleEl' in sample.name): continue
            #if sample.isData: continue
            print sample.name.ljust(nameWidth),
            for cuts in doCuts:
                print str(int(round(yields[cuts][channel][sample.name]))).ljust(cWidth),
                #print str(yields[cuts][channel][sample.name]).ljust(cWidth),
            print
        for sample in ['Total Background']:
            print sample.ljust(nameWidth),
            for cuts in doCuts:
                print str(int(round(yields[cuts][channel][sample]))).ljust(cWidth),
                #print str(yields[cuts][channel][sample]).ljust(cWidth),
            print
        print 'Background/Data'.ljust(nameWidth),
        for cuts in doCuts:
            print str(round(yields[cuts][channel]['Total Background']/yields[cuts][channel]['Data'],3)).ljust(cWidth),
        print 3*'\n'
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    if getWhfCorrections:

        """
        Ndata=TMatrix(2,1)
        Nw=TMatrix(2,2)
        Nother=TMatrix(2,1)
        SF=TMatrix(2,1)
        
        Ndata[0][0]=yields['0']['mu']['Data']
        Nother[0][0]=yields['0']['mu']['Total Background']-yields['0']['mu']['W+light']-yields['0']['mu']['W+c']-yields['0']['mu']['W+b']
        Nw[0][0]=yields['0']['mu']['W+light']
        Nw[0][1]=yields['0']['mu']['W+c']+yields['0']['mu']['W+b']
            
        Ndata[1][0]=yields['1']['mu']['Data']
        Nother[1][0]=yields['1']['mu']['Total Background']-yields['1']['mu']['W+light']-yields['1']['mu']['W+c']-yields['1']['mu']['W+b']
        Nw[1][0]=yields['1']['mu']['W+light']
        Nw[1][1]=yields['1']['mu']['W+c']+yields['1']['mu']['W+b']
                        
        SF=Nw.Invert()*(Ndata-Nother) 
        print "residualSF_Wj="+str(SF[0][0])
        print "residualSF_Wc="+str(SF[1][0])
        print "residualSF_Wb="+str(SF[1][0])
        """
        """
        Ndata=TMatrix(3,1)
        Nw=TMatrix(3,3)
        Nother=TMatrix(3,1)
        SF=TMatrix(3,1)
        
        channel='mu'

        Ndata[0][0]=yields['preselection'][channel]['Data']
        Nother[0][0]=yields['preselection'][channel]['Total Background']-yields['preselection'][channel]['W+light']-yields['preselection'][channel]['W+c']-yields['preselection'][channel]['W+b']
        Nw[0][0]=yields['preselection'][channel]['W+light']
        Nw[0][1]=yields['preselection'][channel]['W+c']
        Nw[0][2]=yields['preselection'][channel]['W+b']
                
        Ndata[1][0]=yields['0'][channel]['Data']
        Nother[1][0]=yields['0'][channel]['Total Background']-yields['0'][channel]['W+light']-yields['0'][channel]['W+c']-yields['0'][channel]['W+b']
        Nw[1][0]=yields['0'][channel]['W+light']
        Nw[1][1]=yields['0'][channel]['W+c']
        Nw[1][2]=yields['0'][channel]['W+b']
                
        Ndata[2][0]=yields['1'][channel]['Data']
        Nother[2][0]=yields['1'][channel]['Total Background']-yields['1'][channel]['W+light']-yields['1'][channel]['W+c']-yields['1'][channel]['W+b']
        Nw[2][0]=yields['1'][channel]['W+light']
        Nw[2][1]=yields['1'][channel]['W+c']
        Nw[2][2]=yields['1'][channel]['W+b']
        
        SF=Nw.Invert()*(Ndata-Nother)
        print 'SF W+light:',SF[0][0]
        print 'SF W+c:',SF[1][0]
        print 'SF W+b:',SF[2][0]
        """

        Ndata=TMatrix(3,1)
        Nw=TMatrix(3,3)
        Nother=TMatrix(3,1)
        SF=TMatrix(3,1)
        
        channel='mu'

        Ndata[0][0]=yields['preselection'][channel]['Data']
        Nother[0][0]=yields['preselection'][channel]['Total Background']-yields['preselection'][channel]['W+light']-yields['preselection'][channel]['W+c']-yields['preselection'][channel]['W+b']-yields['preselection'][channel]['TTbar_Madgraph']
        Nw[0][0]=yields['preselection'][channel]['W+light']
        Nw[0][1]=yields['preselection'][channel]['W+c']+yields['preselection'][channel]['W+b']
        Nw[0][2]=yields['preselection'][channel]['TTbar_Madgraph']
        
        Ndata[1][0]=yields['0'][channel]['Data']
        Nother[1][0]=yields['0'][channel]['Total Background']-yields['0'][channel]['W+light']-yields['0'][channel]['W+c']-yields['0'][channel]['W+b']-yields['0'][channel]['TTbar_Madgraph']
        Nw[1][0]=yields['0'][channel]['W+light']
        Nw[1][1]=yields['0'][channel]['W+c']+yields['0'][channel]['W+b']
        Nw[1][2]=yields['0'][channel]['TTbar_Madgraph']

        Ndata[2][0]=yields['1'][channel]['Data']
        Nother[2][0]=yields['1'][channel]['Total Background']-yields['1'][channel]['W+light']-yields['1'][channel]['W+c']-yields['1'][channel]['W+b']-yields['1'][channel]['TTbar_Madgraph']
        Nw[2][0]=yields['1'][channel]['W+light']
        Nw[2][1]=yields['1'][channel]['W+c']+yields['1'][channel]['W+b']
        Nw[2][2]=yields['1'][channel]['TTbar_Madgraph']
                                                            
        SF=Nw.Invert()*(Ndata-Nother)
        print "residualSF_Wj="+str(SF[0][0])
        print "residualSF_Wc="+str(SF[1][0])
        print "residualSF_Wb=residualSF_Wc"
        print "residualSF_ttbar="+str(SF[2][0])

