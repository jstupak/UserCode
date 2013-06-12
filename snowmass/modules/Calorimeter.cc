
/** \class Calorimeter
 *
 *  Fills calorimeter towers, performs calorimeter resolution smearing,
 *  preselects towers hit by photons and creates energy flow objects.
 *
 *  $Date: 2013-04-09 18:05:58 +0200 (Tue, 09 Apr 2013) $
 *  $Revision: 1086 $
 *
 *
 *  \author P. Demin - UCL, Louvain-la-Neuve
 *
 */

#include "modules/Calorimeter.h"

#include "classes/DelphesClasses.h"
#include "classes/DelphesFactory.h"
#include "classes/DelphesFormula.h"

#include "ExRootAnalysis/ExRootResult.h"
#include "ExRootAnalysis/ExRootFilter.h"
#include "ExRootAnalysis/ExRootClassifier.h"

#include "TMath.h"
#include "TString.h"
#include "TFormula.h"
#include "TRandom3.h"
#include "TObjArray.h"
#include "TDatabasePDG.h"
#include "TLorentzVector.h"

#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <sstream>

using namespace std;

//------------------------------------------------------------------------------

Calorimeter::Calorimeter() :
  fECalResolutionFormula(0), fHCalResolutionFormula(0),
  fItParticleInputArray(0), fItTrackInputArray(0),
  fTowerTrackArray(0), fItTowerTrackArray(0),
  fTowerPhotonArray(0), fItTowerPhotonArray(0)
{
  fECalResolutionFormula = new DelphesFormula;
  fHCalResolutionFormula = new DelphesFormula;
  fTowerTrackArray = new TObjArray;
  fItTowerTrackArray = fTowerTrackArray->MakeIterator();
  fTowerPhotonArray = new TObjArray;
  fItTowerPhotonArray = fTowerPhotonArray->MakeIterator();
}

//------------------------------------------------------------------------------

Calorimeter::~Calorimeter()
{
  if(fECalResolutionFormula) delete fECalResolutionFormula;
  if(fHCalResolutionFormula) delete fHCalResolutionFormula;
  if(fTowerTrackArray) delete fTowerTrackArray;
  if(fItTowerTrackArray) delete fItTowerTrackArray;
  if(fTowerPhotonArray) delete fTowerPhotonArray;
  if(fItTowerPhotonArray) delete fItTowerPhotonArray;
}

//------------------------------------------------------------------------------

void Calorimeter::Init()
{
  ExRootConfParam param, paramEtaBins, paramPhiBins, paramFractions;
  Long_t i, j, k, size, sizeEtaBins, sizePhiBins, sizeFractions;
  Double_t ecalFraction, hcalFraction;
  TBinMap::iterator itEtaBin;
  set< Double_t >::iterator itPhiBin;
  vector< Double_t > *phiBins;

  // read eta and phi bins
  param = GetParam("EtaPhiBins");
  size = param.GetSize();
  fBinMap.clear();
  fEtaBins.clear();
  fPhiBins.clear();
  for(i = 0; i < size/2; ++i)
  {
    paramEtaBins = param[i*2];
    sizeEtaBins = paramEtaBins.GetSize();
    paramPhiBins = param[i*2 + 1];
    sizePhiBins = paramPhiBins.GetSize();

    for(j = 0; j < sizeEtaBins; ++j)
    {
      for(k = 0; k < sizePhiBins; ++k)
      {
        fBinMap[paramEtaBins[j].GetDouble()].insert(paramPhiBins[k].GetDouble());
      }
    }
  }

  // for better performance we transform map of sets to parallel vectors:
  // vector< double > and vector< vector< double >* >
  for(itEtaBin = fBinMap.begin(); itEtaBin != fBinMap.end(); ++itEtaBin)
  {
    fEtaBins.push_back(itEtaBin->first);
    phiBins = new vector< double >(itEtaBin->second.size());
    fPhiBins.push_back(phiBins);
    phiBins->clear();
    for(itPhiBin = itEtaBin->second.begin(); itPhiBin != itEtaBin->second.end(); ++itPhiBin)
    {
      phiBins->push_back(*itPhiBin);
    }
  }

  // read energy fractions for different particles
  param = GetParam("EnergyFraction");
  size = param.GetSize();

  // set default energy fractions values
  fFractionMap.clear();
  fFractionMap[0] = make_pair(0.0, 1.0);

  for(i = 0; i < size/2; ++i)
  {
    paramFractions = param[i*2 + 1];
    sizeFractions = paramFractions.GetSize();

    ecalFraction = paramFractions[0].GetDouble();
    hcalFraction = paramFractions[1].GetDouble();

    fFractionMap[param[i*2].GetInt()] = make_pair(ecalFraction, hcalFraction);
  }
/*
  TFractionMap::iterator itFractionMap;
  for(itFractionMap = fFractionMap.begin(); itFractionMap != fFractionMap.end(); ++itFractionMap)
  {
    cout << itFractionMap->first << "   " << itFractionMap->second.first  << "   " << itFractionMap->second.second << endl;
  }
*/
  // read resolution formulas
  fECalResolutionFormula->Compile(GetString("ECalResolutionFormula", "0"));
  fHCalResolutionFormula->Compile(GetString("HCalResolutionFormula", "0"));

  // import array with output from other modules
  fParticleInputArray = ImportArray(GetString("ParticleInputArray", "ParticlePropagator/particles"));
  fItParticleInputArray = fParticleInputArray->MakeIterator();

  fTrackInputArray = ImportArray(GetString("TrackInputArray", "ParticlePropagator/tracks"));
  fItTrackInputArray = fTrackInputArray->MakeIterator();

  // create output arrays
  fTowerOutputArray = ExportArray(GetString("TowerOutputArray", "towers"));
  fPhotonOutputArray = ExportArray(GetString("PhotonOutputArray", "photons"));

  fEFlowTrackOutputArray = ExportArray(GetString("EFlowTrackOutputArray", "eflowTracks"));
  fEFlowTowerOutputArray = ExportArray(GetString("EFlowTowerOutputArray", "eflowTowers"));
}

//------------------------------------------------------------------------------

void Calorimeter::Finish()
{
  vector< vector< Double_t>* >::iterator itPhiBin;
  if(fItParticleInputArray) delete fItParticleInputArray;
  if(fItTrackInputArray) delete fItTrackInputArray;
  for(itPhiBin = fPhiBins.begin(); itPhiBin != fPhiBins.end(); ++itPhiBin)
  {
    delete *itPhiBin;
  }
}

//------------------------------------------------------------------------------

void Calorimeter::Process()
{
  Candidate *particle, *track;
  TLorentzVector position, momentum;
  Short_t etaBin, phiBin, flags;
  Int_t number;
  Long64_t towerHit, towerEtaPhi, hitEtaPhi;
  Double_t ecalFraction, hcalFraction;
  Double_t ecalEnergy, hcalEnergy;
  Int_t pdgCode;

  TFractionMap::iterator itFractionMap;

  vector< Double_t >::iterator itEtaBin;
  vector< Double_t >::iterator itPhiBin;
  vector< Double_t > *phiBins;

  vector< Long64_t >::iterator itTowerHits;

  DelphesFactory *factory = GetFactory();
  fTowerHits.clear();
  fECalFractions.clear();
  fHCalFractions.clear();

  // loop over all particles
  fItParticleInputArray->Reset();
  number = -1;
  while((particle = static_cast<Candidate*>(fItParticleInputArray->Next())))
  {
    const TLorentzVector &particlePosition = particle->Position;
    ++number;

    pdgCode = TMath::Abs(particle->PID);

    itFractionMap = fFractionMap.find(pdgCode);
    if(itFractionMap == fFractionMap.end())
    {
      itFractionMap = fFractionMap.find(0);
    }

    ecalFraction = itFractionMap->second.first;
    hcalFraction = itFractionMap->second.second;

    fECalFractions.push_back(ecalFraction);
    fHCalFractions.push_back(hcalFraction);

    if(ecalFraction < 1.0E-9 && hcalFraction < 1.0E-9) continue;

    // find eta bin [1, fEtaBins.size - 1]
    itEtaBin = lower_bound(fEtaBins.begin(), fEtaBins.end(), particlePosition.Eta());
    if(itEtaBin == fEtaBins.begin() || itEtaBin == fEtaBins.end()) continue;
    etaBin = distance(fEtaBins.begin(), itEtaBin);

    // phi bins for given eta bin
    phiBins = fPhiBins[etaBin];

    // find phi bin [1, phiBins.size - 1]
    itPhiBin = lower_bound(phiBins->begin(), phiBins->end(), particlePosition.Phi());
    if(itPhiBin == phiBins->begin() || itPhiBin == phiBins->end()) continue;
    phiBin = distance(phiBins->begin(), itPhiBin);

    flags = (particle->Charge == 0);
    flags |= (pdgCode == 22) << 1;
    flags |= (pdgCode == 11) << 2;

    // make tower hit {16-bits for eta bin number, 16-bits for phi bin number, 8-bits for flags, 24-bits for particle number}
    towerHit = (Long64_t(etaBin) << 48) | (Long64_t(phiBin) << 32) | (Long64_t(flags) << 24) | Long64_t(number);

    fTowerHits.push_back(towerHit);
  }

  // loop over all tracks
  fItTrackInputArray->Reset();
  number = -1;
  while((track = static_cast<Candidate*>(fItTrackInputArray->Next())))
  {
    const TLorentzVector &trackPosition = track->Position;
    ++number;

    // find eta bin [1, fEtaBins.size - 1]
    itEtaBin = lower_bound(fEtaBins.begin(), fEtaBins.end(), trackPosition.Eta());
    if(itEtaBin == fEtaBins.begin() || itEtaBin == fEtaBins.end()) continue;
    etaBin = distance(fEtaBins.begin(), itEtaBin);

    // phi bins for given eta bin
    phiBins = fPhiBins[etaBin];

    // find phi bin [1, phiBins.size - 1]
    itPhiBin = lower_bound(phiBins->begin(), phiBins->end(), trackPosition.Phi());
    if(itPhiBin == phiBins->begin() || itPhiBin == phiBins->end()) continue;
    phiBin = distance(phiBins->begin(), itPhiBin);

    // make tower hit {16-bits for eta bin number, 16-bits for phi bin number, 8-bits for flags, 24-bits for track number}
    towerHit = (Long64_t(etaBin) << 48) | (Long64_t(phiBin) << 32) | (Long64_t(1) << 27) | Long64_t(number);

    fTowerHits.push_back(towerHit);
  }

  // all hits are sorted first by eta bin number, then by phi bin number,
  // then by flags and then by particle or track number
  sort(fTowerHits.begin(), fTowerHits.end());

  // loop over all hits
  towerEtaPhi = 0;
  fTower = 0;
  for(itTowerHits = fTowerHits.begin(); itTowerHits != fTowerHits.end(); ++itTowerHits)
  {
    towerHit = (*itTowerHits);
    flags = (towerHit >> 24) & 0x00000000000000FFLL;
    number = (towerHit) & 0x0000000000FFFFFFLL;
    hitEtaPhi = towerHit >> 32;

    if(towerEtaPhi != hitEtaPhi)
    {
      // switch to next tower
      towerEtaPhi = hitEtaPhi;

      // finalize previous tower
      FinalizeTower();

      // create new tower
      fTower = factory->NewCandidate();

      phiBin = (towerHit >> 32) & 0x000000000000FFFFLL;
      etaBin = (towerHit >> 48) & 0x000000000000FFFFLL;

      // phi bins for given eta bin
      phiBins = fPhiBins[etaBin];

      // calculate eta and phi of the tower's center
      fTowerEta = 0.5*(fEtaBins[etaBin - 1] + fEtaBins[etaBin]);
      fTowerPhi = 0.5*((*phiBins)[phiBin - 1] + (*phiBins)[phiBin]);

      fTowerEdges[0] = fEtaBins[etaBin - 1];
      fTowerEdges[1] = fEtaBins[etaBin];
      fTowerEdges[2] = (*phiBins)[phiBin - 1];
      fTowerEdges[3] = (*phiBins)[phiBin];

      fTowerECalEnergy = 0.0;
      fTowerHCalEnergy = 0.0;

      fTowerECalNeutralEnergy = 0.0;
      fTowerHCalNeutralEnergy = 0.0;

      fTowerNeutralHits = 0;
      fTowerPhotonHits = 0;
      fTowerElectronHits = 0;
      fTowerTrackHits = 0;
      fTowerAllHits = 0;

      fTowerTrackArray->Clear();
      fTowerPhotonArray->Clear();
    }

    // check for track hits
    if(flags & 8)
    {
      ++fTowerTrackHits;
      track = static_cast<Candidate*>(fTrackInputArray->At(number));
      fTowerTrackArray->Add(track);
      continue;
    }

    particle = static_cast<Candidate*>(fParticleInputArray->At(number));
    momentum = particle->Momentum;

    // fill current tower
    ecalEnergy = momentum.E() * fECalFractions[number];
    hcalEnergy = momentum.E() * fHCalFractions[number];

    fTowerECalEnergy += ecalEnergy;
    fTowerHCalEnergy += hcalEnergy;

    ++fTowerAllHits;
    fTower->AddCandidate(particle);

    // check for neutral hits in current tower
    if(flags & 1) ++fTowerNeutralHits;

    // check for photon hits in current tower
    if(flags & 2)
    {
      ++fTowerPhotonHits;
      fTowerPhotonArray->Add(particle);
    }

    // check for electron hits in current tower
    if(flags & 4) ++fTowerElectronHits;
  }

  // finalize last tower
  FinalizeTower();
}

//------------------------------------------------------------------------------

void Calorimeter::FinalizeTower()
{
  Candidate *particle, *track, *tower;
  Double_t energy, pt, eta, phi;
  Double_t ecalEnergy, hcalEnergy;

  if(!fTower) return;

  ecalEnergy = gRandom->Gaus(fTowerECalEnergy, fECalResolutionFormula->Eval(0.0, fTowerEta, 0.0, fTowerECalEnergy));
  if(ecalEnergy < 0.0) ecalEnergy = 0.0;

  hcalEnergy = gRandom->Gaus(fTowerHCalEnergy, fHCalResolutionFormula->Eval(0.0, fTowerEta, 0.0, fTowerHCalEnergy));
  if(hcalEnergy < 0.0) hcalEnergy = 0.0;

  energy = ecalEnergy + hcalEnergy;

  // eta = fTowerEta;
  // phi = fTowerPhi;

  eta = gRandom->Uniform(fTowerEdges[0], fTowerEdges[1]);
  phi = gRandom->Uniform(fTowerEdges[2], fTowerEdges[3]);

  pt = energy / TMath::CosH(eta);

  fTower->Position.SetPtEtaPhiE(1.0, eta, phi, 0.0);
  fTower->Momentum.SetPtEtaPhiE(pt, eta, phi, energy);
  fTower->Eem = ecalEnergy;
  fTower->Ehad = hcalEnergy;

  fTower->Edges[0] = fTowerEdges[0];
  fTower->Edges[1] = fTowerEdges[1];
  fTower->Edges[2] = fTowerEdges[2];
  fTower->Edges[3] = fTowerEdges[3];

  // fill calorimeter towers and photon candidates
  if(energy > 0.0)
  {
    if((fTowerPhotonHits > 0 || fTowerElectronHits > 0) &&
        fTowerTrackHits == 0)
    {
      fPhotonOutputArray->Add(fTower);
    }

    fTowerOutputArray->Add(fTower);
  }

  // fill energy flow candidates
  if(fTowerTrackHits == fTowerAllHits)
  {
    fItTowerTrackArray->Reset();
    while((track = static_cast<Candidate*>(fItTowerTrackArray->Next())))
    {
      fEFlowTrackOutputArray->Add(track);
    }
  }
  else if(fTowerTrackHits > 0 &&
          fTowerElectronHits == 0 &&
          fTowerPhotonHits + fTowerTrackHits == fTowerAllHits)
  {
    fItTowerTrackArray->Reset();
    while((track = static_cast<Candidate*>(fItTowerTrackArray->Next())))
    {
      fEFlowTrackOutputArray->Add(track);
    }

    if(ecalEnergy > 0.0)
    {
      DelphesFactory *factory = GetFactory();

      // create new tower
      tower = factory->NewCandidate();

      fItTowerPhotonArray->Reset();
      while((particle = static_cast<Candidate*>(fItTowerPhotonArray->Next())))
      {
        tower->AddCandidate(particle);
      }

      pt = ecalEnergy / TMath::CosH(eta);

      tower->Position.SetPtEtaPhiE(1.0, eta, phi, 0.0);
      tower->Momentum.SetPtEtaPhiE(pt, eta, phi, ecalEnergy);
      tower->Eem = ecalEnergy;
      tower->Ehad = 0.0;

      tower->Edges[0] = fTowerEdges[0];
      tower->Edges[1] = fTowerEdges[1];
      tower->Edges[2] = fTowerEdges[2];
      tower->Edges[3] = fTowerEdges[3];

      fEFlowTowerOutputArray->Add(tower);
    }
  }
  else if(energy > 0.0)
  {
    fEFlowTowerOutputArray->Add(fTower);
  }
}

//------------------------------------------------------------------------------
