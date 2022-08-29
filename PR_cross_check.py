'''
python3 PR_cross_check.py
'''

import os, sys

import optparse
import math

from ROOT import TCanvas, TPad, TFile, TPaveText, TLegend
from ROOT import TH1D, TH1F, TF1, TGraphErrors, TMultiGraph


# The three files are in: /afs/cern.ch/user/c/ckoraka/public/TOP-HLT-DQM/rootFiles_PR_validation
input_folder = "/afs/cern.ch/user/c/ckoraka/public/TOP-HLT-DQM/rootFiles_PR_validation/"

input_files_names = {
    "original" : input_folder + "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_REF.root",
    "wrong_PR" : input_folder + "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO_WRONG-PR.root",
    "current"  : input_folder + "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__latest-PR_Correct--I--hope.root",
}

# Open input files
input_files = {}

# Dictionaries for rootfile structures
structure = {}
sub_structure = {}
sub_sub_structure = {}

for key, value in input_files_names.items():
    print(key, '->', value)
    structure[key] = {}
    sub_structure[key] = {}
    sub_sub_structure[key] = {}
    f = TFile(value, "read")
    input_files[key] = f
    # f.SetDirectory(0)
    base_dir = "DQMData/Run 1/HLT/Run summary"
    f.cd(base_dir)
    f_keys = f.GetListOfKeys()
    for i in f_keys:
        # print(i)
        DQMData = i.ReadObj()
        # print("DQMData = ",DQMData)
        for j in DQMData.GetListOfKeys():
            Run_1 = j.ReadObj()
            # print("Run_1 = ",Run_1)
            for k in Run_1.GetListOfKeys():
                if (k.GetName() != "HLT") : continue
                HLT = k.ReadObj()
                # print("HLT = ",HLT)
                for l in HLT.GetListOfKeys():
                    Run_summary = l.ReadObj()
                    # print("Run_summary = ",Run_summary)
                    for m in Run_summary.GetListOfKeys():
                        if all(x not in m.GetName() for x in ["TOP","HIG","SUSY","Higgs","B2G"]) : continue
                        if m.GetName() == "SUSYBSM" : continue
                        if m.GetName() == "B2GHLTValidation" : continue
                        if m.GetName() == "Higgs" : continue
                        PAGs = m.ReadObj()
                        sub_structure[key][PAGs.GetName()] = {}
                        sub_sub_structure[key][PAGs.GetName()] = {}
                        # print("    PAGs = ",PAGs)
                        # Now we are in the PAGs folder. We look at each sub-folder and what we have inside.
                        # If it is a folder, we keep looking at its content. If it is a histogram, we plot it.
                        list_pag = []
                        for n in PAGs.GetListOfKeys():
                            list_pag.append(n.GetName())
                            sub_pag = n.ReadObj()
                            # print("        sub_pag = ",sub_pag)
                            structure[key][PAGs.GetName()] = list_pag
                            list_sub_pag = []
                            sub_sub_structure[key][PAGs.GetName()][sub_pag.GetName()] = {}
                            for o in sub_pag.GetListOfKeys():
                                list_sub_pag.append(o.GetName())
                                sub_sub_pag = o.ReadObj()
                                # print(key,PAGs.GetName(),sub_pag.GetName())
                                sub_structure[key][PAGs.GetName()][sub_pag.GetName()] = list_sub_pag
                                list_sub_sub_pag = []
                                # print(sub_sub_pag.IsFolder())
                                if sub_sub_pag.IsFolder() == False: continue
                                for p in sub_sub_pag.GetListOfKeys():
                                    list_sub_sub_pag.append(p.GetName())
                                    sub_sub_sub_pag = p.ReadObj()
                                    # print(key,PAGs.GetName(),sub_pag.GetName(),sub_sub_pag.GetName())
                                    sub_sub_structure[key][PAGs.GetName()][sub_pag.GetName()][sub_sub_pag.GetName()] = list_sub_sub_pag


# Check shared entries in the dictionaries
PAG = ["TOP","HIG","SUSY","B2G"]

for pag in PAG:
    print()
    print("Comparing PAG:", pag)
    print(structure["original"][pag])
    print(structure["wrong_PR"][pag])
    print(structure["current"][pag])
    print()


for pag in PAG:
    print()
    print("Comparing sub-folders in PAGs folders:", pag)
    print(sub_structure["original"][pag])
    print(sub_structure["wrong_PR"][pag])
    print(sub_structure["current"][pag])
    print()


for pag in PAG:
    print()
    print("Comparing sub_sub-folders in PAGs folders:", pag)
    print(sub_sub_structure["original"][pag])
    print(sub_sub_structure["wrong_PR"][pag])
    print(sub_sub_structure["current"][pag])
    print()

# A more general comparison
print("Structure:")
for pag in PAG:
    if structure["original"][pag] == structure["current"][pag]:
        print("{} OK".format(pag))

print("Sub_structure:")
for pag in PAG:
    if sub_structure["original"][pag] == sub_structure["current"][pag]:
        print("{} OK".format(pag))

print("Sub_sub_structure:")
for pag in PAG:
    if sub_sub_structure["original"][pag] == sub_sub_structure["current"][pag]:
        print("{} OK".format(pag))
