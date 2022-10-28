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

    paveCMS = r.TPaveText(0.1,0.93,0.92,0.95,"NDC");
    paveCMS.AddText("#bf{CMS Run-3}  #it{Preliminary 2022}          4.5 fb^{-1} + 2.8 fb^{-1} (13.6 TeV)")
    paveCMS.SetFillColor(0)
    paveCMS.SetBorderSize(0)
    paveCMS.SetTextSize(0.032)
    paveCMS.SetTextFont(42)


    inFileRunC = r.TFile.Open("Efficiency_hists_SingleMuon_2022_RunC.root")
    inFileRunD = r.TFile.Open("Efficiency_hists_Muon_2022_RunD.root")
    inFileRef = r.TFile.Open("Efficiency_hists_Reference2018.root")

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
    eff_deepJet_Single_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Single_RunC,"2022 RunC","l")
    l0.AddEntry(eff_deepJet_Single_RunD,"2022 RunD","l")
    l0.AddEntry(eff_deepCSV_HLT_Single_Ref,"Run 325100 - 2018 RunD","l")
    eff_deepJet_Single_RunC.Draw()
    eff_deepJet_Single_RunD.Draw('same')
    eff_deepCSV_HLT_Single_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c5.SaveAs(PlotsDir+'eff_SingleB_Run3_vs_Run2.png')

    c6 = r.TCanvas("c6", "canvas", 800, 800)
    c6.cd()
    eff_deepCSV_HLT_Double_Ref.SetLineColor(r.kBlue)
    eff_deepJet_Double_RunD.SetLineColor(r.kRed)
    eff_deepJet_Double_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Double_RunC,"2022 RunC","l")
    l0.AddEntry(eff_deepJet_Double_RunD,"2022 RunD","l")
    l0.AddEntry(eff_deepCSV_HLT_Double_Ref,"Run 325100 - 2018 RunD","l")
    eff_deepJet_Double_RunC.Draw()
    eff_deepJet_Double_RunD.Draw('same')
    eff_deepCSV_HLT_Double_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c6.SaveAs(PlotsDir+'eff_DoubleB_Run3_vs_Run2.png')

    c7 = r.TCanvas("c7", "canvas", 800, 800)
    c7.cd()
    eff_eleJet_Ref.SetLineColor(r.kBlue)
    eff_eleJet_RunD.SetLineColor(r.kRed)
    eff_eleJet_RunC.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_eleJet_RunC,"2022 RunC","l")
    l0.AddEntry(eff_eleJet_RunD,"2022 RunD","l")
    l0.AddEntry(eff_eleJet_Ref,"Run 325100 - 2018 RunD","l")
    eff_eleJet_RunC.Draw()
    eff_eleJet_RunD.Draw('same')
    eff_eleJet_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c7.SaveAs(PlotsDir+'eff_eleJet_Run3_vs_Run2.png')


    c8 = r.TCanvas("c8", "canvas", 800, 800)
    c8.cd()
    eff_eleHT_Ref.SetLineColor(r.kBlue)
    eff_eleHT_RunD.SetLineColor(r.kRed)
    eff_eleHT_RunC.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_eleHT_RunC,"2022 RunC","l")
    l0.AddEntry(eff_eleHT_RunD,"2022 RunD","l")
    l0.AddEntry(eff_eleHT_Ref,"Run 325100 - 2018 RunD","l")
    eff_eleHT_RunC.Draw()
    eff_eleHT_RunD.Draw('same')
    eff_eleHT_Ref.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c8.SaveAs(PlotsDir+'eff_eleHT_Run3_vs_Run2.png')

    c1 = r.TCanvas("c1", "canvas", 800, 800)
    c1.cd()
    paveCMS.Clear()
    paveCMS.AddText("#bf{CMS Run-3}  #it{Preliminary 2022}          RunC 4.5 fb^{-1} (13.6 TeV)")
    eff_deepCSV_HLT_Single_RunC.SetLineColor(r.kBlue)
    eff_deepCSV_Single_RunC.SetLineColor(r.kRed)
    eff_deepJet_Single_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Single_RunC,"DeepJet path + offline b-jets with deepJet","l")
    l0.AddEntry(eff_deepCSV_Single_RunC,"DeepJet path + offline b-jets with deepCSV","l")
    l0.AddEntry(eff_deepCSV_HLT_Single_RunC,"DeepCSV path + offline b-jets with deepCSV","l")
    eff_deepJet_Single_RunC.Draw()
    eff_deepCSV_Single_RunC.Draw('same')
    eff_deepCSV_HLT_Single_RunC.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c1.SaveAs(PlotsDir+'eff_SingleB_RunC_2022.png')

    c2 = r.TCanvas("c2", "canvas", 800, 800)
    c2.cd()
    paveCMS.Clear()
    paveCMS.AddText("#bf{CMS Run-3}  #it{Preliminary 2022}          RunD 2.8 fb^{-1} (13.6 TeV)")
    eff_deepCSV_HLT_Single_RunD.SetLineColor(r.kBlue)
    eff_deepCSV_Single_RunD.SetLineColor(r.kRed)
    eff_deepJet_Single_RunD.SetLineColor(r.kBlack)
    eff_deepJet_Single_RunD.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Single_RunD,"DeepJet path + offline b-jets with deepJet","l")
    l0.AddEntry(eff_deepCSV_Single_RunD,"DeepJet path + offline b-jets with deepCSV","l")
    l0.AddEntry(eff_deepCSV_HLT_Single_RunD,"DeepCSV path + offline b-jets with deepCSV","l")
    eff_deepJet_Single_RunD.Draw()
    eff_deepCSV_Single_RunD.Draw('same')
    eff_deepCSV_HLT_Single_RunD.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c2.SaveAs(PlotsDir+'eff_SingleB_RunD_2022.png')


    c3 = r.TCanvas("c3", "canvas", 800, 800)
    c3.cd()
    paveCMS.Clear()
    paveCMS.AddText("#bf{CMS Run-3}  #it{Preliminary 2022}          RunC 4.5 fb^{-1} (13.6 TeV)")
    eff_deepCSV_HLT_Double_RunC.SetLineColor(r.kBlue)
    eff_deepCSV_Double_RunC.SetLineColor(r.kRed)
    eff_deepJet_Double_RunC.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Double_RunC,"DeepJet path + offline b-jets with deepJet","l")
    l0.AddEntry(eff_deepCSV_Double_RunC,"DeepJet path + offline b-jets with deepCSV","l")
    l0.AddEntry(eff_deepCSV_HLT_Double_RunC,"DeepCSV path + offline b-jets with deepCSV","l")
    eff_deepJet_Double_RunC.Draw()
    eff_deepCSV_Double_RunC.Draw('same')
    eff_deepCSV_HLT_Double_RunC.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c3.SaveAs(PlotsDir+'eff_DoubleB_RunC_2022.png')

    c4 = r.TCanvas("c4", "canvas", 800, 800)
    c4.cd()
    paveCMS.Clear()
    paveCMS.AddText("#bf{CMS Run-3}  #it{Preliminary 2022}          RunD 2.8 fb^{-1} (13.6 TeV)")
    eff_deepCSV_HLT_Double_RunD.SetLineColor(r.kBlue)
    eff_deepCSV_Double_RunD.SetLineColor(r.kRed)
    eff_deepJet_Double_RunD.SetLineColor(r.kBlack)
    eff_deepJet_Double_RunD.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    l0 = r.TLegend(.4, .12, .89, .24)
    l0.AddEntry(eff_deepJet_Double_RunD,"DeepJet path + offline b-jets with deepJet","l")
    l0.AddEntry(eff_deepCSV_Double_RunD,"DeepJet path + offline b-jets with deepCSV","l")
    l0.AddEntry(eff_deepCSV_HLT_Double_RunD,"DeepCSV path + offline b-jets with deepCSV","l")
    eff_deepJet_Double_RunD.Draw()
    eff_deepCSV_Double_RunD.Draw('same')
    eff_deepCSV_HLT_Double_RunD.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c4.SaveAs(PlotsDir+'eff_DoubleB_RunD_2022.png')

if __name__ == '__main__':
    options, paths = parse_arguments()
    main(options = options, paths = paths)


