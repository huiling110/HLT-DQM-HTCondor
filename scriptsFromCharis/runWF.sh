#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_12_4_0_pre1
cd CMSSW_12_4_0_pre1/src
eval `scramv1 runtime -sh`
cd ../..
export ROOTSYS=/cvmfs/cms.cern.ch/slc7_amd64_gcc10/lcg/root/6.22.08-1bf9217ea66f92d678a8d856b78bb35b/
export PATH=$PATH:$ROOTSYS/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ROOTSYS/lib
ls -ltr
lines=(`cat Muon2022_RunF.txt`)
echo ${lines[$1]}
python3 topHLT-efficiency_nanoAOD.py -l ${lines[$1]}
mv Efficiency_hists.root  Efficiency_hists_Muon_2022_RunF_$1.root
