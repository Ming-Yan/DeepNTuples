
#!/bin/sh
#
#(make sure the right shell will be used)
#$ -S /bin/sh
#$ -l site=hh
#$ -l distro=sld6
#
#(the cpu time for this job)
#$ -l h_rt=05:55:00
#
#(the maximum memory usage of this job)
#$ -l h_vmem=4096M
#$ -l cvmfs
#(stderr and stdout are merged together to stdout)
#$ -j y
#$ -m a
#$ -cwd -V
#( -l h_stack=1536M) #try with small stack
#$ -pe local 1 -R y
#$ -P af-cms

export LOGDIR=/afs/cern.ch/work/a/ademoor/New_Tagger_Dev/CMSSW_10_6_30/src/DeepNTuples/test_ParTEdge_small/ntuple_ttbar_had/batch/
export JOB=3
export NTUPLEOUTFILEPATH=/eos/cms/store/group/phys_btag/ParticleTransformer/JustATest/Wed_110513_test_ParTEdge_small/ntuple_ttbar_had/output/ntuple_ttbar_had_3.root

/afs/cern.ch/work/a/ademoor/New_Tagger_Dev/CMSSW_10_6_30/src/DeepNTuples/test_ParTEdge_small/ntuple_ttbar_had/batchscript.sh /afs/cern.ch/work/a/ademoor/New_Tagger_Dev/CMSSW_10_6_30/src/DeepNTuples/test_ParTEdge_small/DeepNtuplizer.py inputScript=TTToHadronicTuneCP513TeVpowhegpythia8RunIISummer20UL18MiniAOD106Xupgrade2018realisticv11L1v1v2MINIAODSIM nJobs=5 job=3 
            