#!/usr/bin/env python

import ROOT

# Get material map hist from file
f1 = ROOT.TFile.Open("Material_Map_HIST.root")
map_d = f1.Get("material_map")
f1.Close()

# make dataframe from ntuple
df = ROOT.RDataFrame("Events", "NanoAOD_1.root")

