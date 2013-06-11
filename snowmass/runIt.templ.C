{
  gROOT->ProcessLine(".L /uscms/home/jstupak/snowmass/standalone/CMSSW_5_3_6/src/Delphes-3.0.9/libDelphes.so");
  gROOT->ProcessLine(".L /uscms/home/jstupak/snowmass/standalone/CMSSW_5_3_6/src/Delphes-3.0.9/twoHiggsDoublet.cpp+");

  vector<TString> inputs;

  ifstream inputList("INPUTS");
  string line;
  if(inputList.is_open()){
    while(inputList.good()){
      getline(inputList,line);
      inputs.push_back(TString(line));
    }
  }

  run(inputs);
}
