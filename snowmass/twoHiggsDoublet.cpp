bool verbose=false;

double electronPtMin=5;
double electronEtaMax=2.5;

double muonPtMin=5;
double muonEtaMax=2.5;

double tauPtMin=5;
double tauEtaMax=2.5;

double bJetPtMin=20;
double bJetEtaMax=2.5;

double jetPtMin=20;
double jetEtaMax=2.5;

double photonPtMin=20;
double photonEtaMax=2.5;

double ZMassMin_emu=60.;
double ZMassMax_emu=120.;
double ZMassMin_tau=76.;
double ZMassMax_tau=106.;

double hadronicWMassMin=55.;
double hadronicWMassMax=115.;
double muMax=0.4;

double higgsMassMin_b=96.;
double higgsMassMax_b=156.;
double higgsMassMin_tau=106.;
double higgsMassMax_tau=146.;
double higgsMassMin_Z=116.;
double higgsMassMax_Z=136.;
double higgsMassMin_W=96.;
double higgsMassMax_W=156.;
double higgsMassMin_photon=121.;
double higgsMassMax_photon=131.;

double HAMassMin=175.;
double HAMassMax=1200.;

//Pruning parameters
double zcut = 0.1;
double Dcut_factor = 0.5;

//Triggers
double singleLeptonTrigger_pTMin=30.;
double dileptonTrigger_pTMins[2]={20,10};

//------------------------------------------------------------------------------

#include "TH1.h"
#include "TH2.h"
#include "TChain.h"
#include "TClonesArray.h"
#include "TCanvas.h"
#include "TLegend.h"
#include <TROOT.h>
#include <TStyle.h>
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#include "external/ExRootAnalysis/ExRootTreeBranch.h"
#include "external/ExRootAnalysis/ExRootUtilities.h"
#include "classes/DelphesClasses.h"

#include "fastjet/PseudoJet.hh"
#include "fastjet/ClusterSequence.hh"
#include <fastjet/tools/JHTopTagger.hh>

#include <fastjet/Selector.hh>
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/Pruner.hh"

#include <iostream>
#include <sstream>
#include <iomanip>
#include <cmath>

using namespace fastjet;
using namespace std;

//------------------------------------------------------------------------------

//Output
TFile* output=new TFile("twoHiggsDoublet.root","RECREATE");
TTree* tree=new TTree("twoHiggsDoublet","");

double eventWeight;
TBranch* b_eventWeight=tree->Branch("eventWeight", &eventWeight,"eventWeight/D");

//Electrons
int nElectron;
double electron1_pT,electron2_pT,electron3_pT,electron4_pT;
double electron1_eta,electron2_eta,electron3_eta,electron4_eta;

TBranch* b_nElectron=tree->Branch("nElectron",&nElectron,"nElectron/I");
TBranch* b_electron1_pT=tree->Branch("electron1_pT", &electron1_pT,"electron1_pT/D");
TBranch* b_electron2_pT=tree->Branch("electron2_pT", &electron2_pT,"electron2_pT/D");
TBranch* b_electron3_pT=tree->Branch("electron3_pT", &electron3_pT,"electron3_pT/D");
TBranch* b_electron4_pT=tree->Branch("electron4_pT", &electron4_pT,"electron4_pT/D");
TBranch* b_electron1_eta=tree->Branch("electron1_eta", &electron1_eta,"electron1_eta/D");
TBranch* b_electron2_eta=tree->Branch("electron2_eta", &electron2_eta,"electron2_eta/D");
TBranch* b_electron3_eta=tree->Branch("electron3_eta", &electron3_eta,"electron3_eta/D");
TBranch* b_electron4_eta=tree->Branch("electron4_eta", &electron4_eta,"electron4_eta/D");

//Muons
int nMuon;
double muon1_pT,muon2_pT,muon3_pT,muon4_pT;
double muon1_eta,muon2_eta,muon3_eta,muon4_eta;

TBranch* b_nMuon=tree->Branch("nMuon",&nMuon,"nMuon/I");
TBranch* b_muon1_pT=tree->Branch("muon1_pT", &muon1_pT,"muon1_pT/D");
TBranch* b_muon2_pT=tree->Branch("muon2_pT", &muon2_pT,"muon2_pT/D");
TBranch* b_muon3_pT=tree->Branch("muon3_pT", &muon3_pT,"muon3_pT/D");
TBranch* b_muon4_pT=tree->Branch("muon4_pT", &muon4_pT,"muon4_pT/D");
TBranch* b_muon1_eta=tree->Branch("muon1_eta", &muon1_eta,"muon1_eta/D");
TBranch* b_muon2_eta=tree->Branch("muon2_eta", &muon2_eta,"muon2_eta/D");
TBranch* b_muon3_eta=tree->Branch("muon3_eta", &muon3_eta,"muon3_eta/D");
TBranch* b_muon4_eta=tree->Branch("muon4_eta", &muon4_eta,"muon4_eta/D");

//Leptons
int nLepton;
double lepton1_pT,lepton2_pT,lepton3_pT,lepton4_pT;
double lepton1_eta,lepton2_eta,lepton3_eta,lepton4_eta;

TBranch* b_nLepton=tree->Branch("nLepton",&nLepton,"nLepton/I");
TBranch* b_lepton1_pT=tree->Branch("lepton1_pT", &lepton1_pT,"lepton1_pT/D");
TBranch* b_lepton2_pT=tree->Branch("lepton2_pT", &lepton2_pT,"lepton2_pT/D");
TBranch* b_lepton3_pT=tree->Branch("lepton3_pT", &lepton3_pT,"lepton3_pT/D");
TBranch* b_lepton4_pT=tree->Branch("lepton4_pT", &lepton4_pT,"lepton4_pT/D");
TBranch* b_lepton1_eta=tree->Branch("lepton1_eta", &lepton1_eta,"lepton1_eta/D");
TBranch* b_lepton2_eta=tree->Branch("lepton2_eta", &lepton2_eta,"lepton2_eta/D");
TBranch* b_lepton3_eta=tree->Branch("lepton3_eta", &lepton3_eta,"lepton3_eta/D");
TBranch* b_lepton4_eta=tree->Branch("lepton4_eta", &lepton4_eta,"lepton4_eta/D");



//Taus
int nTau;
double tau1_pT,tau2_pT,tau3_pT,tau4_pT;
double tau1_eta,tau2_eta,tau3_eta,tau4_eta;

TBranch* b_nTau=tree->Branch("nTau",&nTau,"nTau/I");
TBranch* b_tau1_pT=tree->Branch("tau1_pT", &tau1_pT,"tau1_pT/D");
TBranch* b_tau2_pT=tree->Branch("tau2_pT", &tau2_pT,"tau2_pT/D");
TBranch* b_tau3_pT=tree->Branch("tau3_pT", &tau3_pT,"tau3_pT/D");
TBranch* b_tau4_pT=tree->Branch("tau4_pT", &tau4_pT,"tau4_pT/D");
TBranch* b_tau1_eta=tree->Branch("tau1_eta", &tau1_eta,"tau1_eta/D");
TBranch* b_tau2_eta=tree->Branch("tau2_eta", &tau2_eta,"tau2_eta/D");
TBranch* b_tau3_eta=tree->Branch("tau3_eta", &tau3_eta,"tau3_eta/D");
TBranch* b_tau4_eta=tree->Branch("tau4_eta", &tau4_eta,"tau4_eta/D");

int nJet;
double jet1_pT,jet2_pT,jet3_pT,jet4_pT,jet5_pT,jet6_pT,jet7_pT,jet8_pT;
double jet1_eta,jet2_eta,jet3_eta,jet4_eta,jet5_eta,jet6_eta,jet7_eta,jet8_eta;

TBranch* b_nJet=tree->Branch("nJet",&nJet,"nJet/I");
TBranch* b_jet1_pT=tree->Branch("jet1_pT", &jet1_pT,"jet1_pT/D");
TBranch* b_jet2_pT=tree->Branch("jet2_pT", &jet2_pT,"jet2_pT/D");
TBranch* b_jet3_pT=tree->Branch("jet3_pT", &jet3_pT,"jet3_pT/D");
TBranch* b_jet4_pT=tree->Branch("jet4_pT", &jet4_pT,"jet4_pT/D");
TBranch* b_jet5_pT=tree->Branch("jet5_pT", &jet5_pT,"jet5_pT/D");
TBranch* b_jet6_pT=tree->Branch("jet6_pT", &jet6_pT,"jet6_pT/D");
TBranch* b_jet7_pT=tree->Branch("jet7_pT", &jet7_pT,"jet7_pT/D");
TBranch* b_jet8_pT=tree->Branch("jet8_pT", &jet8_pT,"jet8_pT/D");
TBranch* b_jet1_eta=tree->Branch("jet1_eta", &jet1_eta,"jet1_eta/D");
TBranch* b_jet2_eta=tree->Branch("jet2_eta", &jet2_eta,"jet2_eta/D");
TBranch* b_jet3_eta=tree->Branch("jet3_eta", &jet3_eta,"jet3_eta/D");
TBranch* b_jet4_eta=tree->Branch("jet4_eta", &jet4_eta,"jet4_eta/D");
TBranch* b_jet5_eta=tree->Branch("jet5_eta", &jet5_eta,"jet5_eta/D");
TBranch* b_jet6_eta=tree->Branch("jet6_eta", &jet6_eta,"jet6_eta/D");
TBranch* b_jet7_eta=tree->Branch("jet7_eta", &jet7_eta,"jet7_eta/D");
TBranch* b_jet8_eta=tree->Branch("jet8_eta", &jet8_eta,"jet8_eta/D");
  
//b-Jets
int nBJet;
double bJet1_pT,bJet2_pT,bJet3_pT,bJet4_pT;
double bJet1_eta,bJet2_eta,bJet3_eta,bJet4_eta;

TBranch* b_nBJet=tree->Branch("nBJet",&nBJet,"nBJet/I");
TBranch* b_bJet1_pT=tree->Branch("bJet1_pT", &bJet1_pT,"bJet1_pT/D");
TBranch* b_bJet2_pT=tree->Branch("bJet2_pT", &bJet2_pT,"bJet2_pT/D");
TBranch* b_bJet3_pT=tree->Branch("bJet3_pT", &bJet3_pT,"bJet3_pT/D");
TBranch* b_bJet4_pT=tree->Branch("bJet4_pT", &bJet4_pT,"bJet4_pT/D");
TBranch* b_bJet1_eta=tree->Branch("bJet1_eta", &bJet1_eta,"bJet1_eta/D");
TBranch* b_bJet2_eta=tree->Branch("bJet2_eta", &bJet2_eta,"bJet2_eta/D");
TBranch* b_bJet3_eta=tree->Branch("bJet3_eta", &bJet3_eta,"bJet3_eta/D");
TBranch* b_bJet4_eta=tree->Branch("bJet4_eta", &bJet4_eta,"bJet4_eta/D");

//Photons
int nPhoton;
double photon1_pT,photon2_pT,photon3_pT,photon4_pT;
double photon1_eta,photon2_eta,photon3_eta,photon4_eta;

TBranch* b_nPhoton=tree->Branch("nPhoton",&nPhoton,"nPhoton/I");
TBranch* b_photon1_pT=tree->Branch("photon1_pT", &photon1_pT,"photon1_pT/D");
TBranch* b_photon2_pT=tree->Branch("photon2_pT", &photon2_pT,"photon2_pT/D");
TBranch* b_photon3_pT=tree->Branch("photon3_pT", &photon3_pT,"photon3_pT/D");
TBranch* b_photon4_pT=tree->Branch("photon4_pT", &photon4_pT,"photon4_pT/D");
TBranch* b_photon1_eta=tree->Branch("photon1_eta", &photon1_eta,"photon1_eta/D");
TBranch* b_photon2_eta=tree->Branch("photon2_eta", &photon2_eta,"photon2_eta/D");
TBranch* b_photon3_eta=tree->Branch("photon3_eta", &photon3_eta,"photon3_eta/D");
TBranch* b_photon4_eta=tree->Branch("photon4_eta", &photon4_eta,"photon4_eta/D");

//Zs
int nZ;
double Z1_pT,Z2_pT,Z3_pT,Z4_pT;
double Z1_eta,Z2_eta,Z3_eta,Z4_eta;
double Z1_mass,Z2_mass,Z3_mass,Z4_mass;
double Z1_daughter1_pT,Z1_daughter2_pT,Z2_daughter1_pT,Z2_daughter2_pT,Z3_daughter1_pT,Z3_daughter2_pT,Z4_daughter1_pT,Z4_daughter2_pT;

TBranch* b_nZ=tree->Branch("nZ",&nZ,"nZ/I");
TBranch* b_Z1_pT=tree->Branch("Z1_pT", &Z1_pT,"Z1_pT/D");
TBranch* b_Z2_pT=tree->Branch("Z2_pT", &Z2_pT,"Z2_pT/D");
TBranch* b_Z3_pT=tree->Branch("Z3_pT", &Z3_pT,"Z3_pT/D");
TBranch* b_Z4_pT=tree->Branch("Z4_pT", &Z4_pT,"Z4_pT/D");
TBranch* b_Z1_eta=tree->Branch("Z1_eta", &Z1_eta,"Z1_eta/D");
TBranch* b_Z2_eta=tree->Branch("Z2_eta", &Z2_eta,"Z2_eta/D");
TBranch* b_Z3_eta=tree->Branch("Z3_eta", &Z3_eta,"Z3_eta/D");
TBranch* b_Z4_eta=tree->Branch("Z4_eta", &Z4_eta,"Z4_eta/D");
TBranch* b_Z1_mass=tree->Branch("Z1_mass", &Z1_mass,"Z1_mass/D");
TBranch* b_Z2_mass=tree->Branch("Z2_mass", &Z2_mass,"Z2_mass/D");
TBranch* b_Z3_mass=tree->Branch("Z3_mass", &Z3_mass,"Z3_mass/D");
TBranch* b_Z4_mass=tree->Branch("Z4_mass", &Z4_mass,"Z4_mass/D");
TBranch* b_Z1_daughter1_pT=tree->Branch("Z1_daughter1_pT", &Z1_daughter1_pT,"Z1_daughter1_pT/D");
TBranch* b_Z1_daughter2_pT=tree->Branch("Z1_daughter2_pT", &Z1_daughter2_pT,"Z1_daughter2_pT/D");
TBranch* b_Z2_daughter1_pT=tree->Branch("Z2_daughter1_pT", &Z2_daughter1_pT,"Z2_daughter1_pT/D");
TBranch* b_Z2_daughter2_pT=tree->Branch("Z2_daughter2_pT", &Z2_daughter2_pT,"Z2_daughter2_pT/D");
TBranch* b_Z3_daughter1_pT=tree->Branch("Z3_daughter1_pT", &Z3_daughter1_pT,"Z3_daughter1_pT/D");
TBranch* b_Z3_daughter2_pT=tree->Branch("Z3_daughter2_pT", &Z3_daughter2_pT,"Z3_daughter2_pT/D");
TBranch* b_Z4_daughter1_pT=tree->Branch("Z4_daughter1_pT", &Z4_daughter1_pT,"Z4_daughter1_pT/D");
TBranch* b_Z4_daughter2_pT=tree->Branch("Z4_daughter2_pT", &Z4_daughter2_pT,"Z4_daughter2_pT/D");

//Ws
int nW;
double W1_pT,W2_pT,W3_pT,W4_pT;
double W1_eta,W2_eta,W3_eta,W4_eta;
double W1_mass,W2_mass,W3_mass,W4_mass;

TBranch* b_nW=tree->Branch("nW",&nW,"nW/I");
TBranch* b_W1_pT=tree->Branch("W1_pT", &W1_pT,"W1_pT/D");
TBranch* b_W2_pT=tree->Branch("W2_pT", &W2_pT,"W2_pT/D");
TBranch* b_W3_pT=tree->Branch("W3_pT", &W3_pT,"W3_pT/D");
TBranch* b_W4_pT=tree->Branch("W4_pT", &W4_pT,"W4_pT/D");
TBranch* b_W1_eta=tree->Branch("W1_eta", &W1_eta,"W1_eta/D");
TBranch* b_W2_eta=tree->Branch("W2_eta", &W2_eta,"W2_eta/D");
TBranch* b_W3_eta=tree->Branch("W3_eta", &W3_eta,"W3_eta/D");
TBranch* b_W4_eta=tree->Branch("W4_eta", &W4_eta,"W4_eta/D");
TBranch* b_W1_mass=tree->Branch("W1_mass", &W1_mass,"W1_mass/D");
TBranch* b_W2_mass=tree->Branch("W2_mass", &W2_mass,"W2_mass/D");
TBranch* b_W3_mass=tree->Branch("W3_mass", &W3_mass,"W3_mass/D");
TBranch* b_W4_mass=tree->Branch("W4_mass", &W4_mass,"W4_mass/D");

//h's
int nh;
double h1_pT,h2_pT,h3_pT,h4_pT;
double h1_eta,h2_eta,h3_eta,h4_eta;
double h1_mass,h2_mass,h3_mass,h4_mass;

TBranch* b_nh=tree->Branch("nh",&nh,"nh/I");
TBranch* b_h1_pT=tree->Branch("h1_pT", &h1_pT,"h1_pT/D");
TBranch* b_h2_pT=tree->Branch("h2_pT", &h2_pT,"h2_pT/D");
TBranch* b_h3_pT=tree->Branch("h3_pT", &h3_pT,"h3_pT/D");
TBranch* b_h4_pT=tree->Branch("h4_pT", &h4_pT,"h4_pT/D");
TBranch* b_h1_eta=tree->Branch("h1_eta", &h1_eta,"h1_eta/D");
TBranch* b_h2_eta=tree->Branch("h2_eta", &h2_eta,"h2_eta/D");
TBranch* b_h3_eta=tree->Branch("h3_eta", &h3_eta,"h3_eta/D");
TBranch* b_h4_eta=tree->Branch("h4_eta", &h4_eta,"h4_eta/D");
TBranch* b_h1_mass=tree->Branch("h1_mass", &h1_mass,"h1_mass/D");
TBranch* b_h2_mass=tree->Branch("h2_mass", &h2_mass,"h2_mass/D");
TBranch* b_h3_mass=tree->Branch("h3_mass", &h3_mass,"h3_mass/D");
TBranch* b_h4_mass=tree->Branch("h4_mass", &h4_mass,"h4_mass/D");

//H's
int nH;
double H1_pT,H2_pT,H3_pT,H4_pT;
double H1_eta,H2_eta,H3_eta,H4_eta;
double H1_mass,H2_mass,H3_mass,H4_mass;

TBranch* b_nH=tree->Branch("nH",&nH,"nH/I");
TBranch* b_H1_pT=tree->Branch("H1_pT", &H1_pT,"H1_pT/D");
TBranch* b_H2_pT=tree->Branch("H2_pT", &H2_pT,"H2_pT/D");
TBranch* b_H3_pT=tree->Branch("H3_pT", &H3_pT,"H3_pT/D");
TBranch* b_H4_pT=tree->Branch("H4_pT", &H4_pT,"H4_pT/D");
TBranch* b_H1_eta=tree->Branch("H1_eta", &H1_eta,"H1_eta/D");
TBranch* b_H2_eta=tree->Branch("H2_eta", &H2_eta,"H2_eta/D");
TBranch* b_H3_eta=tree->Branch("H3_eta", &H3_eta,"H3_eta/D");
TBranch* b_H4_eta=tree->Branch("H4_eta", &H4_eta,"H4_eta/D");
TBranch* b_H1_mass=tree->Branch("H1_mass", &H1_mass,"H1_mass/D");
TBranch* b_H2_mass=tree->Branch("H2_mass", &H2_mass,"H2_mass/D");
TBranch* b_H3_mass=tree->Branch("H3_mass", &H3_mass,"H3_mass/D");
TBranch* b_H4_mass=tree->Branch("H4_mass", &H4_mass,"H4_mass/D");

//A's
int nA;
double A1_pT,A2_pT,A3_pT,A4_pT;
double A1_eta,A2_eta,A3_eta,A4_eta;
double A1_mass,A2_mass,A3_mass,A4_mass;

TBranch* b_nA=tree->Branch("nA",&nA,"nA/I");
TBranch* b_A1_pT=tree->Branch("A1_pT", &A1_pT,"A1_pT/D");
TBranch* b_A2_pT=tree->Branch("A2_pT", &A2_pT,"A2_pT/D");
TBranch* b_A3_pT=tree->Branch("A3_pT", &A3_pT,"A3_pT/D");
TBranch* b_A4_pT=tree->Branch("A4_pT", &A4_pT,"A4_pT/D");
TBranch* b_A1_eta=tree->Branch("A1_eta", &A1_eta,"A1_eta/D");
TBranch* b_A2_eta=tree->Branch("A2_eta", &A2_eta,"A2_eta/D");
TBranch* b_A3_eta=tree->Branch("A3_eta", &A3_eta,"A3_eta/D");
TBranch* b_A4_eta=tree->Branch("A4_eta", &A4_eta,"A4_eta/D");
TBranch* b_A1_mass=tree->Branch("A1_mass", &A1_mass,"A1_mass/D");
TBranch* b_A2_mass=tree->Branch("A2_mass", &A2_mass,"A2_mass/D");
TBranch* b_A3_mass=tree->Branch("A3_mass", &A3_mass,"A3_mass/D");
TBranch* b_A4_mass=tree->Branch("A4_mass", &A4_mass,"A4_mass/D");

double MET, ST, HT;
TBranch* b_MET=tree->Branch("MET",&MET,"MET/D");
TBranch* b_ST=tree->Branch("ST",&ST,"ST/D");
TBranch* b_HT=tree->Branch("HT",&HT,"HT/D");

int passSingleLeptonTrigger,passDiLeptonTrigger;
TBranch* b_passSingleLeptonTrigger=tree->Branch("passSingleLeptonTrigger",&passSingleLeptonTrigger,"passSingleLeptonTrigger/I");
TBranch* b_passDiLeptonTrigger=tree->Branch("passDiLeptonTrigger",&passDiLeptonTrigger,"passDiLeptonTrigger/I");

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

class Particle{
public:
 
  Particle(): P4(0),daughters(0),mother(0),charge(0) {};
  Particle(TLorentzVector* tlv): daughters(0),mother(0),charge(0) {
    P4=(TLorentzVector*)tlv->Clone();
  };
  Particle(TLorentzVector tlv): daughters(0),mother(0),charge(0) {
    P4=new TLorentzVector(tlv);
  };
  Particle(TLorentzVector* tlv, int q): daughters(0),mother(0),charge(q) {
    P4=(TLorentzVector*)tlv->Clone();
  };
  Particle(TLorentzVector tlv,int q): daughters(0),mother(0),charge(q) {
    P4=new TLorentzVector(tlv);
  };


  TLorentzVector* P4;

  std::vector<Particle*> daughters;
  Particle* mother;
  
  int charge;
};

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

bool closerToZMass(Particle part1, Particle part2){
  double ZMass=91.1876;

  return ( fabs(part1.P4->M()-ZMass) <= fabs(part2.P4->M()-ZMass) );
}

//==============================================================================

bool largerPt(Particle part1, Particle part2){
  return ( part1.P4->Pt() >= part2.P4->Pt() );
}

//==============================================================================

bool smallerPt(Particle part1, Particle part2){
  return ( part1.P4->Pt() < part2.P4->Pt() );
}

bool smallerPt_p(Particle* part1, Particle* part2){
  return ( part1->P4->Pt() < part2->P4->Pt() );
}

//==============================================================================

std::vector<Particle> getMothers(std::vector<Particle> &daughters, double minMass, double maxMass, bool OS=true){
  if(verbose) cout<<"Inside getMothers"<<endl;
  std::vector<Particle> result;

  Particle daughter1, daughter2, motherCand;
  bool used[daughters.size()];  for(int daughterNo=0; daughterNo<daughters.size(); daughterNo++) used[daughterNo]=false;

  for(int daughter1No=0; daughter1No<daughters.size(); daughter1No++){
    if(!used[daughter1No]){
      daughter1=daughters[daughter1No];
      for(int daughter2No=0; daughter2No<daughters.size(); daughter2No++){
        if(!used[daughter2No]){
          if(daughter1No!=daughter2No){
	    if(!OS || daughter1.charge!=daughter2.charge){
	      daughter2=daughters[daughter2No];
	      
	      if(verbose) cout<<"Messing with motherCand"<<endl;
	      motherCand.P4=new TLorentzVector((*daughter1.P4)+(*daughter2.P4));
	      if(motherCand.P4->M()>minMass && motherCand.P4->M()<maxMass){
		motherCand.daughters.push_back(new Particle(daughter1.P4));
		motherCand.daughters.push_back(new Particle(daughter2.P4));
		std::sort(motherCand.daughters.begin(),motherCand.daughters.end(),smallerPt_p);
		result.push_back(motherCand);
		used[daughter1No]=true;
		used[daughter2No]=true;
	      }
            }
          }
        }
      }
    }
  }
  for(int daughterNo=0; daughterNo<daughters.size(); daughterNo++){
    if(used[daughterNo]) daughters.erase(daughters.begin()+daughterNo);
  }

  if(verbose) cout<<"Leaving getMothers"<<endl;
  return result;
}

//==============================================================================

void resetBranches(){

  nElectron=0;
  electron1_pT=-99; electron2_pT=-99; electron3_pT=-99; electron4_pT=-99;
  electron1_eta=-99; electron2_eta=-99; electron3_eta=-99; electron4_eta=-99;

  nMuon=0;
  muon1_pT=-99; muon2_pT=-99; muon3_pT=-99; muon4_pT=-99;
  muon1_eta=-99; muon2_eta=-99; muon3_eta=-99; muon4_eta=-99;

  nLepton=0;
  lepton1_pT=-99; lepton2_pT=-99; lepton3_pT=-99; lepton4_pT=-99;
  lepton1_eta=-99; lepton2_eta=-99; lepton3_eta=-99; lepton4_eta=-99;

  nTau=0;
  tau1_pT=-99; tau2_pT=-99; tau3_pT=-99; tau4_pT=-99;
  tau1_eta=-99; tau2_eta=-99; tau3_eta=-99; tau4_eta=-99;

  nJet=0;
  jet1_pT=-99; jet2_pT=-99; jet3_pT=-99; jet4_pT=-99; jet5_pT=-99; jet6_pT=-99; jet7_pT=-99; jet8_pT=-99;
  jet1_eta=-99; jet2_eta=-99; jet3_eta=-99; jet4_eta=-99; jet5_eta=-99; jet6_eta=-99; jet7_eta=-99; jet8_eta=-99;

  nBJet=0;
  bJet1_pT=-99; bJet2_pT=-99; bJet3_pT=-99; bJet4_pT=-99;
  bJet1_eta=-99; bJet2_eta=-99; bJet3_eta=-99; bJet4_eta=-99;

  nPhoton=0;
  photon1_pT=-99; photon2_pT=-99; photon3_pT=-99; photon4_pT=-99;
  photon1_eta=-99; photon2_eta=-99; photon3_eta=-99; photon4_eta=-99;

  nZ=0;
  Z1_pT=-99; Z2_pT=-99; Z3_pT=-99; Z4_pT=-99;
  Z1_eta=-99; Z2_eta=-99; Z3_eta=-99; Z4_eta=-99;
  Z1_mass=-99; Z2_mass=-99; Z3_mass=-99; Z4_mass=-99;

  nW=0;
  W1_pT=-99; W2_pT=-99; W3_pT=-99; W4_pT=-99;
  W1_eta=-99; W2_eta=-99; W3_eta=-99; W4_eta=-99;
  W1_mass=-99; W2_mass=-99; W3_mass=-99; W4_mass=-99;

  nh=0;
  h1_pT=-99; h2_pT=-99; h3_pT=-99; h4_pT=-99;
  h1_eta=-99; h2_eta=-99; h3_eta=-99; h4_eta=-99;
  h1_mass=-99; h2_mass=-99; h3_mass=-99; h4_mass=-99;

  nH=0;
  h1_pT=-99; h2_pT=-99; h3_pT=-99; h4_pT=-99;
  h1_eta=-99; h2_eta=-99; h3_eta=-99; h4_eta=-99;
  H1_mass=-99; H2_mass=-99; H3_mass=-99; H4_mass=-99;

  nA=0;
  A1_pT=-99; A2_pT=-99; A3_pT=-99; A4_pT=-99;
  A1_eta=-99; A2_eta=-99; A3_eta=-99; A4_eta=-99;
  A1_mass=-99; A2_mass=-99; A3_mass=-99; A4_mass=-99;
}

//==============================================================================

void fillElectronBranches(std::vector<Particle> electrons){
  if(verbose) cout<<"Filling Electron Branches"<<endl;
  
  nElectron=electrons.size();
  if(nElectron>0){
    electron1_pT=electrons[0].P4->Pt();
    electron1_eta=electrons[0].P4->Eta();
  }
  if(nElectron>1){
    electron2_pT=electrons[1].P4->Pt();
    electron2_eta=electrons[1].P4->Eta();
  }
  if(nElectron>2){
    electron3_pT=electrons[2].P4->Pt();
    electron3_eta=electrons[2].P4->Eta();
  }
  if(nElectron>3){
    electron4_pT=electrons[3].P4->Pt();
    electron4_eta=electrons[3].P4->Eta();
  }
}

//==============================================================================

void fillMuonBranches(std::vector<Particle> muons){
  if(verbose) cout<<"Filling Muon Branches"<<endl;

  nMuon=muons.size();
  if(nMuon>0){
    muon1_pT=muons[0].P4->Pt();
    muon1_eta=muons[0].P4->Eta();
  }
  if(nMuon>1){
    muon2_pT=muons[1].P4->Pt();
    muon2_eta=muons[1].P4->Eta();
  }
  if(nMuon>2){
    muon3_pT=muons[2].P4->Pt();
    muon3_eta=muons[2].P4->Eta();
  }
  if(nMuon>3){
    muon4_pT=muons[3].P4->Pt();
    muon4_eta=muons[3].P4->Eta();
  }
}

//==============================================================================

void fillLeptonBranches(std::vector<Particle> leptons){
  if(verbose) cout<<"Filling Lepton Branches"<<endl;

  nLepton=leptons.size();
  if(nLepton>0){
    lepton1_pT=leptons[0].P4->Pt();
    lepton1_eta=leptons[0].P4->Eta();
  }
  if(nLepton>1){
    lepton2_pT=leptons[1].P4->Pt();
    lepton2_eta=leptons[1].P4->Eta();
  }
  if(nLepton>2){
    lepton3_pT=leptons[2].P4->Pt();
    lepton3_eta=leptons[2].P4->Eta();
  }
  if(nLepton>3){
    lepton4_pT=leptons[3].P4->Pt();
    lepton4_eta=leptons[3].P4->Eta();
  }
}

//==============================================================================

void fillTauBranches(std::vector<Particle> taus){
  if(verbose) cout<<"Filling Tau Branches"<<endl;

  nTau=taus.size();
  if(nTau>0){
    tau1_pT=taus[0].P4->Pt();
    tau1_eta=taus[0].P4->Eta();
  }
  if(nTau>1){
    tau2_pT=taus[1].P4->Pt();
    tau2_eta=taus[1].P4->Eta();
  }
  if(nTau>2){
    tau3_pT=taus[2].P4->Pt();
    tau3_eta=taus[2].P4->Eta();
  }
  if(nTau>3){
    tau4_pT=taus[3].P4->Pt();
    tau4_eta=taus[3].P4->Eta();
  }
}

//==============================================================================

void fillJetBranches(std::vector<Particle> jets){
  if(verbose) cout<<"Filling Jet Branches"<<endl;

  nJet=jets.size();
  if(nJet>0){
    jet1_pT=jets[0].P4->Pt();
    jet1_eta=jets[0].P4->Eta();
  }
  if(nJet>1){
    jet2_pT=jets[1].P4->Pt();
    jet2_eta=jets[1].P4->Eta();
  }
  if(nJet>2){
    jet3_pT=jets[2].P4->Pt();
    jet3_eta=jets[2].P4->Eta();
  }
  if(nJet>3){
    jet4_pT=jets[3].P4->Pt();
    jet4_eta=jets[3].P4->Eta();
  }
}

//==============================================================================

void fillBJetBranches(std::vector<Particle> bJets){
  if(verbose) cout<<"Filling B-Jet Branches"<<endl;

  nBJet=bJets.size();
  if(nBJet>0){
    bJet1_pT=bJets[0].P4->Pt();
    bJet1_eta=bJets[0].P4->Eta();
  }
  if(nBJet>1){
    bJet2_pT=bJets[1].P4->Pt();
    bJet2_eta=bJets[1].P4->Eta();
  }
  if(nBJet>2){
    bJet3_pT=bJets[2].P4->Pt();
    bJet3_eta=bJets[2].P4->Eta();
  }
  if(nBJet>3){
    bJet4_pT=bJets[3].P4->Pt();
    bJet4_eta=bJets[3].P4->Eta();
  }
}

//==============================================================================

void fillPhotonBranches(std::vector<Particle> photons){
  if(verbose) cout<<"Filling Photon Branches"<<endl;

  nPhoton=photons.size();
  if(nPhoton>0){
    photon1_pT=photons[0].P4->Pt();
    photon1_eta=photons[0].P4->Eta();
  }
  if(nPhoton>1){
    photon2_pT=photons[1].P4->Pt();
    photon2_eta=photons[1].P4->Eta();
  }
  if(nPhoton>2){
    photon3_pT=photons[2].P4->Pt();
    photon3_eta=photons[2].P4->Eta();
  }
  if(nPhoton>3){
    photon4_pT=photons[3].P4->Pt();
    photon4_eta=photons[3].P4->Eta();
  }
}

//==============================================================================

void fillZBranches(std::vector<Particle> Zs){
  if(verbose) cout<<"Filling Z Branches"<<endl;

  nZ=Zs.size();
  if(nZ>0){
    Z1_pT=Zs[0].P4->Pt();
    Z1_eta=Zs[0].P4->Eta();
    Z1_mass=Zs[0].P4->M();

    Z1_daughter1_pT=Zs[0].daughters[0]->P4->Pt();
    Z1_daughter2_pT=Zs[0].daughters[1]->P4->Pt();
  }
  if(nZ>1){
    Z2_pT=Zs[1].P4->Pt();
    Z2_eta=Zs[1].P4->Eta();
    Z2_mass=Zs[1].P4->M();

    Z2_daughter1_pT=Zs[1].daughters[0]->P4->Pt();
    Z2_daughter2_pT=Zs[1].daughters[1]->P4->Pt();
  }
  if(nZ>2){
    Z3_pT=Zs[2].P4->Pt();
    Z3_eta=Zs[2].P4->Eta();
    Z3_mass=Zs[2].P4->M();

    Z3_daughter1_pT=Zs[2].daughters[0]->P4->Pt();
    Z3_daughter2_pT=Zs[2].daughters[1]->P4->Pt();
  }
  if(nZ>3){
    Z4_pT=Zs[3].P4->Pt();
    Z4_eta=Zs[3].P4->Eta();
    Z4_mass=Zs[3].P4->M();

    Z4_daughter1_pT=Zs[3].daughters[0]->P4->Pt();
    Z4_daughter2_pT=Zs[3].daughters[1]->P4->Pt();
  }
}

//==============================================================================

void fillWBranches(std::vector<Particle> Ws){
  if(verbose) cout<<"Filling W Branches"<<endl;

  nW=Ws.size();
  if(nW>0){
    W1_pT=Ws[0].P4->Pt();
    W1_eta=Ws[0].P4->Eta();
    W1_mass=Ws[0].P4->M();
  }
  if(nW>1){
    W2_pT=Ws[1].P4->Pt();
    W2_eta=Ws[1].P4->Eta();
    W2_mass=Ws[1].P4->M();
  }
  if(nW>2){
    W3_pT=Ws[2].P4->Pt();
    W3_eta=Ws[2].P4->Eta();
    W3_mass=Ws[2].P4->M();
  }
  if(nW>3){
    W4_pT=Ws[3].P4->Pt();
    W4_eta=Ws[3].P4->Eta();
    W4_mass=Ws[3].P4->M();
  }
}

//==============================================================================

void fillhBranches(std::vector<Particle> hs){
  if(verbose) cout<<"Filling h Branches"<<endl;

  nh=hs.size();
  if(nh>0){
    h1_pT=hs[0].P4->Pt();
    h1_eta=hs[0].P4->Eta();
    h1_mass=hs[0].P4->M();
  }
  if(nh>1){
    h2_pT=hs[1].P4->Pt();
    h2_eta=hs[1].P4->Eta();
    h2_mass=hs[1].P4->M();
  }
  if(nh>2){
    h3_pT=hs[2].P4->Pt();
    h3_eta=hs[2].P4->Eta();
    h3_mass=hs[2].P4->M();
  }
  if(nh>3){
    h4_pT=hs[3].P4->Pt();
    h4_eta=hs[3].P4->Eta();
    h4_mass=hs[3].P4->M();
  }
}

//==============================================================================

void fillHBranches(std::vector<Particle> Hs){
  if(verbose) cout<<"Filling H Branches"<<endl;

  nH=Hs.size();
  if(nH>0){
    H1_pT=Hs[0].P4->Pt();
    H1_eta=Hs[0].P4->Eta();
    H1_mass=Hs[0].P4->M();
  }
  if(nH>1){
    H2_pT=Hs[1].P4->Pt();
    H2_eta=Hs[1].P4->Eta();
    H2_mass=Hs[1].P4->M();
  }
  if(nH>2){
    H3_pT=Hs[2].P4->Pt();
    H3_eta=Hs[2].P4->Eta();
    H3_mass=Hs[2].P4->M();
  }
  if(nH>3){
    H4_pT=Hs[3].P4->Pt();
    H4_eta=Hs[3].P4->Eta();
    H4_mass=Hs[3].P4->M();
  }
}

//==============================================================================

void fillABranches(std::vector<Particle> As){
  if(verbose) cout<<"Filling A Branches"<<endl;
  
nA=As.size();
  if(nA>0){
    A1_pT=As[0].P4->Pt();
    A1_eta=As[0].P4->Eta();
    A1_mass=As[0].P4->M();
  }
  if(nA>1){
    A2_pT=As[1].P4->Pt();
    A2_eta=As[1].P4->Eta();
    A2_mass=As[1].P4->M();
  }
  if(nA>2){
    A3_pT=As[2].P4->Pt();
    A3_eta=As[2].P4->Eta();
    A3_mass=As[2].P4->M();
  }
  if(nA>3){
    A4_pT=As[3].P4->Pt();
    A4_eta=As[3].P4->Eta();
    A4_mass=As[3].P4->M();
  }
}

//==============================================================================

void run(std::vector<TString> inputs){
  if(verbose) cout<<"Starting Analysis"<<endl;
  
  //Input
  TChain *chain = new TChain("Delphes");
  for(int lp=0; lp<inputs.size(); lp++) chain->Add(inputs[lp]);

  ExRootTreeReader *treeReader = new ExRootTreeReader(chain);
  Long64_t allEntries = treeReader->GetEntries();
  cout << "** Chain contains " << allEntries << " events" << endl;

  TClonesArray *branchEvent = treeReader->UseBranch("Event");
  TClonesArray *branchParticle = treeReader->UseBranch("Particle");

  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchPhoton = treeReader->UseBranch("Photon");
  TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchCAJet = treeReader->UseBranch("CAJet");

  TClonesArray *branchEFlowTrack = treeReader->UseBranch("EFlowTrack");
  TClonesArray *branchEFlowTower = treeReader->UseBranch("EFlowTower");
  TClonesArray *branchEFlowMuon = treeReader->UseBranch("EFlowMuon");

  //------------------------------------------------------------------------------
  //Object selection
  
  for(int eventNo = 0; eventNo < allEntries; eventNo++){
    if (eventNo%1000==0) cout<<"Event number: "<<eventNo<<endl;
    treeReader->ReadEntry(eventNo);
    resetBranches();

    LHEFEvent* event=(LHEFEvent*)branchEvent->At(0);
    eventWeight=event->Weight;

    passSingleLeptonTrigger=0;
    passDiLeptonTrigger=0;

    std::vector<Particle> allObjects,leptons;

    if(verbose) cout<<"Starting Electron Selection"<<endl;
    std::vector<Particle> electrons;
    Electron *electron;
    for(int electronNo=0; electronNo<branchElectron->GetEntriesFast(); electronNo++){
      electron=(Electron*)branchElectron->At(electronNo);
      
      if(electron->PT > electronPtMin && fabs(electron->Eta)<electronEtaMax){
	Particle e(electron->P4(),electron->Charge);
	allObjects.push_back(e);
	electrons.push_back(e);
	leptons.push_back(e);
      }
    }
    std::sort(electrons.begin(),electrons.end(),largerPt);
    fillElectronBranches(electrons);

    if(verbose) cout<<"Starting Muon Selection"<<endl;
    std::vector<Particle> muons;
    Muon *muon;
    for(int muonNo=0; muonNo<branchMuon->GetEntriesFast(); muonNo++){
      muon=(Muon*)branchMuon->At(muonNo);

      if(muon->PT > muonPtMin && fabs(muon->Eta)<muonEtaMax){
	Particle mu(muon->P4(),muon->Charge);
	allObjects.push_back(mu);
	muons.push_back(mu);
	leptons.push_back(mu);
      }
    }
    std::sort(muons.begin(),muons.end(),largerPt);
    fillMuonBranches(muons);

    if(verbose) cout<<"Sorting Leptons"<<endl;
    std::sort(leptons.begin(),leptons.end(),largerPt); 
    fillLeptonBranches(leptons);
    if(leptons.size()>0){
      if(leptons[0].P4->Pt() > singleLeptonTrigger_pTMin) passSingleLeptonTrigger=1;
      if(leptons.size()>1){
	if(leptons[0].P4->Pt() > dileptonTrigger_pTMins[0] && leptons[1].P4->Pt() > dileptonTrigger_pTMins[1]) passDiLeptonTrigger=1;
      }
    }

    if(verbose) cout<<"Starting Jet, B-jet, and Tau Selection"<<endl;
    std::vector<Particle> bJets,taus,jets;
    Jet *jet;
    for(int jetNo=0; jetNo<branchJet->GetEntriesFast(); jetNo++){
      jet=(Jet*)branchJet->At(jetNo);
      
      bool isMuon=false;
      TLorentzVector j=jet->P4();
      for(int muonNo=0; muonNo<branchMuon->GetEntriesFast(); muonNo++){
	muon=(Muon*)branchMuon->At(muonNo);
	TLorentzVector m=muon->P4();
	if(m.DeltaR(j)<0.5){
	  isMuon=true;
	  break;
	}
      }

      if(!isMuon){
	  if(jet->BTag&(1<<0) && jet->PT>bJetPtMin && fabs(jet->Eta)<bJetEtaMax){
	    allObjects.push_back(jet->P4());
	    bJets.push_back(jet->P4());
	    jets.push_back(jet->P4());
	  }
	  else {
	    if(jet->TauTag && jet->PT>tauPtMin && fabs(jet->Eta)<tauEtaMax){
	      allObjects.push_back(jet->P4());
	      taus.push_back(jet->P4());
	      leptons.push_back(jet->P4());
	    }
	    else {
	      if(jet->PT>jetPtMin && fabs(jet->Eta)<jetEtaMax){
		allObjects.push_back(jet->P4());
		jets.push_back(jet->P4());
	      }
	    }
	  }
	  fillBJetBranches(bJets);
	  fillTauBranches(taus);
	  fillJetBranches(jets);
      }
    }

    if(verbose) cout<<"Starting Photon Selection"<<endl;
    std::vector<Particle> photons;
    Photon *photon;
    for(int photonNo=0; photonNo<branchPhoton->GetEntriesFast(); photonNo++){
      photon=(Photon*)branchPhoton->At(photonNo);

      if(photon->PT > photonPtMin && fabs(photon->Eta)<photonEtaMax){
	allObjects.push_back(photon->P4());
	photons.push_back(photon->P4());
      }
    }
    fillPhotonBranches(photons);

    //------------------------------------------------------------------------------
    //Object reconstruction
    if(verbose) cout<<"Starting Object Reconstruction"<<endl;

    double METx=0;
    double METy=0;
    for(int objectNo=0; objectNo<allObjects.size(); objectNo++){
      METx+=allObjects[objectNo].P4->Px();
      METy+=allObjects[objectNo].P4->Py();
    }
    MET=sqrt(METx*METx+METy*METy);

    ST=0;
    for(int objectNo=0; objectNo<allObjects.size(); objectNo++){
      ST+=allObjects[objectNo].P4->Pt();
    }

    HT=0;
    for(int jetNo=0; jetNo<jets.size(); jetNo++)
      HT+=jets[jetNo].P4->Pt();

    std::vector<Particle> Ws, Zs, hs, Hs, As;

    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    //Leptonic Zs
    if(verbose) cout<<"Starting Leptonic Z Reconstruction"<<endl;

    Zs=getMothers(electrons,ZMassMin_emu,ZMassMax_emu,true);

    std::vector<Particle> moreZs;
    moreZs=getMothers(muons,ZMassMin_emu,ZMassMax_emu,true);
    Zs.insert(Zs.end(), moreZs.begin(), moreZs.end());

    //moreZs=getMothers(taus,ZMassMin_tau,ZMassMax_tau);
    //Zs.insert(Zs.end(), moreZs.begin(),moreZs.end());

    std::sort(Zs.begin(),Zs.end(),closerToZMass);

    fillZBranches(Zs);

    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    //Hadronic Ws: Adapted from recipe by Jim Dolen
    /*
    if(verbose) cout<<"Starting Hadronic W Reconstruction"<<endl;

    GenParticle *particle;
    Track *track;
    Tower *tower;

    TObject *constituent;
    TLorentzVector momentum;
    Particle W;
    for(int jetNo=0; jetNo<branchCAJet->GetEntriesFast(); jetNo++){
      jet=(Jet*) branchCAJet->At(jetNo);
      if (jet->PT<250) continue; 

      std::vector<fastjet::PseudoJet> input_particles;
      for(int constituentNo=0; constituentNo<jet->Constituents.GetEntriesFast(); constituentNo++){
	constituent=jet->Constituents.At(constituentNo);
        if(constituent!=0){
          momentum.SetPxPyPzE(0, 0, 0, 0);
          if(constituent->IsA()==GenParticle::Class())          
            momentum=((GenParticle*) constituent)->P4();      
          else if(constituent->IsA()==Track::Class())
            momentum=((Track*) constituent)->P4();
          if(constituent->IsA()==Tower::Class())
            momentum=((Tower*) constituent)->P4(); 
          if(constituent->IsA()==Muon::Class())
            momentum=((Muon*) constituent)->P4();
          input_particles.push_back( fastjet::PseudoJet(momentum.Px(), momentum.Py(), momentum.Pz(), momentum.E()));
        }
      }//end constituent loop
      //Recluster jet
      if(verbose) cout<<"Reclustering Jet"<<endl;

      double R=0.8;
      fastjet::JetDefinition jet_def(fastjet::cambridge_algorithm, R);
      fastjet::ClusterSequence cs(input_particles, jet_def);
      std::vector<fastjet::PseudoJet> pJets=sorted_by_pt(cs.inclusive_jets());

      if(verbose) cout<<"Pruning Jet"<<endl;
      //Pruning 
      Pruner pruner(cambridge_algorithm, zcut, Dcut_factor);
      PseudoJet prunedJet=pruner(pJets[0]);

      if(verbose) cout<<"W-tagging"<<endl;
      std::vector<PseudoJet> prunedSubjets=sorted_by_pt(prunedJet.exclusive_subjets_up_to(2));
      double mu=10000;
      if(prunedSubjets.size()>1){
        if(prunedSubjets[0].m() >  prunedSubjets[1].m()) mu=prunedSubjets[0].m()/prunedJet.m();
        else mu=prunedSubjets[1].m()/prunedJet.m();
	
	if(mu<muMax && prunedJet.m()>hadronicWMassMin && prunedJet.m()<hadronicWMassMax){
	  W.P4->SetPxPyPzE(prunedJet.px(), prunedJet.py(), prunedJet.pz(), prunedJet.E());
	  Ws.push_back(W);
	}     
      }
    }//end jet loop  

    fillWBranches(Ws);
    */

    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    //h -> bb, tautau, VV, gammagamma
    /*
    if(verbose) cout<<"Starting h Reconstruction"<<endl;

    hs=getMothers(bJets,higgsMassMin_b,higgsMassMax_b);

    std::vector<Particle> morehs;
    morehs=getMothers(taus,higgsMassMin_tau,higgsMassMax_tau);
    hs.insert(hs.end(), morehs.begin(), morehs.end());

    morehs=getMothers(Zs,higgsMassMin_Z,higgsMassMax_Z);
    hs.insert(hs.end(), morehs.begin(), morehs.end());

    morehs=getMothers(Ws,higgsMassMin_W,higgsMassMax_W);
    hs.insert(hs.end(), morehs.begin(), morehs.end());

    morehs=getMothers(photons,higgsMassMin_photon,higgsMassMax_photon);
    hs.insert(hs.end(), morehs.begin(), morehs.end());

    fillhBranches(hs);
    */
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    //H -> bb, tautau, VV, gammagamma, hh
    if(verbose) cout<<"Starting H Reconstruction"<<endl;
    
    /*
    Hs=getMothers(bJets,HAMassMin,HAMassMax);

    std::vector<Particle> moreHs;
    moreHs=getMothers(taus,HAMassMin,HAMassMax);
    Hs.insert(Hs.end(), moreHs.begin(), moreHs.end());

    moreHs=getMothers(Zs,HAMassMin,HAMassMax);
    Hs.insert(Hs.end(), moreHs.begin(), moreHs.end());

    moreHs=getMothers(Ws,HAMassMin,HAMassMax);
    Hs.insert(Hs.end(), moreHs.begin(), moreHs.end());

    moreHs=getMothers(photons,HAMassMin,HAMassMax);
    Hs.insert(Hs.end(), moreHs.begin(), moreHs.end());

    moreHs=getMothers(hs,HAMassMin,HAMassMax);
    Hs.insert(Hs.end(), moreHs.begin(), moreHs.end());
    */

    Hs=getMothers(Zs,0,9999999,false);
    fillHBranches(Hs);
    
    //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    //A -> bb, tautau, gammagamma, Zh 
    if(verbose) cout<<"Starting A Reconstruction"<<endl;

    Particle Z, h;

    As=getMothers(bJets,HAMassMin,HAMassMax);

    std::vector<Particle> moreAs;
    moreAs=getMothers(taus,HAMassMin,HAMassMax);
    As.insert(As.end(), moreAs.begin(), moreAs.end());

    moreAs=getMothers(photons,HAMassMin,HAMassMax);
    As.insert(As.end(), moreAs.begin(), moreAs.end());

    Particle ACand;
    bool usedZ[Zs.size()], usedh[hs.size()];  
    for(int ZNo=0; ZNo<Zs.size(); ZNo++) usedZ[ZNo]=false;
    for(int hNo=0; hNo<hs.size(); hNo++) usedh[hNo]=false;
    
    for(int ZNo=0; ZNo<Zs.size(); ZNo++){
      if(!usedZ[ZNo]){
	Z=Zs[ZNo];
	for(int hNo=0; hNo<hs.size(); hNo++){
	  if(!usedh[hNo]){
	    h=hs[hNo];

	    *(ACand.P4)=(*Z.P4)+(*h.P4);
	    if(ACand.P4->M()>HAMassMin && ACand.P4->M()<HAMassMax){
	      As.push_back(ACand);
	      usedZ[ZNo]=true;
	      usedh[hNo]=true;
	    }
	  }
	}
      }
    }
    for(int ZNo=0; ZNo<Zs.size(); ZNo++){
      if(usedZ[ZNo]) Zs.erase(Zs.begin()+ZNo);
    }
    for(int hNo=0; hNo<hs.size(); hNo++){
      if(usedh[hNo]) hs.erase(hs.begin()+hNo);
    }
    fillABranches(As);

    tree->Fill();
  }//end event loop

  output->Write();
  return;
}
