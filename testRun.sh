#!/bin/bash
cd /afs/cern.ch/work/h/hhua/HLT_QDM/CMSSW_12_4_0_pre1/src/HLT-DQM-HTCondor/efficiencyNanoAOD/ 
# python3 topHLT-efficiency_nanoAOD.py -l root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v3-v1/2820000/e55c38a4-5776-4b0f-8190-39da36d63bca.root 
# python3 topHLT-efficiency_nanoAOD.py -l root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v4-v1/80000/6d9312db-ff45-467f-be97-2dda70897b5a.root
python3 topHLT-efficiency_nanoAOD.py -l root://cmsxrootd.fnal.gov//store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v4-v1/60000/fdd8324d-a4f8-4286-945f-5528e7ae46e9.root
