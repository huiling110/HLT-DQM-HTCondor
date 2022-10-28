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

    parser.add_option(  "-i", "--input",
                        help="""Input root file with histos""",
                        dest = "input",
                        default = "input.root"
                    )

    parser.add_option(  "-f", "--Lumi",
                        help="""Luminosity""",
                        dest = "Lumi",
                        default = 1.
                    )

    (options, args) = parser.parse_args()
    return options, args

def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main(options, paths):

    r.gStyle.SetOptStat(0)
 
    lumi = options.Lumi
    era = 2022
    PlotsDir = "TOP-HLT_trigEff_all/" + str(era) + "/plots/"
    createDir(PlotsDir)

    paveCMS = r.TPaveText(0.05,0.93,0.95,0.95,"NDC");
    paveCMS.AddText("#bf{CMS Run-3} #it{Preliminary 2022}   4.5/fb + 1.4/fb + 4.8/fb + 1.5/fb (13.6 TeV)")
    paveCMS.SetFillColor(0)
    paveCMS.SetBorderSize(0)
    paveCMS.SetTextSize(0.03)
    paveCMS.SetTextFont(42)


    inFileRunC = r.TFile.Open("public/TOP-HLT-DQM/efficiencyNanoAOD/Efficiency2022/Efficiency_hists_SingleMuon_2022_RunC.root")
    inFileRunD = r.TFile.Open("public/TOP-HLT-DQM/efficiencyNanoAOD/Efficiency2022/Efficiency_hists_Muon_2022_RunD.root")
    inFileRunE = r.TFile.Open("public/TOP-HLT-DQM/efficiencyNanoAOD/Efficiency2022/Efficiency_hists_Muon_2022_RunE.root")
    inFileRunF = r.TFile.Open("public/TOP-HLT-DQM/efficiencyNanoAOD/Efficiency2022/Efficiency_hists_Muon_2022_RunF_Exclude360442.root")
    inFileRef = r.TFile.Open("public/TOP-HLT-DQM/efficiencyNanoAOD/Efficiency2022/Efficiency_hists_Reference2018.root")

    eff_deepCSV_Single_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFileRunC.den_deepcsv)
    eff_deepCSV_Double_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFileRunC.den_deepcsv)
    eff_deepCSV_HLT_Single_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFileRunC.den_deepcsv)
    eff_deepCSV_HLT_Double_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFileRunC.den_deepcsv)
    eff_deepJet_Single_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFileRunC.den_deepjet)
    eff_deepJet_Double_RunC = r.TEfficiency(inFileRunC.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFileRunC.den_deepjet)
    eff_eleJet_RunC = r.TEfficiency(inFileRunC.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFileRunC.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT_RunC = r.TEfficiency(inFileRunC.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFileRunC.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)

    eff_deepCSV_Single_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFileRunD.den_deepcsv)
    eff_deepCSV_Double_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFileRunD.den_deepcsv)
    eff_deepCSV_HLT_Single_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFileRunD.den_deepcsv)
    eff_deepCSV_HLT_Double_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFileRunD.den_deepcsv)
    eff_deepJet_Single_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFileRunD.den_deepjet)
    eff_deepJet_Double_RunD = r.TEfficiency(inFileRunD.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFileRunD.den_deepjet)
    eff_eleJet_RunD = r.TEfficiency(inFileRunD.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFileRunD.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT_RunD = r.TEfficiency(inFileRunD.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFileRunD.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)

    eff_deepCSV_Single_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFileRunE.den_deepcsv)
    eff_deepCSV_Double_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFileRunE.den_deepcsv)
    eff_deepCSV_HLT_Single_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFileRunE.den_deepcsv)
    eff_deepCSV_HLT_Double_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFileRunE.den_deepcsv)
    eff_deepJet_Single_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFileRunE.den_deepjet)
    eff_deepJet_Double_RunE = r.TEfficiency(inFileRunE.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFileRunE.den_deepjet)
    eff_eleJet_RunE = r.TEfficiency(inFileRunE.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFileRunE.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT_RunE = r.TEfficiency(inFileRunE.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFileRunE.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)

    eff_deepCSV_Single_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFileRunF.den_deepcsv)
    eff_deepCSV_Double_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFileRunF.den_deepcsv)
    eff_deepCSV_HLT_Single_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFileRunF.den_deepcsv)
    eff_deepCSV_HLT_Double_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFileRunF.den_deepcsv)
    eff_deepJet_Single_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFileRunF.den_deepjet)
    eff_deepJet_Double_RunF = r.TEfficiency(inFileRunF.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFileRunF.den_deepjet)
    eff_eleJet_RunF = r.TEfficiency(inFileRunF.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFileRunF.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT_RunF = r.TEfficiency(inFileRunF.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFileRunF.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)

    eff_deepCSV_Single_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFileRef.den_deepcsv)
    eff_deepCSV_Double_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFileRef.den_deepcsv)
    eff_deepCSV_HLT_Single_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFileRef.den_deepcsv)
    eff_deepCSV_HLT_Double_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFileRef.den_deepcsv)
    eff_deepJet_Single_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFileRef.den_deepjet)
    eff_deepJet_Double_Ref = r.TEfficiency(inFileRef.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFileRef.den_deepjet)
    eff_eleJet_Ref = r.TEfficiency(inFileRef.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFileRef.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT_Ref = r.TEfficiency(inFileRef.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFileRef.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)


    c5 = r.TCanvas("c5", "canvas", 800, 800)
    c5.cd()
    eff_deepCSV_HLT_Single_Ref.SetLineColor(r.kBlue)
    eff_deepJet_Single_RunD.SetLineColor(r.kRed)
    eff_deepJet_Single_RunE.SetLineColor(r.kGreen+2)
    eff_deepJet_Single_RunF.SetLineColor(r.kMagenta+2)
    eff_deepJet_Single_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.5, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Single_RunC,"2022 RunC","l")
    l0.AddEntry(eff_deepJet_Single_RunD,"2022 RunD","l")
    l0.AddEntry(eff_deepJet_Single_RunE,"2022 RunE","l")
    l0.AddEntry(eff_deepJet_Single_RunF,"2022 RunF","l")
    l0.AddEntry(eff_deepCSV_HLT_Single_Ref,"Run 325100 - 2018 RunD","l")
    eff_deepJet_Single_RunC.Draw()
    eff_deepJet_Single_RunD.Draw('same')
    eff_deepJet_Single_RunE.Draw('same')
    eff_deepJet_Single_RunF.Draw('same')
    eff_deepCSV_HLT_Single_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c5.SaveAs(PlotsDir+'eff_SingleB_Run3_vs_Run2.png')

    c6 = r.TCanvas("c6", "canvas", 800, 800)
    c6.cd()
    eff_deepCSV_HLT_Double_Ref.SetLineColor(r.kBlue)
    eff_deepJet_Double_RunD.SetLineColor(r.kRed)
    eff_deepJet_Double_RunE.SetLineColor(r.kGreen+2)
    eff_deepJet_Double_RunF.SetLineColor(r.kMagenta+2)
    eff_deepJet_Double_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.5, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Double_RunC,"2022 RunC","l")
    l0.AddEntry(eff_deepJet_Double_RunD,"2022 RunD","l")
    l0.AddEntry(eff_deepJet_Double_RunE,"2022 RunE","l")
    l0.AddEntry(eff_deepJet_Double_RunF,"2022 RunF","l")
    l0.AddEntry(eff_deepCSV_HLT_Double_Ref,"Run 325100 - 2018 RunD","l")
    eff_deepJet_Double_RunC.Draw()
    eff_deepJet_Double_RunD.Draw('same')
    eff_deepJet_Double_RunE.Draw('same')
    eff_deepJet_Double_RunF.Draw('same')
    eff_deepCSV_HLT_Double_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c6.SaveAs(PlotsDir+'eff_DoubleB_Run3_vs_Run2.png')

    c7 = r.TCanvas("c7", "canvas", 800, 800)
    c7.cd()
    eff_eleJet_Ref.SetLineColor(r.kBlue)
    eff_eleJet_RunD.SetLineColor(r.kRed)
    eff_eleJet_RunE.SetLineColor(r.kGreen+2)
    eff_eleJet_RunF.SetLineColor(r.kMagenta+2)
    eff_eleJet_RunC.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.5, .12, .89, .24)
    l0.AddEntry(eff_eleJet_RunC,"2022 RunC","l")
    l0.AddEntry(eff_eleJet_RunD,"2022 RunD","l")
    l0.AddEntry(eff_eleJet_RunE,"2022 RunE","l")
    l0.AddEntry(eff_eleJet_RunF,"2022 RunF","l")
    l0.AddEntry(eff_eleJet_Ref,"Run 325100 - 2018 RunD","l")
    eff_eleJet_RunC.Draw()
    eff_eleJet_RunD.Draw('same')
    eff_eleJet_RunE.Draw('same')
    eff_eleJet_RunF.Draw('same')
    eff_eleJet_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c7.SaveAs(PlotsDir+'eff_eleJet_Run3_vs_Run2.png')


    c8 = r.TCanvas("c8", "canvas", 800, 800)
    c8.cd()
    eff_eleHT_Ref.SetLineColor(r.kBlue)
    eff_eleHT_RunD.SetLineColor(r.kRed)
    eff_eleHT_RunE.SetLineColor(r.kGreen+2)
    eff_eleHT_RunF.SetLineColor(r.kMagenta+2)
    eff_eleHT_RunC.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.5, .12, .89, .24)
    l0.AddEntry(eff_eleHT_RunC,"2022 RunC","l")
    l0.AddEntry(eff_eleHT_RunD,"2022 RunD","l")
    l0.AddEntry(eff_eleHT_RunE,"2022 RunE","l")
    l0.AddEntry(eff_eleHT_RunF,"2022 RunF","l")
    l0.AddEntry(eff_eleHT_Ref,"Run 325100 - 2018 RunD","l")
    eff_eleHT_RunC.Draw()
    eff_eleHT_RunD.Draw('same')
    eff_eleHT_RunE.Draw('same')
    eff_eleHT_RunF.Draw('same')
    eff_eleHT_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c8.SaveAs(PlotsDir+'eff_eleHT_Run3_vs_Run2.png')

if __name__ == '__main__':
    options, paths = parse_arguments()
    main(options = options, paths = paths)