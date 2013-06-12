#!/bin/csh

#
#_____ setup the environment ____________________________________________
#

#setenv PATH /bin:/usr/bin:/usr/local/bin:/usr/krb5/bin:/usr/afsws/bin:/usr/krb5/bin/aklog

source /uscmst1/prod/sw/cms/cshrc prod
cd CMSSWBASE/src/
cmsenv

#setenv SCRAM_ARCH slc5_amd64_gcc462
#eval `scramv1 runtime -csh`

cd -


root -l -b -q ${CMSSW_BASE}/src/JohnStupak/snowmass/runItBatch.C\(\"INPUTS\"\)

mv twoHiggsDoublet.root OUTPUT
