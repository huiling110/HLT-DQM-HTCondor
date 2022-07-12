Add at the beginning of step0.py:

    from filelist import *

and then change :

    input = cms.untracked.int32(-1)

    fileNames = cms.untracked.vstring(filelist),


# In step1.py, change:
    
#    fileNames = cms.untracked.vstring('file:step0_HLT.root'),


The list of files is in the file `list`. Since each file would require high computing and disk resources, we split the list to have one file processed per job. Run the split_one.sh macro to split this in subfiles of 1 file each:

    bash split_one.sh

It creates several subfiles named `filelist.py.XXX`.

Now, update the `hlt_efficiency.sh` script with the correct local paths and the path to the grid certificate in hlt_efficiency.sub.

Then submit the jobs:

    condor_submit hlt_efficiency.sub

One all the jobs are done, merge the output files in:

    /eos/user/n/ntrevisa/DQM_HLT/

To merge them, use the `MULTIRUN_HARVESTING.py` script. Create a python list with the output files into the `step4_list.py` file. Then, import the list into `MULTIRUN_HARVESTING.py` by adding the line:

    from step4_list import *

Modify then the line in `process.source` to:

    fileNames = cms.untracked.vstring(step4_list),

Run the `MULTIRUN_HARVESTING.py` script:

    cmsRun MULTIRUN_HARVESTING.py


Original files in:

    /afs/cern.ch/user/c/ckoraka/public/TOP-HLT-DQM
