#include <stdlib.h>

runIt(char* fileList){
  TString cmsswBase(getenv("CMSSW_BASE"));

  TString command(".L ");
  command+=cmsswBase+TString("/libDelphes.so");
  gROOT->ProcessLine(command);

  command=TString(".include ");
  command+=cmsswBase+TString("/src/JohnStupak/snowmass/external");
  gROOT->ProcessLine(command.Data());

  gROOT->ProcessLine(".L twoHiggsDoublet.cpp+");

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
