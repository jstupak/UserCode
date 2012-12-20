from ROOT import *
gROOT.SetBatch(1)
from LJMet.Com.Sample import samplesForPlotting as samples
from tdrStyle import *
setTDRStyle()
gStyle.SetOptStat(False)

DEBUG=False

inputDir='/uscms_data/d1/jstupak/analysisOutputs/'
inputDir+='2012_12_16/newEventSelTest'

bJetRequirements=['0p','0','1','1p','2p']

channels=['el','mu']

doCutTable=True
doFracFit=True
    
outputName=inputDir+'/plots.root'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

elLumi=6732.0
muLumi=12211.0

treeName='ljmet'

sharedSelectionCuts='jet_0_pt_WprimeCalc >= 100 && jet_1_pt_WprimeCalc >= 40'
elSelectionCuts='elec_1_pt_WprimeCalc > 30 && abs(elec_1_eta_WprimeCalc) < 2.5 && elec_1_RelIso_WprimeCalc < 0.1  && corr_met_WprimeCalc > 20'
muSelectionCuts='muon_1_pt_WprimeCalc > 26 && abs(muon_1_eta_WprimeCalc) < 2.1 && muon_1_RelIso_WprimeCalc < 0.12 && corr_met_WprimeCalc > 20'

SFWj = 0.85
SFWc = 0.92*1.66
SFWb = 0.92*1.21

lumiFracUnc = 0.022
ttbarSigmaFracUnc = 0.15
wJetsSigmaFracUnc = 0.20
otherSigmaFracUnc = 0.20
                
#---------------------------------------------------------------------------------------------------------------------------------------------

output=TFile(outputName,"RECREATE")
bkgdNorms={}
QCDFrac={}
QCDFracUnc={}
fakeRate={}
fitChi2={}
fitNDF={}

class WPrimePlot:
    
    def __init__(self,name,distribution,nBins=100,xMin=0,xMax=100,xTitle='',yLog=True,nB="0",otherCuts='',channel='el'):
        self.name=name; self.distribution=distribution; self.nBins=nBins; self.xMin=xMin; self.xMax=xMax; self.xTitle=xTitle; self.yLog=yLog; self.nB=nB; self.otherCuts=otherCuts; self.channel=channel;
        if not bkgdNorms.has_key(self.nB): bkgdNorms[self.nB]={}
        if not QCDFrac.has_key(self.nB):
            QCDFrac[self.nB]={}
            QCDFracUnc[self.nB]={}
            fakeRate[self.nB]={}
            fitChi2[self.nB]={}
            fitNDF[self.nB]={}
                      
    def Prepare(self):
        result={}
        
        cuts=sharedSelectionCuts
        if self.channel=='el': cuts+='&&'+elSelectionCuts
        elif self.channel=='mu': cuts+='&&'+muSelectionCuts

        if self.nB=="0":
            bTagCut='((jet_0_tag_WprimeCalc + jet_1_tag_WprimeCalc)==0)'
        elif self.nB=="0p":
            bTagCut='1'
        elif self.nB=="1":
            bTagCut='((jet_0_tag_WprimeCalc + jet_1_tag_WprimeCalc)==1)'
        elif self.nB=="1p":
            bTagCut='((jet_0_tag_WprimeCalc + jet_1_tag_WprimeCalc)>=1)'
        elif self.nB=="2":
            bTagCut='((jet_0_tag_WprimeCalc + jet_1_tag_WprimeCalc)==2)'
        elif self.nB=="2p":
            #bTagCut='((jet_0_tag_WprimeCalc + jet_1_tag_WprimeCalc)>=2)'
            bTagCut='((jet_0_tag_WprimeCalc==1 && (jet_1_tag_WprimeCalc + jet_2_tag_WprimeCalc + jet_3_tag_WprimeCalc + jet_4_tag_WprimeCalc + jet_5_tag_WprimeCalc + jet_6_tag_WprimeCalc + jet_7_tag_WprimeCalc + jet_8_tag_WprimeCalc + jet_9_tag_WprimeCalc) >= 1 ) || (jet_1_tag_WprimeCalc==1 && (jet_0_tag_WprimeCalc + jet_2_tag_WprimeCalc + jet_3_tag_WprimeCalc + jet_4_tag_WprimeCalc + jet_5_tag_WprimeCalc + jet_6_tag_WprimeCalc + jet_7_tag_WprimeCalc + jet_8_tag_WprimeCalc + jet_9_tag_WprimeCalc) >= 1))'

        #make name unique
        self.name+='_nB'+self.nB+'_'+self.channel

        if (self.channel == 'el'): lumi=elLumi
        elif (self.channel == 'mu'): lumi=muLumi

        #get histograms with proper normalization
        for sample in samples:
            #skip electron (muon) data for muon (electron) channel
            if (self.channel=='el' and 'SingleMu' in sample.name) or (self.channel=='mu' and 'SingleEl' in sample.name): continue
            
            sample.file=TFile(inputDir+'/'+sample.name+'.root')
            sample.tree=sample.file.Get(treeName)
            hName=self.name+'_'+sample.name
            sample.h=TH1F(hName,";"+self.xTitle,self.nBins,self.xMin,self.xMax)

            if sample.tree.GetLeaf('sampleWeight_WprimeCalc'): weight='sampleWeight_WprimeCalc'
            else: weight='1' #for backwards compatibility

            if sample.isMC:
                SF=1. #not currently being used
                weight+='*weight_PU_ABC_PileUpCalc'
                if (self.channel == 'el'): weight+='*weight_ElectronEff_WprimeCalc'
                elif (self.channel == 'mu'): weight+='*weight_MuonEff_WprimeCalc'

            if sample.name=='WJets':
                sample.tree.Draw(self.distribution+">>"+hName,weight+'*'+str(SFWj)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_WprimeCalc==0 && n_Cjets_WprimeCalc==0)','goff')
                sample.tree.Draw(self.distribution+">>+"+hName,weight+'*'+str(SFWc)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_WprimeCalc==0 && n_Cjets_WprimeCalc>0)','goff')
                sample.tree.Draw(self.distribution+">>+"+hName,weight+'*'+str(SFWb)+'*('+cuts+'&&'+bTagCut+'&& n_Bjets_WprimeCalc>0)','goff')
                bTagEff=sample.h.Integral(0,self.nBins+1)

                #get shape from untagged sample
                sample.tree.Draw(self.distribution+">>"+hName,weight+'*'+str(SFWj)+'*('+cuts+'&& n_Bjets_WprimeCalc==0 && n_Cjets_WprimeCalc==0)','goff')
                result['W+light']=sample.h.Integral(0,self.nBins+1)
                sample.tree.Draw(self.distribution+">>+"+hName,weight+'*'+str(SFWc)+'*('+cuts+'&& n_Bjets_WprimeCalc==0 && n_Cjets_WprimeCalc>0)','goff')
                result['W+c']=sample.h.Integral(0,self.nBins+1)-result['W+light']
                sample.tree.Draw(self.distribution+">>+"+hName,weight+'*'+str(SFWb)+'*('+cuts+'&& n_Bjets_WprimeCalc>0)','goff')
                result['W+b']=sample.h.Integral(0,self.nBins+1)-result['W+light']-result['W+c']
                bTagEff/=sample.h.Integral(0,self.nBins+1)

                sample.h.Scale(bTagEff) #get proper normalization
                result['W+b']*=bTagEff*SF*lumi*sample.crossSection/sample.nEvents
                result['W+c']*=bTagEff*SF*lumi*sample.crossSection/sample.nEvents
                result['W+b']*=bTagEff*SF*lumi*sample.crossSection/sample.nEvents
                
            else: 
                nSelectedRaw=sample.tree.Draw(self.distribution+">>"+hName,weight+'*('+cuts+'&&'+bTagCut+')','goff')

            if sample.isMC and sample.h.Integral(0,self.nBins+1)!=0: sample.h.Scale(SF*lumi*sample.crossSection/sample.nEvents)

            if DEBUG: #for event comparison
                if 'TTbar_Powheg' in sample.name and self.channel=='el':
                    sample.tree.SetScanField(0)
                    print '\n',sample.name,'   ',self.channel
                    sample.tree.Scan('run_CommonCalc:lumi_CommonCalc:event_CommonCalc:corr_met_WprimeCalc:jet_0_pt_WprimeCalc:jet_1_pt_WprimeCalc:elec_1_pt_WprimeCalc:elec_1_eta_WprimeCalc:elec_1_RelIso_WprimeCalc:muon_1_pt_WprimeCalc:muon_1_eta_WprimeCalc:muon_1_RelIso_WprimeCalc','('+cuts+'&&'+bTagCut+')')
                    
            result[sample.name]=sample.h.Integral(0,self.nBins+1) #for cutflow table

        #format histograms and draw plots
        output.cd()
        self.signals=[]
        self.backgroundStack=THStack()
        self.ewk=TH1F(self.name+'_ewk',';'+self.xTitle,self.nBins,self.xMin,self.xMax)
        self.top=TH1F(self.name+'_top',';'+self.xTitle,self.nBins,self.xMin,self.xMax)
        self.qcd=TH1F(self.name+'_qcd',';'+self.xTitle,self.nBins,self.xMin,self.xMax)
        self.data=TH1F(self.name+'_data',';'+self.xTitle,self.nBins,self.xMin,self.xMax)
        self.data.SetMarkerStyle(20)
        for sample in samples:
            if (self.channel=='el' and 'SingleMu' in sample.name) or (self.channel=='mu' and 'SingleEl' in sample.name): continue
            elif sample.doQCD:
                self.qcd.Add(sample.h)
            elif sample.isSignal:
                sample.h.Scale(20)
                sample.h.SetLineColor(1)
                sample.h.SetLineStyle(6+len(self.signals))
                self.signals+=[sample.h]
            elif sample.isBackground:
                if sample.name[0]=='T': self.top.Add(sample.h)
                else: self.ewk.Add(sample.h)
            elif sample.isData: self.data.Add(sample.h)
            sample.h.SetLineWidth(2)
                        
        self.qcd.SetFillColor(ROOT.kBlue)
        self.qcd.SetLineColor(ROOT.kBlue+2)
        self.ewk.SetFillColor(ROOT.kGreen-3)
        self.ewk.SetLineColor(ROOT.kGreen-2)
        self.top.SetFillColor(ROOT.kRed-7)
        self.top.SetLineColor(ROOT.kRed-4)

        #get QCD normalization
        if doFracFit:
            #zero out any negetive bins if present
            for binNo in range(0,self.nBins+1):
                if self.qcd.GetBinContent(binNo)<0:
                    self.qcd.SetBinContent(binNo,0)
                    self.qcd.SetBinError(binNo,0)
            if not bkgdNorms[self.nB].has_key(self.channel): #if fit hasn't been performed yet for this channel/multiplicity
                bkgdNorms[self.nB][self.channel]=self.getNorms() #do the fit
                if bkgdNorms[self.nB][self.channel]: #if fit was succesful
                    value=Double()
                    error=Double()
                    self.fitter.GetResult(0,value,error)
                    QCDFrac[self.nB][self.channel]=value
                    QCDFracUnc[self.nB][self.channel]=error
                    fitChi2[self.nB][self.channel]=self.fitter.GetChisquare()
                    fitNDF[self.nB][self.channel]=self.fitter.GetNDF()
                    fakeRate[self.nB][self.channel]=bkgdNorms[self.nB][self.channel]['qcd']/self.qcd.Integral(0,self.nBins+1)
                    self.ewk.Scale(bkgdNorms[self.nB][self.channel]['ewk']/self.ewk.Integral(0,self.nBins+1)) #this is only done to show results of fit
                    self.top.Scale(bkgdNorms[self.nB][self.channel]['top']/self.top.Integral(0,self.nBins+1)) #this is only done to show results of fit
            self.qcd.Scale(fakeRate[self.nB][self.channel])

            #Scheme Choice
            #Scheme B
            #if self.nB=='2p': self.qcd.Scale(fakeRate['1p'][self.channel])
            #else: self.qcd.Scale(fakeRate[self.nB][self.channel])
            #Scheme C
            self.qcd.Scale(fakeRate['0p'][self.channel])
                        
        self.backgroundStack.Add(self.qcd)
        self.backgroundStack.Add(self.ewk)
        self.backgroundStack.Add(self.top)

        self.background=self.backgroundStack.GetStack().Last().Clone(self.name+'_background')
        result['Total Background']=self.background.Integral(0,self.nBins+1)
        result['Data']=self.data.Integral(0,self.nBins+1)
        result['QCD']=self.qcd.Integral(0,self.nBins+1)

        return result


    def Draw(self):

        self.canvas=TCanvas(self.name,"",1000,800)

        yDiv=0.35
        self.uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
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
        self.data.GetYaxis().CenterTitle()
        self.data.GetXaxis().SetLabelSize(0)
        self.data.GetYaxis().SetLabelSize(0.08)
        self.data.GetYaxis().SetTitleSize(0.12)
        self.data.GetYaxis().SetTitleOffset(.75)
                
        if self.yLog:
            self.uPad.SetLogy()
            self.data.SetMaximum(500*self.data.GetMaximum())

        binWidth=round(self.data.GetBinWidth(1),5)
        if binWidth-round(binWidth)<.001*binWidth: binWidth=int(round(binWidth))
        yTitle="Events / "+str(binWidth)
        if '[' in self.xTitle and ']' in self.xTitle: #get units from x axis title
            begin=self.xTitle.find('[')+1
            end=self.xTitle.find(']')
            yTitle+=' '+self.xTitle[begin:end]
        self.data.GetYaxis().SetTitle(yTitle)

        self.uPad.cd()
        self.data.Draw("E1") #draw data first because its easier to format a TH1 than a THStack
        self.backgroundStack.Draw("SAME HIST")
        for signal in self.signals: signal.Draw("SAME HIST")
        self.data.Draw("SAME E1") #redraw data so its not hidden
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
        gStyle.SetHatchesLineWidth(1)
        self.uncBand.Draw("SAME E2")
        
        legend=TLegend(0.60,0.60,0.90,0.90)
        legend.SetShadowColor(0);
        legend.SetFillColor(0);
        legend.SetLineColor(0);
        legend.AddEntry(self.data,"Data")
        legend.AddEntry(self.top,"t#bar{t} + Single-Top", "f")
        legend.AddEntry(self.ewk,"W#rightarrowl#nu + Z/#gamma*#rightarrowl^{+}l^{-} + VV" , "f")
        legend.AddEntry(self.qcd,"QCD","f")
        for signal in self.signals:
            name=signal.GetName()
            begin=name.find("Wprime")+6
            end=name.find("Right")-2
            dot=end-1
            mass=name[begin:dot]+'.'+name[dot:end]
            legend.AddEntry(signal, "W'_{R} x 20, m="+mass+" TeV", "l")
        legend.AddEntry(self.uncBand , "Uncertainty" , "f")
        legend.Draw("SAME")
        
        prelimTex=TLatex()
        prelimTex.SetNDC()
        prelimTex.SetTextSize(0.04)
        prelimTex.SetTextAlign(31) # align right
        if self.channel=='el': lumi=elLumi
        elif self.channel=='mu': lumi=muLumi
        lumi/=1000.
        lumi=round(lumi,2)
        prelimTex.DrawLatex(0.87, 0.95, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");

        if self.nB=="0":
            bTagLabel="N_{b tags} = 0"
        elif self.nB=="0p":
            bTagLabel="N_{b tags} #geq 0"
        elif self.nB=="1":
            bTagLabel="N_{b tags} = 1"
        elif self.nB=="1p":
            bTagLabel="N_{b tags} #geq 1"
        elif self.nB=="2":
            bTagLabel="N_{b tags} = 2"
        elif self.nB=="2p":
            bTagLabel="N_{b tags} #geq 2"
        channelTex = TLatex()
        channelTex.SetNDC()
        channelTex.SetTextSize(0.08)
        channelTex.SetTextAlign(31) # align right
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
        self.pull.GetXaxis().SetLabelSize(.15)
        self.pull.GetXaxis().SetTitleSize(0.18)
        self.pull.GetXaxis().SetTitle(self.xTitle)
        self.pull.GetXaxis().SetTitleOffset(.95) #1.15
        self.pull.GetYaxis().SetLabelSize(0.125)
        self.pull.GetYaxis().SetTitleSize(0.1)
        self.pull.GetYaxis().SetTitle('#sigma(Data-MC)')
        self.pull.GetYaxis().SetTitleOffset(.35)
        self.pull.GetYaxis().SetNdivisions(5);
        self.pull.Draw("HIST")

        output.cd()
        self.canvas.Write()
        self.data.Write()
        self.qcd.Write()
        self.ewk.Write()
        self.top.Write()
        self.canvas.SaveAs(inputDir+'/'+self.name+'.pdf')
        #self.canvas.SaveAs(inputDir+'/'+self.name+'.eps')
        #self.canvas.SaveAs(inputDir+'/'+self.name+'.C')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    #does the QCD fit
    def getNorms(self):
        data=self.data.Clone("data")
        backgrounds=TObjArray(3)
        backgrounds.Add(self.qcd.Clone(self.name+'_qcd_fitRes'))
        backgrounds.Add(self.ewk.Clone(self.name+'_ewk_fitRes'))
        backgrounds.Add(self.top.Clone(self.name+'_top_fitRes'))

        self.fitter=TFractionFitter(data,backgrounds)
        for binNo in range(self.nBins+2):
            for hist in [data,backgrounds[0],backgrounds[1],backgrounds[2]]:
                if hist.GetBinContent(binNo)<5: self.fitter.ExcludeBin(binNo) #can't have bins with very small content included in fit

        status=self.fitter.Fit()
        
        result={}
        if status==0:
            value=Double()
            error=Double()

            fitChi2[self.nB][self.channel]=self.fitter.GetChisquare()
            fitNDF[self.nB][self.channel]=self.fitter.GetNDF()
            
            self.fitter.GetResult(0,value,error)
            result['qcd']=value*data.Integral(0,self.nBins+1)
            QCDFrac[self.nB][self.channel]=value
            QCDFracUnc[self.nB][self.channel]=error
            
            self.fitter.GetResult(1,value,error)
            result['ewk']=value*data.Integral(0,self.nBins+1)
            self.fitter.GetResult(2,value,error)
            result['top']=value*data.Integral(0,self.nBins+1)
            
        return result
    
                                
##################################################################################################################################################################
                                    
if __name__=='__main__':

    yields={}
    plots=[]
    for n in bJetRequirements:
        yields[n]={}

        if doFracFit:
            plots+=[#WPrimePlot(name='corr_met_fitRes',distribution='corr_met_WprimeCalc',nBins=250,xMin=0,xMax=1000,xTitle='E_{T}^{miss} [GeV]',yLog=True,nB=n,channel='el'),
                    WPrimePlot(name='electron0_RelIso_fitRes',distribution='elec_1_RelIso_WprimeCalc',nBins=90,xMin=0,xMax=0.15,xTitle='electron Rel. Isolation',yLog=True,nB=n,channel='el'),
                    #WPrimePlot(name='corr_met_fitRes',distribution='corr_met_WprimeCalc',nBins=250,xMin=0,xMax=1000,xTitle='E_{T}^{miss} [GeV]',yLog=True,nB=n,channel='mu'),
                    #WPrimePlot(name='muon0_RelIso_fitRes',distribution='muon_1_RelIso_WprimeCalc',nBins=250,xMin=0,xMax=0.15,xTitle='muon Rel. Isolation',yLog=True,nB=n,channel='mu')
                    ]
            
        if doCutTable:
            plots+=[WPrimePlot(name='electron0_pt',distribution='elec_1_pt_WprimeCalc',nBins=100,xMin=0,xMax=7000,xTitle='electron p_{T} [GeV]',yLog=True,nB=n,channel='el'),
                    WPrimePlot(name='muon0_pt',distribution='muon_1_pt_WprimeCalc',nBins=100,xMin=0,xMax=7000,xTitle='muon p_{T} [GeV]',yLog=True,nB=n,channel='mu')
                    ]

        else:
            plots+=[WPrimePlot(name='electron0_pt',distribution='elec_1_pt_WprimeCalc',nBins=100,xMin=0,xMax=1000,xTitle='electron p_{T} [GeV]',yLog=True,nB=n,channel='el'),
                    WPrimePlot(name='electron0_eta',distribution='elec_1_eta_WprimeCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='electron #eta',yLog=False,nB=n,channel='el'),
                    WPrimePlot(name='electron0_RelIso',distribution='elec_1_RelIso_WprimeCalc',nBins=30,xMin=0,xMax=0.15,xTitle='electron Rel. Isolation',yLog=True,nB=n,channel='el'),
                    
                    #WPrimePlot(name='muon0_pt',distribution='muon_1_pt_WprimeCalc',nBins=100,xMin=0,xMax=1000,xTitle='muon p_{T} [GeV]',yLog=True,nB=n,channel='mu'),
                    #WPrimePlot(name='muon0_eta',distribution='muon_1_eta_WprimeCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='muon #eta',yLog=False,nB=n,channel='mu'),
                    #WPrimePlot(name='muon0_RelIso',distribution='muon_1_RelIso_WprimeCalc',nBins=30,xMin=0,xMax=0.15,xTitle='muon Rel. Isolation',yLog=True,nB=n,channel='mu')
                    ]
            for c in channels:
                plots+=[WPrimePlot(name='BestJetJet2W_M',distribution='BestJetJet2W_M_LjetsTopoCalcNew',nBins=68,xMin=100,xMax=3500,xTitle='M(tb) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='Jet1Jet2W_M',distribution='Jet1Jet2W_M_LjetsTopoCalcNew',nBins=68,xMin=100,xMax=3500,xTitle='M(tb) [GeV]',yLog=True,nB=n,channel=c),
                        WPrimePlot(name='corr_met',distribution='corr_met_WprimeCalc',nBins=100,xMin=0,xMax=1000,xTitle='E_{T}^{miss} [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='PFjet0_pt',distribution='jet_0_pt_WprimeCalc',nBins=130,xMin=0,xMax=1300,xTitle='p_{T} (jet1) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='PFjet0_eta',distribution='jet_0_eta_WprimeCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet1)',yLog=False,nB=n,channel=c),
                        #WPrimePlot(name='PFjet1_pt',distribution='jet_1_pt_WprimeCalc',nBins=120,xMin=0,xMax=1200,xTitle='p_{T} (jet2) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='PFjet1_eta',distribution='jet_1_eta_WprimeCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet2)',yLog=False,nB=n,channel=c),
                        #WPrimePlot(name='PFjet2_pt',distribution='jet_2_pt_WprimeCalc',nBins=80,xMin=0,xMax=800,xTitle='p_{T} (jet3) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='PFjet2_eta',distribution='jet_2_eta_WprimeCalc',nBins=50,xMin=-2.5,xMax=2.5,xTitle='#eta (jet3)',yLog=False,nB=n,channel=c),
                        WPrimePlot(name='TopMass_Best',distribution='BestTop_LjetsTopoCalcNew',nBins=100,xMin=0,xMax=1000,xTitle='M(best jet,W) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='TopPt_Best',distribution='BestTop_Pt_LjetsTopoCalcNew',nBins=150,xMin=0,xMax=1500,xTitle='p_{T}(best jet,W) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='Pt_Jet1Jet2',distribution='Jet1Jet2_Pt_LjetsTopoCalcNew',nBins=150,xMin=0,xMax=1500,xTitle='p_{T}(jet1,jet2) [GeV]',yLog=True,nB=n,channel=c),
                        #WPrimePlot(name='HT',distribution='Ht_LjetsTopoCalcNew',nBins=125,xMin=0,xMax=2500,xTitle='H_{T} [GeV]',yLog=True,nB=n,channel=c),
                        WPrimePlot(name='nPV',distribution='nPV_WprimeCalc',nBins=50,xMin=0,xMax=50,xTitle='# Vertices',yLog=True,nB=n,channel=c)
                        ]
                
    for plot in plots:
        yields[plot.nB][plot.channel]=plot.Prepare()
        plot.Draw()

    cWidth=15; nameWidth=35
    for c in channels:
        print ("CHANNEL:"+c).ljust(nameWidth+(2*cWidth+1)),"N_b"
        print "".ljust(nameWidth),
        for n in bJetRequirements: print n.ljust(cWidth),
        print
        for sample in ['Data','QCD']: #,'W+light','W+c','W+b']:
            print sample.ljust(nameWidth),
            for n in bJetRequirements:
                try: print str(int(round(yields[n][c][sample]))).ljust(cWidth),
                except: pass
            print
        for sample in samples:
            if (c=='el' and 'SingleMu' in sample.name) or (c=='mu' and 'SingleEl' in sample.name) or 'QCD_' in sample.name: continue
            if sample.isData: continue
            print sample.name.ljust(nameWidth),
            for n in bJetRequirements:
                print str(int(round(yields[n][c][sample.name]))).ljust(cWidth),
            print
        for sample in ['Total Background']:
            print sample.ljust(nameWidth),
            for n in bJetRequirements:
                print str(int(round(yields[n][c][sample]))).ljust(cWidth),
            print
        print 'Background/Data'.ljust(nameWidth),
        for n in bJetRequirements:
            print str(round(yields[n][c]['Total Background']/yields[n][c]['Data'],3)).ljust(cWidth),
        print 3*'\n'
        
if doFracFit:
    for c in channels:
        print 'CHANNEL:',c
        for n in bJetRequirements:
            print 'nB:',n
            print 'QCDFrac =',QCDFrac[n][c]
            print 'QCDFracUnc =',QCDFracUnc[n][c]
            print "fake rate:",fakeRate[n][c]
            print '100*QCDFracUnc/QCDFrac =',100*QCDFracUnc[n][c]/QCDFrac[n][c]
            print 'chi2/nDF =',fitChi2[n][c]/fitNDF[n][c]
        print
