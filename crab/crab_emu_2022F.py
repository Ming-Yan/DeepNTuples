import os
from CRABClient.UserUtilities import config

config = config()

config.General.requestName = 'emu_muon_2022F_v2'
config.General.workArea = 'crab_projects'
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../DeepNtuplizer/production/DeepNtuplizer_Domain.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2500
config.JobType.numCores    = 1

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

config.Data.inputDataset = "/Muon/Run2022F-22Sep2023-v2/MINIAOD"
config.Data.outLFNDirBase = "/store/user/ademoor/"
config.Data.outputDatasetTag = "part_2024"
config.Data.inputDBS = "global"
config.Data.publishDBS = "phys03"
config.Data.splitting = "LumiBased"
config.Data.publication = True
config.Data.ignoreLocality = False
config.Data.unitsPerJob = 50
config.JobType.maxJobRuntimeMin = 2750
config.Data.lumiMask = '../json/Cert_Collisions2022_355100_362760_Golden.json'

config.Site.storageSite = "T2_BE_IIHE"
config.Site.whitelist = ["T2_*","T3_*"]
config.Site.blacklist = ["T2_BR_UERJ"]

print("Done :)")