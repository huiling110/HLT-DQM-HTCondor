import glob
import os
import json
import sys
import time
import csv
import math as m
import numpy as np
import ROOT as r

r.gROOT.SetBatch(True)

from optparse import OptionParser

def parse_arguments():
    usage = """ 
    usage: %prog [options] Calculates expected pseudosignificance
    """

    parser = OptionParser(usage=usage)

    parser.add_option(  "-l", "--List",
                        help="""List of input root files""",
                        dest = "List",
                        default = "filelist_Fill8136_Muon.txt"
                    )

    parser.add_option(  "-f", "--Fill",
                        help="""Fill number""",
                        dest = "Fill",
                        default = 8136.
                    )

    (options, args) = parser.parse_args()
    return options, args

def printProgBar(percent):
    bar = " "
    for i in range(0,50):
        if( i < (percent/2)):
            bar = bar[:len(bar)-1]+'='
        else:
            bar = bar[:len(bar)-1]+'>'
    sys.stdout.write('\r')
    sys.stdout.write('[')
    sys.stdout.write(bar)
    sys.stdout.write('] ')
    sys.stdout.write(str(percent))
    sys.stdout.write('%     ')
    sys.stdout.flush()

def main(options, paths):

    r.gStyle.SetOptStat(0)
    fill = options.Fill
    era = 2022

    binning =  np.array((0.,5.,10.,15.,20.,25.,30.,35.,40.,45.,50.,55.,60.,65.,70.,75.,80.,90.,100.,120.,140.,160.,200.))
    binning_e = np.array((0.,25.,30.,32.5,35.,40.,45.,50.,60.,80.,120.,200.,400.))

    # HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59 & HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94
    ## vs leading jet pT
    ### Use the deepCSV score to select offline jets & deepJet HLT path
    h_num_deepCSV_Single = r.TH1F("h_num_deepCSV_Single",";Leading jet p_{T};Entries",len(binning)-1,binning)
    h_num_deepCSV_Double = r.TH1F("h_num_deepCSV_Double",";Leading jet p_{T};Entries",len(binning)-1,binning)
    h_den_deepCSV = r.TH1F("h_den_deepCSV",";Leading jet p_{T};Entries",len(binning)-1,binning)
    ### Use the deepCSV score to select offline jets & deepCSV HLT path
    h_num_deepCSV_HLT_Single = r.TH1F("h_num_deepCSV_HLT_Single",";Leading jet p_{T};Entries",len(binning)-1,binning)
    h_num_deepCSV_HLT_Double = r.TH1F("h_num_deepCSV_HLT_Double",";Leading jet p_{T};Entries",len(binning)-1,binning)
    ### Use the deepJet score to select offline jets & check deepJet paths
    h_num_deepJet_Single = r.TH1F("h_num_deepJet_Single",";Leading jet p_{T};Entries",len(binning)-1,binning)
    h_num_deepJet_Double = r.TH1F("h_num_deepJet_Double",";Leading jet p_{T};Entries",len(binning)-1,binning)
    h_den_deepJet = r.TH1F("h_den_deepJet",";Leading jet p_{T};Entries",len(binning)-1,binning)

    ## vs offline b-tag score
    ### Use the deepJet score & check the deepCSV path    
    h_num_deepCSV_HLT_Single_csv = r.TH1F("h_num_deepCSV_HLT_Single_csv",";Offline b-tag value;Entries",10,0.,1.)
    h_num_deepCSV_HLT_Double_csv = r.TH1F("h_num_deepCSV_HLT_Double_csv",";Offline b-tag value;Entries",10,0.,1.)
    ### Use the deepJet score & check the deepJet path
    h_num_deepJet_Single_csv = r.TH1F("h_num_deepJet_Single_csv",";Offline b-tag value;Entries",10,0.,1.)
    h_num_deepJet_Double_csv = r.TH1F("h_num_deepJet_Double_csv",";Offline b-tag value;Entries",10,0.,1.)
    h_den_deepJet_csv = r.TH1F("h_den_deepJet_csv",";Offline b-tag value;Entries",10,0.,1.)


    # HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned
    h_num_eleJet = r.TH1F("h_num_eleJet",";Leading electron p_{T};Entries",len(binning_e)-1,binning_e)
    h_den_eleJet = r.TH1F("h_den_eleJet",";Leading electron p_{T};Entries",len(binning_e)-1,binning_e)

    # HLT_Ele28_eta2p1_WPTight_Gsf_HT150
    h_num_eleHT = r.TH1F("h_num_eleHT",";Leading electron p_{T};Entries",len(binning_e)-1,binning_e)
    h_den_eleHT = r.TH1F("h_den_eleHT",";Leading electron p_{T};Entries",len(binning_e)-1,binning_e)

    print('------ Running over files ------')
    chain = r.TChain("Events")
    print("Adding file: ",options.List)
    chain.AddFile(options.List)
    entries = int(chain.GetEntries())
    print('entries :',entries)
    entry = 0
    # for event in chain:
    for entry in range(1000):
        chain.GetEntry(entry) 
        # Progress bar
        # if(((entry+1)%(5*entries/100))==0):
        #     printProgBar(100*entry/entries +1)
        # if (entry == entries-1):
        #     printProgBar(100)
        # entry = entry + 1

        HT = 0 # Event HT using jet pT cut for b-jet HLT paths
        nb = 0 # Number of offline b-tagged jets using deepJet score
        nj = 0 # Using jet pT cut for b-jet HLT paths
        nb_csv = 0 # Number of offline b-tagged jets using deepCSV score
        nj_ele = 0 # Using jet pT cut for electron HLT paths
        ne = 0 # Number of electrons

        #if(chain.run<360459):
        #    continue

        if((chain.HLT_IsoMu27==1) & (chain.nJet>5)):
            for jet in range(0,chain.nJet):
                # chain HT
                if((chain.Jet_pt[jet] > 30.) & (abs(chain.Jet_eta[jet])<2.4)): 
                    HT = HT + chain.Jet_pt[jet]
                # nJets
                if((chain.Jet_pt[jet] > 40.) & (abs(chain.Jet_eta[jet])<2.4) ):
                    nj = nj+1
                # nBjets
                if((chain.Jet_pt[jet] > 40.) & (abs(chain.Jet_eta[jet])<2.4) & (chain.Jet_btagDeepFlavB[jet]>0.2770)):
                    nb = nb+1
                # if((chain.Jet_pt[jet] > 40.) & (abs(chain.Jet_eta[jet])<2.4) & (chain.Jet_btagDeepB[jet]>0.4941)):##!!!
                    # nb_csv = nb_csv+1

            # b-jet paths   
            if((nj > 5)  & (nb>1) & (HT>500) & (chain.HLT_IsoMu27==1)):
                h_den_deepJet.Fill(chain.Jet_pt[0],1.)

                # DeepJet with DeepJet tagger offline
                if(chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59==1):
                    h_num_deepJet_Single.Fill(chain.Jet_pt[0],1.)
                if(chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94==1):
                    h_num_deepJet_Double.Fill(chain.Jet_pt[0],1.)

                # DeepCSV with DeepJet tagger offline 
                if(chain.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59==1):
                    h_num_deepCSV_HLT_Single.Fill(chain.Jet_pt[0],1.)
                if(chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94==1):
                    h_num_deepCSV_HLT_Double.Fill(chain.Jet_pt[0],1.)

                # Plots according to BTV PAG
                if(chain.HLT_PFHT400_SixPFJet32>-1):
                    maxBtag = max(chain.Jet_btagDeepFlavB)
                    h_den_deepJet_csv.Fill(maxBtag,1.)
                    if(chain.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59==1):
                        h_num_deepCSV_HLT_Single_csv.Fill(maxBtag,1.)
                    if(chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94==1):
                        h_num_deepCSV_HLT_Double_csv.Fill(maxBtag,1.)
                    if(chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59==1):
                        h_num_deepJet_Single_csv.Fill(maxBtag,1.)
                    if(chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94==1):
                        h_num_deepJet_Double_csv.Fill(maxBtag,1.)

            # DeepJet with DeepCSV tagger offline 
            if((nj > 5)  & (nb_csv>1) & (HT>500) & (chain.HLT_IsoMu27==1)):
                h_den_deepCSV.Fill(chain.Jet_pt[0],1.)
                if(chain.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59==1):
                    h_num_deepCSV_Single.Fill(chain.Jet_pt[0],1.)
                if(chain.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94==1):
                    h_num_deepCSV_Double.Fill(chain.Jet_pt[0],1.)
              

        if((chain.nJet>0)):
            for jet in range(0,chain.nJet):
                # nJets ele paths
                if((chain.Jet_pt[jet] > 30.) & (abs(chain.Jet_eta[jet])<2.4) ):
                    nj_ele = nj_ele+1     
            for electron in range(0,chain.nElectron):
                # nElectrons
                if((chain.Electron_pt[electron] > 25.) & (abs(chain.Electron_eta[electron])<2.1) & (chain.Electron_cutBased[electron]==4)):
                    ne = ne+1
            # ele+jet path
            if((nj_ele > 0) & (ne>0)):
                h_den_eleJet.Fill(chain.Electron_pt[0],1.)
                if(chain.HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned==1):
                    h_num_eleJet.Fill(chain.Electron_pt[0],1.)

            # ele+HT path
            if((nj_ele > 1) & (ne>0) & (HT>100.) ):
                h_den_eleHT.Fill(chain.Electron_pt[0],1.)
                if(chain.HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1):
                    h_num_eleHT.Fill(chain.Electron_pt[0],1.)

    # Efficiency calculation
    eff_deepCSV_Single = r.TEfficiency(h_num_deepCSV_Single,h_den_deepCSV)
    eff_deepCSV_Double = r.TEfficiency(h_num_deepCSV_Double,h_den_deepCSV)
    eff_deepJet_Single = r.TEfficiency(h_num_deepJet_Single,h_den_deepJet)
    eff_deepJet_Double = r.TEfficiency(h_num_deepJet_Double,h_den_deepJet)
    eff_deepCSV_HLT_Single = r.TEfficiency(h_num_deepCSV_HLT_Single,h_den_deepCSV)
    eff_deepCSV_HLT_Double = r.TEfficiency(h_num_deepCSV_HLT_Double,h_den_deepCSV)
    eff_deepCSV_HLT_Single_csv = r.TEfficiency(h_num_deepCSV_HLT_Single_csv,h_den_deepJet_csv)    
    eff_deepCSV_HLT_Double_csv = r.TEfficiency(h_num_deepCSV_HLT_Double_csv,h_den_deepJet_csv)
    eff_deepJet_HLT_Single_csv = r.TEfficiency(h_num_deepJet_Single_csv,h_den_deepJet_csv)
    eff_deepJet_HLT_Double_csv = r.TEfficiency(h_num_deepJet_Double_csv,h_den_deepJet_csv)
    eff_eleJet = r.TEfficiency(h_num_eleJet,h_den_eleJet)
    eff_eleHT = r.TEfficiency(h_num_eleHT,h_den_eleHT)

    paveCMS = r.TPaveText(0.12,0.93,0.92,0.96,"NDC");
    paveCMS.AddText("#bf{CMS Run-3}                       #bf{Fill %d} (13.6 TeV)"%(int(fill)))
    paveCMS.SetFillColor(0)
    paveCMS.SetBorderSize(0)
    paveCMS.SetTextSize(0.045)
    paveCMS.SetTextFont(42)

    myfile = r.TFile('Efficiency_hists.root', 'RECREATE' )
    
    h_num_deepCSV_Single.SetName('num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv')
    h_num_deepCSV_Single.Write()
    h_num_deepCSV_Double.SetName('num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv')
    h_num_deepCSV_Double.Write()
    h_num_deepCSV_HLT_Single.SetName('num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59')
    h_num_deepCSV_HLT_Single.Write()
    h_num_deepCSV_HLT_Double.SetName('num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94')
    h_num_deepCSV_HLT_Double.Write()
    h_den_deepCSV.SetName('den_deepcsv')
    h_den_deepCSV.Write()
    h_num_deepJet_Single.SetName('num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet')
    h_num_deepJet_Single.Write()
    h_num_deepJet_Double.SetName('num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet')
    h_num_deepJet_Double.Write() 
    h_den_deepJet.SetName('den_deepjet')
    h_den_deepJet.Write()     
    h_num_eleJet.SetName('num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned')
    h_num_eleJet.Write()
    h_den_eleJet.SetName('den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned')
    h_den_eleJet.Write()
    h_num_eleHT.SetName('num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150')
    h_num_eleHT.Write()
    h_den_eleHT.SetName('den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150')
    h_den_eleHT.Write()

    h_num_deepCSV_HLT_Single_csv.SetName('num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_deepjetCSV')
    h_num_deepCSV_HLT_Single_csv.Write()
    h_num_deepJet_Single_csv.SetName('num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59_deepjetCSV')
    h_num_deepJet_Single_csv.Write()
    h_num_deepCSV_HLT_Double_csv.SetName('num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_deepjetCSV')
    h_num_deepCSV_HLT_Double_csv.Write()
    h_num_deepJet_Double_csv.SetName('num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjetCSV')
    h_num_deepJet_Double_csv.Write()
    h_den_deepJet_csv.SetName('den_deepjetCSV')
    h_den_deepJet_csv.Write()

    eff_deepCSV_Single.SetName('eff_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv')
    eff_deepCSV_Single.Write()
    eff_deepCSV_Double.SetName('eff_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv')
    eff_deepCSV_Double.Write()
    eff_deepJet_Single.SetName('eff_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet')
    eff_deepJet_Single.Write()
    eff_deepJet_Double.SetName('eff_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet')
    eff_deepJet_Double.Write()
    eff_deepCSV_HLT_Single.SetName('eff_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59')
    eff_deepCSV_HLT_Single.Write()
    eff_deepCSV_HLT_Double.SetName('eff_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94')
    eff_deepCSV_HLT_Double.Write()
    eff_eleJet.SetName('eff_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned')
    eff_eleJet.Write()
    eff_eleHT.SetName('eff_HLT_Ele28_eta2p1_WPTight_Gsf_HT150')
    eff_eleHT.Write()
    eff_deepCSV_HLT_Single_csv.SetName('eff_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_deepJetCSV')
    eff_deepCSV_HLT_Single_csv.Write()
    eff_deepJet_HLT_Single_csv.SetName('eff_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59_deepJetCSV')
    eff_deepJet_HLT_Single_csv.Write()
    eff_deepCSV_HLT_Double_csv.SetName('eff_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_deepJetCSV')
    eff_deepCSV_HLT_Double_csv.Write()
    eff_deepJet_HLT_Double_csv.SetName('eff_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepJetCSV')
    eff_deepJet_HLT_Double_csv.Write()


if __name__ == '__main__':
    options, paths = parse_arguments()
    main(options = options, paths = paths)


