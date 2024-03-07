
import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
### parsing job options 
import sys

options = VarParsing.VarParsing()

options.register('inputScript','',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"input Script")
options.register('outputFile','output',VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string,"output File (w/o .root)")
options.register('maxEvents', -1,VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.int,"maximum events")
options.register('skipEvents', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "total jobs")
options.register('reportEvery', 1000, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "report every")
options.register('gluonReduction', 0.0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.float, "gluon reduction")
options.register('selectJets', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "select jets with good gen match")
options.register('phase2', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "apply jet selection for phase 2. Currently sets JetEtaMax to 3.0 and picks slimmedJetsPuppi as jet collection.")
options.register('puppi', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use puppi jets")
options.register('eta', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use eta up to 5.0")
#options.register('roccorData', 'DeepNTuples/DeepNtuplizer/data/RochesterCorrections/RoccoR2018UL.txt', VarParsing.VarParsing.multiplicity.singleton,
 #                VarParsing.VarParsing.varType.string,'location of rochester correction files via edm::FilePath')
options.register('isMC', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "use MC info (gen) or not")

import os
release=os.environ['CMSSW_VERSION'][6:]
print("Using release "+release)


options.register(
	'inputFiles','',
	VarParsing.VarParsing.multiplicity.list,
	VarParsing.VarParsing.varType.string,
	"input files (default is the tt RelVal)"
	)

if hasattr(sys, "argv"):
    options.parseArguments()



if options.puppi:
    usePuppi = True
else:
    usePuppi = False
process = cms.Process("DNNFiller")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#'auto:run2_mc'
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_dataRun3_PromptAnalysis_v1', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

process.options = cms.untracked.PSet(
   allowUnscheduled = cms.untracked.bool(True),  
   wantSummary=cms.untracked.bool(False)
)


process.load('DeepNTuples.DeepNtuplizer.samples.TTJetsPhase1_cfg') #default input


if options.inputFiles:
	process.source.fileNames = options.inputFiles

if options.inputScript != '' and options.inputScript != 'DeepNTuples.DeepNtuplizer.samples.TTJetsPhase1_cfg':
    process.load(options.inputScript)

numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job


process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)

process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
process.maxEvents  = cms.untracked.PSet( 
    input = cms.untracked.int32 (options.maxEvents) 
)
releases = release.split("_")

bTagInfos = ['pfDeepFlavourTagInfos',
             'pfImpactParameterTagInfos',
             'pfInclusiveSecondaryVertexFinderTagInfos',
             'pfParticleNetAK4TagInfos',] #['pfParticleTransformerAK4TagInfos',]

from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsAll as pfParticleNetAK4JetTagsAll
from RecoBTag.ONNXRuntime.pfParticleNetFromMiniAODAK4_cff import _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs

if (int(releases[0])>8) or ( (int(releases[0])==8) and (int(releases[1]) >= 4) ) :
 bTagDiscriminators = [
     'pfDeepCSVJetTags:probudsg', #to be fixed with new names
     'pfDeepCSVJetTags:probb',
     'pfDeepCSVJetTags:probc',
     'pfDeepCSVJetTags:probbb',
     'pfDeepFlavourJetTags:probb',
     'pfDeepFlavourJetTags:probbb',
     'pfDeepFlavourJetTags:problepb',
     'pfDeepFlavourJetTags:probc',
     'pfDeepFlavourJetTags:probuds',
     'pfDeepFlavourJetTags:probg',
     'pfParticleTransformerAK4JetTags:probb',
     'pfParticleTransformerAK4JetTags:probbb',
     'pfParticleTransformerAK4JetTags:problepb',
     'pfParticleTransformerAK4JetTags:probc',
     'pfParticleTransformerAK4JetTags:probuds',
     'pfParticleTransformerAK4JetTags:probg',
 ] + _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs + pfParticleNetAK4JetTagsAll
else :
  bTagDiscriminators = [
      'pfDeepCSVJetTags:probudsg', #to be fixed with new names
      'pfDeepCSVJetTags:probb',
      'pfDeepCSVJetTags:probc',
      'pfDeepCSVJetTags:probbb',
      'pfDeepCSVJetTags:probcc',
      'pfDeepFlavourJetTags:probb',
      'pfDeepFlavourJetTags:probbb',
      'pfDeepFlavourJetTags:problepb',
      'pfDeepFlavourJetTags:probc',
      'pfDeepFlavourJetTags:probuds',
      'pfDeepFlavourJetTags:probg',
      'pfParticleTransformerAK4JetTags:probb',
      'pfParticleTransformerAK4JetTags:probbb',
      'pfParticleTransformerAK4JetTags:problepb',
      'pfParticleTransformerAK4JetTags:probc',
      'pfParticleTransformerAK4JetTags:probuds',
      'pfParticleTransformerAK4JetTags:probg',
 ] + _pfParticleNetFromMiniAODAK4PuppiCentralJetTagsProbs + pfParticleNetAK4JetTagsAll

jetCorrectionsAK4 = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None')

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
if options.phase2:
    usePuppi = True

if usePuppi:
    jet_collection = 'slimmedJetsPuppi'
else:
    jet_collection = 'slimmedJets'

updateJetCollection(
        process,
        labelName = "DeepFlavour",
#         jetSource=cms.InputTag('slimmedJetsAK8PFPuppiSoftDropPacked', 'SubJets'),  # 'subjets from AK8'
        jetSource = cms.InputTag(jet_collection),  # 'ak4Jets'
        jetCorrections = jetCorrectionsAK4,
        pfCandidates = cms.InputTag('packedPFCandidates'),
        pvSource = cms.InputTag("offlineSlimmedPrimaryVertices"),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        muSource = cms.InputTag('slimmedMuons'),
        elSource = cms.InputTag('slimmedElectrons'),
        btagInfos = bTagInfos,
        btagDiscriminators = bTagDiscriminators,
        explicitJTA = False
)

if hasattr(process,'updatedPatJetsTransientCorrectedDeepFlavour'):
	process.updatedPatJetsTransientCorrectedDeepFlavour.addTagInfos = cms.bool(True) 
	process.updatedPatJetsTransientCorrectedDeepFlavour.addBTagInfo = cms.bool(True)
else:
	raise ValueError('I could not find updatedPatJetsTransientCorrectedDeepFlavour to embed the tagInfos, please check the cfg')


# QGLikelihood
process.load("DeepNTuples.DeepNtuplizer.QGLikelihood_cfi")
process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", "QGPoolDBESSource")
process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets   = cms.InputTag("selectedUpdatedPatJetsDeepFlavour")
process.QGTagger.jetsLabel = cms.string('QGL_AK4PFchs')


#from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
#process.ak4GenJetsWithNu = ak4GenJets.clone(src = 'packedGenParticles')
 
 ## Filter out neutrinos from packed GenParticles
#process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))
 ## Define GenJets
#process.ak4GenJetsRecluster = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')

#process.patGenJetMatchAllowDuplicates = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
#    src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
#    matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
#    mcPdgId     = cms.vint32(),                      # n/a   
#    mcStatus    = cms.vint32(),                      # n/a   
#    checkCharge = cms.bool(False),                   # n/a   
#    maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
#    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
#    resolveAmbiguities    = cms.bool(False),          # Forbid two RECO objects to match to the same GEN object 
#    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
#)
 
 
#process.patGenJetMatchWithNu = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
#    src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
#    matched     = cms.InputTag("ak4GenJetsWithNu"),        # GEN jets  (must be GenJetCollection)              
#    mcPdgId     = cms.vint32(),                      # n/a   
#    mcStatus    = cms.vint32(),                      # n/a   
#    checkCharge = cms.bool(False),                   # n/a   
#    maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
#    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
#    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
#    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
#)

#process.patGenJetMatchRecluster = cms.EDProducer("GenJetMatcher",  # cut on deltaR; pick best by deltaR           
#    src         = cms.InputTag("selectedUpdatedPatJetsDeepFlavour"),      # RECO jets (any View<Jet> is ok) 
#    matched     = cms.InputTag("ak4GenJetsRecluster"),        # GEN jets  (must be GenJetCollection)              
#    mcPdgId     = cms.vint32(),                      # n/a   
#    mcStatus    = cms.vint32(),                      # n/a   
#    checkCharge = cms.bool(False),                   # n/a   
#    maxDeltaR   = cms.double(0.4),                   # Minimum deltaR for the match   
#    #maxDPtRel   = cms.double(3.0),                  # Minimum deltaPt/Pt for the match (not used in GenJetMatcher)                     
#    resolveAmbiguities    = cms.bool(True),          # Forbid two RECO objects to match to the same GEN object 
#    resolveByMatchQuality = cms.bool(False),         # False = just match input in order; True = pick lowest deltaR pair first          
#)

#process.genJetSequence = cms.Sequence(process.packedGenParticlesForJetsNoNu*process.ak4GenJetsWithNu*process.ak4GenJetsRecluster*process.patGenJetMatchAllowDuplicates*process.patGenJetMatchWithNu*process.patGenJetMatchRecluster)


# Very Loose IVF SV collection
from PhysicsTools.PatAlgos.tools.helpers import loadWithPrefix
loadWithPrefix(process, 'RecoVertex.AdaptiveVertexFinder.inclusiveVertexing_cff', "looseIVF")
process.looseIVFinclusiveCandidateVertexFinder.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFinclusiveCandidateVertexFinder.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLen2DSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.vertexMinDLenSig = cms.double(0.)
process.looseIVFinclusiveCandidateVertexFinder.fitterSigmacut = 20

process.looseIVFcandidateVertexArbitrator.primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices")
process.looseIVFcandidateVertexArbitrator.tracks = cms.InputTag("packedPFCandidates")
process.looseIVFcandidateVertexArbitrator.secondaryVertices = cms.InputTag("looseIVFcandidateVertexMerger")
process.looseIVFcandidateVertexArbitrator.fitterSigmacut = 20


outFileName = options.outputFile + '_' + str(options.job) +  '.root'
print ('Using output file ' + outFileName)

process.TFileService = cms.Service("TFileService", 
                                   fileName = cms.string(outFileName))

# DeepNtuplizer
process.load("DeepNTuples.DeepNtuplizer.DeepNtuplizer_cfi")
process.deepntuplizer.jets = cms.InputTag('selectedUpdatedPatJetsDeepFlavour')
process.deepntuplizer.bDiscriminators = bTagDiscriminators 
process.deepntuplizer.bDiscriminators.append('pfCombinedMVAV2BJetTags')
process.deepntuplizer.LooseSVs = cms.InputTag("looseIVFinclusiveCandidateSecondaryVertices")

process.deepntuplizer.applySelection = cms.bool(options.selectJets)

if ( int(releases[0]) > 8 ) or ( (int(releases[0])==8) and (int(releases[1]) >= 4) ):
   process.deepntuplizer.tagInfoName = cms.string('pfDeepCSV')

if options.isMC:
    process.deepntuplizer.MC = cms.bool(True)
if options.eta :
    process.deepntuplizer.jetAbsEtaMax = cms.double(5.0)
    process.deepntuplizer.jetPtMin = cms.double(10.0)
else :
    process.deepntuplizer.jetAbsEtaMax = cms.double(2.5)
    process.deepntuplizer.jetPtMin = cms.double(15.0)

if options.phase2 :
    process.deepntuplizer.jetAbsEtaMax = cms.double(3.0)

process.deepntuplizer.gluonReduction  = cms.double(options.gluonReduction)

### Rochester corrections for muons
#process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
 #   correctedMuons = cms.PSet(
  #      initialSeed = cms.untracked.uint32(1),
   #     engineName  = cms.untracked.string('TRandom3')
    #)
#)

######## Correct muons with the Rochester corrections                                                                                                                                                 
#process.correctedMuons = cms.EDProducer("RochesterCorrectedMuonProducer",
 #   src     = cms.InputTag("slimmedMuons"),
  #  gens    = cms.InputTag("prunedGenParticles"),
   # data    = cms.FileInPath(options.roccorData),
    #isMC    = cms.bool(options.isMC),
#)

#Domain region
from DeepNTuples.DeepNtuplizer.emu_skim_cff import emuSelection
process = emuSelection(process,"pfParticleNetAK4JetTags");
process.deepntuplizer.leptonPairs = cms.InputTag("emuPairs")

#1631
process.ProfilerService = cms.Service (
      "ProfilerService",
       firstEvent = cms.untracked.int32(1631),
       lastEvent = cms.untracked.int32(1641),
       paths = cms.untracked.vstring('p') 
)

#Trick to make it work in 9_1_X
process.tsk = cms.Task()
for mod in process.producers_().values(): #.itervalues():
    process.tsk.add(mod)
for mod in process.filters_().values(): #.itervalues():
    process.tsk.add(mod)

process.p = cms.Path(
	process.QGTagger +
#        process.genJetSequence *
        process.leptonSelection *
        process.jetSelection *
	process.deepntuplizer,
	process.tsk
	)