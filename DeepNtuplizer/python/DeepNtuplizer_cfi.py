import FWCore.ParameterSet.Config as cms

deepntuplizer = cms.EDAnalyzer('DeepNtuplizer',
                                vertices   = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                secVertices = cms.InputTag("slimmedSecondaryVertices"),
                                jets       = cms.InputTag("slimmedJetsPuppi"),
                                V0_ks = cms.InputTag("slimmedKshortVertices"),
                                losttracks = cms.InputTag("lostTracks"),
                                #packed   = cms.InputTag("packedGenParticles"),
                                pixelhit = cms.InputTag("slimmedJets", "tagInfos", "PAT"),
                                #genJetsWnu        = cms.InputTag("ak4GenJetsWithNu"),
                                #genJets           = cms.InputTag("slimmedGenJets"),
                                jetR       = cms.double(0.4),
                                runFatJet = cms.bool(False),
                                MC = cms.bool(False),
                                eta = cms.bool(True),
                                puppi = cms.bool(True),
                                runDeepVertex = cms.bool(False),
                                pupInfo = cms.InputTag("slimmedAddPileupInfo"),
                                rhoInfo = cms.InputTag("fixedGridRhoFastjetAll"),	
                                SVs  = cms.InputTag("slimmedSecondaryVertices"),
                                LooseSVs = cms.InputTag("inclusiveCandidateSecondaryVertices"),
                                #genJetMatchWithNu = cms.InputTag("patGenJetMatchWithNu"),
                                #genJetMatchRecluster = cms.InputTag("patGenJetMatchRecluster"),
                                #genJetMatchAllowDuplicates = cms.InputTag("patGenJetMatchAllowDuplicates"),
                                #pruned = cms.InputTag("prunedGenParticles"),
                                fatjets = cms.InputTag('slimmedJetsAK8'),
                                muons = cms.InputTag("slimmedMuons"),
                                electrons = cms.InputTag("slimmedElectrons"),
                                leptonPairs  = cms.InputTag(""),
                                jetPtMin     = cms.double(10.0),
                                jetPtMax     = cms.double(2000),
                                jetAbsEtaMin = cms.double(0.0),
                                jetAbsEtaMax = cms.double(5.0),
                                gluonReduction = cms.double(0.0),
                                tagInfoName = cms.string('deepNN'),
                                tagInfoFName = cms.string('pfBoostedDoubleSVAK8'),
                                bDiscriminators = cms.vstring(),
                                qgtagger        = cms.string("QGTagger"),
                                candidates      = cms.InputTag("packedPFCandidates"),
                                minCandidatePt  = cms.double(0.1), ### Is this the pfCand cut used for PNet Run3 ? Should be increased ?###
                                useHerwigCompatible=cms.bool(False),
                                isHerwig=cms.bool(False),
                                useOffsets=cms.bool(True),
                                applySelection=cms.bool(True)
                                )
