from ROOT import *
from math import pi

gStyle.SetOptStat(0)

dir="rawCrossSections"

sigma={}
BR={}

c=TCanvas()
#c.SetLogz()
c.SetBottomMargin(0.12)
c.SetRightMargin(0.15)

for type in ['T1','T2']:
    sigma[type]={}
    BR[type]={}
    for particle in ['A','H']:
        sigma[type][particle]={}
        BR[type][particle]={}
        for mass in range(200,600,50)+range(600,1000,100):
            mass=str(mass)

            for E in ['14']: #,'33']:

                sigmaFile=dir+'/'+'gg_'+particle+'_'+E+'TeV_'+type+'_'+mass+'.txt'
                h_sigma=TH2F("sigma",";cos( #beta - #alpha );#beta;#sigma [pb]", 61, -0.6-.01 ,0.6+.01 ,99 ,(pi/200)-(98*pi)/(400*99), (99*pi/200)+(98*pi)/(400*99))
                h_sigma.GetXaxis().SetTitleSize(0.07)
                h_sigma.GetYaxis().SetTitleSize(0.07)
                h_sigma.GetZaxis().SetTitleSize(0.07)
                h_sigma.GetXaxis().SetTitleOffset(0.75)
                h_sigma.GetYaxis().SetTitleOffset(0.45)
                h_sigma.GetZaxis().SetTitleOffset(0.65)

                min=9999999
                for line in open(sigmaFile):
                    cosBetaMinusAlpha=float(line.split()[0])
                    beta=float(line.split()[1])
                    s=float(line.split()[2])
                    h_sigma.Fill(cosBetaMinusAlpha,beta,s)

                h_sigma.Draw("COLZ")
                c.SaveAs(dir+'/'+'gg_'+particle+'_'+E+'TeV_'+type+'_'+mass+'.pdf')
                h_sigma.SaveAs()


                for finalState in ['ZZ','WW','Zh','hh']:

                    try:
                        BRFile=dir+'/'+'BR_'+particle+'_'+finalState+'_'+type+'_'+mass+'.txt'

                        h_BR=h_sigma.Clone("BR"); h_BR.Reset(); h_BR.SetTitle(";cos( #beta - #alpha );#beta;BR")
                        h_sigmaTimesBR=h_sigma.Clone("sigmaTimesBR"); h_sigmaTimesBR.Reset(); h_sigmaTimesBR.SetTitle(";cos( #beta - #alpha );#beta;#sigma #times BR [pb]")
                        
                        for line in open(BRFile):
                            cosBetaMinusAlpha=float(line.split()[0])
                            beta=float(line.split()[1])
                            br=float(line.split()[2])
                            h_BR.Fill(cosBetaMinusAlpha,beta,br)
                            if cosBetaMinusAlpha!=0 and br<min: min=br

                        if h_BR.Integral()>0:
                            #h_BR.SetMinimum(min/2)
                            h_BR.SetMinimum(0)
                            h_BR.SetMaximum(1)
                            h_BR.Draw("COLZ")
                            c.SaveAs(dir+'/'+'BR_'+particle+'_'+finalState+'_'+type+'_'+mass+'.pdf')
                            h_BR.SaveAs()

                            h_sigmaTimesBR.Multiply(h_sigma,h_BR,1,1)
                            min=999999999999
                            for xBin in range(1,h_sigmaTimesBR.GetNbinsX()+1):
                                for yBin in range(1,h_sigmaTimesBR.GetNbinsY()+1):
                                    if xBin!=31 and h_sigmaTimesBR.GetBinContent(xBin,yBin)<min: min=h_sigmaTimesBR.GetBinContent(xBin,yBin)
                            h_sigmaTimesBR.SetMinimum(min/2)
                            h_sigmaTimesBR.Draw("COLZ")
                            c.SaveAs(dir+'/'+'sigmaTimesBR_'+particle+'_'+E+'TeV_'+finalState+'_'+type+'_'+mass+'.pdf')
                            h_sigmaTimesBR.SaveAs()
                        
                    except IOError: pass
                    
