#!/bin/bash
#export X509_USER_PROXY=/afs/cern.ch/user/n/ntrevisa/.proxy
#voms-proxy-info
echo "Input 1:"
echo $1
scp -r /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/ .
source /cvmfs/cms.cern.ch/cmsset_default.sh
mv $1 CMSSW_12_4_0/src/filelist.py
cd CMSSW_12_4_0/src
eval `scramv1 runtime -sh`
echo "cmsRun step0_L1REPACK_RAW2DIGI.py"
cmsRun step0_L1REPACK_RAW2DIGI.py
echo "cmsRun step1_HLT.py"
cmsRun step1_HLT.py
rm step0_L1REPACK_RAW2DIGI.root
echo "cmsRun step2_RAW2DIGI_L1Reco_RECO_DQM.py"
cmsRun step2_RAW2DIGI_L1Reco_RECO_DQM.py
rm step1_HLT.root
# echo "cmsRun step3_HARVESTING.py"
# cmsRun step3_HARVESTING.py
# rm step2_RAW2DIGI_L1Reco_RECO_DQM.root
# echo "Moving output to eos"
# mv DQM_V0001_R000323755__Global__CMSSW_X_Y_Z__RECO.root /eos/user/n/ntrevisa/DQM_HLT/DQM_V0001_R000323755__Global__CMSSW_X_Y_Z__RECO.root.$1
mv step2_RAW2DIGI_L1Reco_RECO_DQM.root /eos/user/n/ntrevisa/DQM_HLT/step2_RAW2DIGI_L1Reco_RECO_DQM_$1.root
echo $1
