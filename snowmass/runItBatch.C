#include <stdlib.h>

runItBatch(char* fileList){
  TString cmsswBase(getenv("CMSSW_BASE"));

  TString command(".L ");
  command+=cmsswBase+TString("/src/JohnStupak/snowmass/libDelphes.so");
  gROOT->ProcessLine(command);

  command=TString(".include ");
  command+=cmsswBase+TString("/src/JohnStupak/snowmass/external");
  gROOT->ProcessLine(command.Data());

  //TString command(".L ");
  //command+=cmsswBase+TString("/src/JohnStupak/snowmass/twoHiggsDoublet.cpp+");
  TString command(".L twoHiggsDoublet.cpp+");
  gROOT->ProcessLine(command);

  //---------------------------------------------------------------

  vector<TString> inputs;

  ifstream inputList(fileList);
  string line;
  if(inputList.is_open()){
    while(inputList.good()){
      getline(inputList,line);
      inputs.push_back(TString(line));
    }
  }

  run(inputs);
}
