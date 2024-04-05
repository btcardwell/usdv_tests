#!/usr/bin/env python

import ROOT

# make dataframe from ntuple
df = ROOT.RDataFrame("Events", "NanoAOD_1.root")
df = df.Range(10) # only look at first 10 events while testing
#print(df.Count().GetValue())

# print columns that contain 'SV'
#[print(c) for c in df.GetColumnNames() if "SV" in str(c)]

# define new test column
df = df.Define("test", "5")
#df.Display("test").Print()

# define new test column that takes df info as inputs
df = df.Define("five_times_SV_x", "5*SV_x")
#df.Display("five_times_SV_x").Print()

# allow access to material hist from df following https://root-forum.cern.ch/t/define-new-rdataframe-column-using-values-from-th1f-in-pyroot/34052
# I suppose it just looks for an object named 'material_map' in the currently open file
f1 = ROOT.TFile.Open("Material_Map_HIST.root")
ROOT.gInterpreter.ProcessLine("auto material_hist = material_map;")
#f1.Close()

# define new test column that takes material_hist info as input
df = df.Define("material_hist_nEntries", "material_hist->GetEntries()")
#df.Display("material_hist_nEntries").Print()

# define new test column that stores relevant bin number
# the following line doesn't work because SV_x and SV_y are actually vectors of floats (I think), which makes sense because there can be more than one SV per event. I'm thinking we therefore want one material flag per SV, not one flag per event. I'll start by just handling the leading SV, then I or Zhenyu can generalize it to an arbitrary number of SVs later.
#df = df.Define("material_hist_bin", "material_hist->FindBin(double(SV_x), double(SV_y))")
#df.Display("material_hist_bin").Print()

# define new test column that stores relevant bin number for leading SV
# first filter out events with no SV
#df = df.Filter("nSV > 0", ">= 1 SV")
# then directly access leading SV x and y values; apparently double() isn't necessary
#df = df.Define("material_hist_bin", "material_hist->FindBin(SV_x[0], SV_y[0])")
#df.Display("material_hist_bin").Print()

# check how many events have >=1 SV
#df.Report().Print()

# now define the actual column we want (at least for the leading SV in events with >=1 SV)
#df = df.Define("material_flag", "material_hist->GetBinContent(material_hist->FindBin(SV_x[0], SV_y[0])) > 0.0")
#df.Display("material_flag").Print()

# define new test column that uses a vector
#df = df.Define("vec_test", "std::vector<float> {1.0, 2.0}")
#df.Display("vec_test").Print()
#df = df.Define("rvec_test", "ROOT::VecOps::RVec<float>({1.0, 2.0})")
#df.Display("rvec_test").Print()

# define new test column that uses a python function
# the below doesn't work because numba isn't installed
#import numba
#@ROOT.Numba.Declare(["float"], "bool")
#def bigger_than_2(x):
#    return x > 2

# define new test column using VecOps::Map
df = df.Define("map_test", "return ROOT::VecOps::Map(SV_x, [](float f){return 2*f;})")
df.Display("map_test").Print()
