#!/bin/bash
# Check input and where we are
echo "Input 1:" $1
echo $PWD
mkdir -p workspace
# Sources
cd /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/src/HLT-DQM-HTCondor/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd -
scp /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/src/HLT-DQM-HTCondor/$1 ./filelist.py
ls -lrt
# Step0
echo "cmsRun step0_L1REPACK_RAW2DIGI.py"
echo $PWD
scp /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/src/HLT-DQM-HTCondor/step0_L1REPACK_RAW2DIGI.py .
cmsRun step0_L1REPACK_RAW2DIGI.py
# Step1
echo "cmsRun step1_HLT.py"
echo $PWD
scp /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/src/HLT-DQM-HTCondor/step1_HLT.py .
cmsRun step1_HLT.py
rm workspace/step0_L1REPACK_RAW2DIGI.root
# Step2
echo "cmsRun step2_RAW2DIGI_L1Reco_RECO_DQM.py"
echo $PWD
scp /afs/cern.ch/user/n/ntrevisa/work/HLT_DQM/CMSSW_12_4_0/src/HLT-DQM-HTCondor/step2_RAW2DIGI_L1Reco_RECO_DQM.py .
cmsRun step2_RAW2DIGI_L1Reco_RECO_DQM.py
rm workspace/step1_HLT.root
# Finish
mv workspace/step2_RAW2DIGI_L1Reco_RECO_DQM.root /eos/user/n/ntrevisa/DQM_HLT/step2_RAW2DIGI_L1Reco_RECO_DQM_${1/\//_}.root
echo ${1/\//_}
