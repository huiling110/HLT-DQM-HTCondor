# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step0 -s L1REPACK:uGT,RAW2DIGI --conditions 124X_dataRun2_v2 --era Run2_2018 --data --eventcontent FEVTDEBUGHLT --inputCommands=keep *,drop Run3Scouting*_hltScouting*Packer__HLT -n 100 --filein /store/data/Run2018D/EphemeralZeroBias1/RAW/v1/000/323/755/00000/08D7B1A7-B8C5-0944-9A69-B698A2BF52EB.root --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2018_v1_3 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/Configuration/customiseUtils.L1TGlobalMenuXML --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

from filelist import *

process = cms.Process('RAW2DIGI',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1EmulatorRepack_uGT_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1),
    input = cms.untracked.int32(10),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    # fileNames = cms.untracked.vstring('/store/data/Run2018D/EphemeralZeroBias1/RAW/v1/000/323/755/00000/08D7B1A7-B8C5-0944-9A69-B698A2BF52EB.root'),
    fileNames = cms.untracked.vstring(filelist),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop Run3Scouting*_hltScouting*Packer__HLT'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step0 nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('workspace/step0_L1REPACK_RAW2DIGI.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '124X_dataRun2_v2', '')

# Path and EndPath definitions
process.L1RePack_step = cms.Path(process.SimL1Emulator)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.L1RePack_step,process.raw2digi_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseSettings
from L1Trigger.Configuration.customiseSettings import L1TSettingsToCaloParams_2018_v1_3 

#call to customisation function L1TSettingsToCaloParams_2018_v1_3 imported from L1Trigger.Configuration.customiseSettings
process = L1TSettingsToCaloParams_2018_v1_3(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseReEmul
from L1Trigger.Configuration.customiseReEmul import L1TReEmulFromRAW 

#call to customisation function L1TReEmulFromRAW imported from L1Trigger.Configuration.customiseReEmul
process = L1TReEmulFromRAW(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import L1TGlobalMenuXML 

#call to customisation function L1TGlobalMenuXML imported from L1Trigger.Configuration.customiseUtils
process = L1TGlobalMenuXML(process)

# End of customisation functions


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

process.load('L1Trigger.L1TGlobal.simGtStage2Digis_cfi')
process.load('L1Trigger.L1TGlobal.hackConditions_cff')                                                                                                       
process.L1TGlobalPrescalesVetosFract.PrescaleXMLFile = cms.string('UGT_BASE_RS_PRESCALES_L1MenuCollisions2022_v1_2_0.xml')   
process.L1TGlobalPrescalesVetosFract.FinOrMaskXMLFile = cms.string('UGT_BASE_RS_FINOR_MASK_L1MenuCollisions2022_v1_2_0.xml')  
process.simGtStage2Digis.AlgorithmTriggersUnmasked = cms.bool(False)
process.simGtStage2Digis.AlgorithmTriggersUnprescaled = cms.bool(False)
process.simGtStage2Digis.PrescaleSet = cms.uint32(4) #5 corresponds to Prescale column at 1.5e34 (At the moment,It is advised to run the skim at this L1 PS column for EZB dataset)
process.simGtStage2Digis.resetPSCountersEachLumiSec = cms.bool(False)
