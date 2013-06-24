#!/bin/csh

source /uscmst1/prod/sw/cms/cshrc prod
cd CMSSWBASE/src/
cmsenv

cd -
ln -s ${CMSSW_BASE}/src/JohnStupak/snowmass/external
ln -s ${CMSSW_BASE}/src/JohnStupak/snowmass/modules
ln -s ${CMSSW_BASE}/src/JohnStupak/snowmass/classes

cp ${CMSSW_BASE}/src/JohnStupak/snowmass/runItBatch.C .
cp ${CMSSW_BASE}/src/JohnStupak/snowmass/twoHiggsDoublet.cpp .

root -l -b -q runItBatch.C\(\"INPUTS\"\)

mv twoHiggsDoublet.root OUTPUT
