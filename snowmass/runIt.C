#include <stdlib.h> 

runIt(){
  gROOT->ProcessLine(".L libDelphes.so");
  
  TString incDir(getenv("CMSSW_BASE"));
  TString command(".include ");
  command+=incDir+TString("/src/JohnStupak/snowmass/external");
  gROOT->ProcessLine(command.Data());
  
  gROOT->ProcessLine(".L twoHiggsDoublet.cpp+");
  
  vector<TString> inputs;
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_7694.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_7829.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_7900.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_8231.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_832419311.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_854761553.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_8635.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_8865.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_9018.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_93106106.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_9347.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_93662892.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_9389.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_95961970.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_9630.root"));
  inputs.push_back(TString("dcap://cmsgridftp.fnal.gov:24125/pnfs/fnal.gov/usr/cms/WAX/11/store/user/snowmass/Delphes-3.0.9/NoPileUp/WJETS_13TEV/WJETS_13TEV_NoPileUp_98103320.root"));
  
    run(inputs);
}
