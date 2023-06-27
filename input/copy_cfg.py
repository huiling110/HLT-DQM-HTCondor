import FWCore.ParameterSet.Config as cms

# Give the process a name
process = cms.Process("PickEvent")

# Tell the process which files to use as the source
process.source = cms.Source ("PoolSource",
        #   fileNames = cms.untracked.vstring ("/store/relval/CMSSW_5_3_15/RelValPyquen_ZeemumuJets_pt10_2760GeV/DQM/PU_STARTHI53V10A_TEST_feb14-v3/00000/FE0AF9FB-C196-E311-8678-0025904CF75A.root")
          fileNames = cms.untracked.vstring ("/store/data/Run2023C/Muon0/NANOAOD/PromptNanoAODv12_v3-v1/2820000/e55c38a4-5776-4b0f-8190-39da36d63bca.root")

)

# tell the process to only run over 100 events (-1 would mean run over
#  everything
process.maxEvents = cms.untracked.PSet(
            input = cms.untracked.int32 (10000)

)

# Tell the process what filename to use to save the output
process.Out = cms.OutputModule("PoolOutputModule",
         fileName = cms.untracked.string ("MyOutputFile.root")
)

# make sure everything is hooked up
process.end = cms.EndPath(process.Out)