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
    PlotsDir = "TOP-HLT_trigEff_Ref_2018/" + str(era) + "/plots/"
    createDir(PlotsDir)

    paveCMS = r.TPaveText(0.12,0.93,0.92,0.96,"NDC");
    paveCMS.AddText("#bf{CMS Run-3}                       #bf{%lf} (13.6 TeV)"%(lumi))
    paveCMS.SetFillColor(0)
    paveCMS.SetBorderSize(0)
    paveCMS.SetTextSize(0.045)
    paveCMS.SetTextFont(42)

    inFile = r.TFile.Open(options.input)


    eff_deepCSV_Single = r.TEfficiency(inFile.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepcsv,inFile.den_deepcsv)
    eff_deepCSV_Double = r.TEfficiency(inFile.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepcsv,inFile.den_deepcsv)
    eff_deepCSV_HLT_Single = r.TEfficiency(inFile.num_HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59,inFile.den_deepcsv)
    eff_deepCSV_HLT_Double = r.TEfficiency(inFile.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94,inFile.den_deepcsv)
    eff_deepJet_Single = r.TEfficiency(inFile.num_HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59__deepjet,inFile.den_deepjet)
    eff_deepJet_Double = r.TEfficiency(inFile.num_HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_deepjet,inFile.den_deepjet)
    eff_eleJet = r.TEfficiency(inFile.num_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned,inFile.den_HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned)
    eff_eleHT = r.TEfficiency(inFile.num_HLT_Ele28_eta2p1_WPTight_Gsf_HT150,inFile.den_HLT_Ele28_eta2p1_WPTight_Gsf_HT150)

    c1 = r.TCanvas("c1", "canvas", 800, 800)
    c1.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59","l")
    eff_deepJet_Single.Draw()
    eff_deepJet_Single.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c1.SaveAs(PlotsDir+'eff_deepJet_Single.png')

    c2 = r.TCanvas("c2", "canvas", 800, 800)
    c2.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94","l")    
    eff_deepJet_Double.Draw()
    eff_deepJet_Double.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c2.SaveAs(PlotsDir+'eff_deepJet_Double.png')

    c3 = r.TCanvas("c3", "canvas", 800, 800)
    c3.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59","l")   
    eff_deepCSV_Single.Draw()
    eff_deepCSV_Single.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c3.SaveAs(PlotsDir+'eff_deepCSV_Single.png')

    c4 = r.TCanvas("c4", "canvas", 800, 800)
    c4.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94","l")   
    eff_deepCSV_Double.Draw()
    eff_deepCSV_Double.SetTitle('; Leading jet p_{T} [GeV] ; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c4.SaveAs(PlotsDir+'eff_deepCSV_Double.png')

    c5 = r.TCanvas("c5", "canvas", 800, 800)
    c5.cd()
    eff_deepCSV_Double.SetLineColor(46)
    l0 = r.TLegend(.63, .75, .89, .83)
    l0.AddEntry(eff_deepJet_Double,"DeepJet offline tagger","l")
    l0.AddEntry(eff_deepCSV_Double,"DeepCSV offline tagger","l")
    l0.SetTextSize(0.02)
    eff_deepJet_Double.Draw()
    eff_deepCSV_Double.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c5.SaveAs(PlotsDir+'eff_DoubleBtag_superimposed.png')
    
    c6 = r.TCanvas("c6", "canvas", 800, 800)
    c6.cd()
    eff_deepCSV_Single.SetLineColor(46)
    l0 = r.TLegend(.63, .75, .89, .83)
    l0.AddEntry(eff_deepJet_Single,"DeepJet offline tagger","l")
    l0.AddEntry(eff_deepCSV_Single,"DeepCSV offline tagger","l")
    l0.SetTextSize(0.02)
    eff_deepJet_Single.Draw()
    eff_deepCSV_Single.Draw('same')
    paveCMS.Draw('same')
    l0.Draw('same')
    c6.SaveAs(PlotsDir+'eff_SingleBtag_superimposed.png')

    c7 = r.TCanvas("c7", "canvas", 800, 800)
    c7.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned","l")   
    eff_eleJet.Draw()
    eff_eleJet.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c7.SaveAs(PlotsDir+'eff_eleJet.png')

    c8 = r.TCanvas("c8", "canvas", 800, 800)
    c8.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_Ele28_eta2p1_WPTight_Gsf_HT150","l")   
    eff_eleHT.Draw()
    eff_eleHT.SetTitle('; Leading electron p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c8.SaveAs(PlotsDir+'eff_eleHT.png')

    c9 = r.TCanvas("c9", "canvas", 800, 800)
    c9.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59","l")
    eff_deepCSV_HLT_Single.Draw()
    eff_deepCSV_HLT_Single.SetTitle('; Leading jet p_{T} [GeV]; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c9.SaveAs(PlotsDir+'eff_deepCSV_HLT_Single.png')

    c10 = r.TCanvas("c10", "canvas", 800, 800)
    c10.cd()
    l0 = r.TLegend(.25, .24, .89, .28)
    l0.AddEntry(eff_deepJet_Single,"HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94","l")
    eff_deepCSV_HLT_Double.Draw()
    eff_deepCSV_HLT_Double.SetTitle('; Leading jet p_{T} [GeV] ; Efficiency')
    paveCMS.Draw('same')
    l0.Draw('same')
    c10.SaveAs(PlotsDir+'eff_deepCSV_HLT_Double.png')

if __name__ == '__main__':
    options, paths = parse_arguments()
    main(options = options, paths = paths)


