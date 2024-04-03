#!/usr/bin/env python


import ROOT
import sys
import numpy as np


f1 = ROOT.TFile.Open("Material_Map_HIST.root")
map_d = f1.Get("material_map")
#map_d.SetDirectory(0)
#f1.Close()

#@ROOT.Numba.Declare(['float','float'],'float')
#def veto_map(x, y):
#    bin_pos = map1.FindBin(x,y)
#    bin_val = map1.GetBinContent(bin_pos)
#    return bin_val

#def DeclareToCpp(**kwargs):
#    for k, v in kwargs.items():
#        ROOT.gInterpreter.Declare(f"namespace PyVars {{ auto &{k} = *reinterpret_cast<{type(v).__cpp_name__}*>({ROOT.addressof(v)}); }}")


#ROOT.gInterpreter.Declare('''
#        Float_t vetomap(const char *filename, Float_t *SVx, Float_t *SVy){
#            TFile f1 = TFile(filename, "READ");
#            TH2D *map_d = (TH2D*) f1.Get("material_map");
#            TH2F *map_f;
#            Float_t *bin_pos;
#            Float_t *bin_val;
#
#            map_d.Copy(map_f);
#            map_f->SetDirectory(0);
#            
#            bin_pos = map_f->FindBin(SVx,SVy);
#            bin_val = map_f->GetBinContent(bin_pos);
#
#            f1.Close();
#            return bin_val;
#        }
#''')






#d0 = ROOT.RDataFrame("Events", "NanoAOD_1.root")
#df = d0.Range(20)
df = ROOT.RDataFrame("Events", "NanoAOD_1.root")

#df0 = df.Define("double_svx",[](const ROOT::RVecI &v) {return double(v.begin(), v.end());}, {"SV_x"}).Define("double_svy",[](const ROOT::RVecI &w) {return double(w.begin(), w.end());}, {"SV_y"})

#df0 = df.Define("veto_check",veto_map,["SV_x","SV_y"])
#df0 = df.Define('veto_check','Numba::veto_map(SV_x,SV_y)')
#df0 = df.Define("veto_check","veto_map(SV_x,SV_y)")
#df1 = df0.Filter("veto_check == 0")

#df_pos = df.Define("vetobin_pos", "map_d.FindBin(SV_x,SV_y)")


#DeclareToCpp(map_d=map_d)
df_d = df.Define("double_SVx","ROOT.Double(SV_x)").Define("double_SVy","ROOT.Double(SV_y)")
#df1 = df_d.Filter("PyVars::map1.GetBinContent(PyVars::map1.FindBin(double_svx, double_svy)) == 0")
#df1 = df.Filter("map_d.GetBinContent(map_d.FindBin(SV_x, SV_y)) == 0")
#df1 = df.Filter("PyVars::map_d.GetBinContent(PyVars::map_d.FindBin(ROOT.Double(SV_x), ROOT.Double(SV_y))) == 0")
#df.Display("SV_x").Print()



#df0 = df.Define("veto_check","vetomap("Material_Map_HIST.root",SV_x,SV_y)")
#ROOT.vetomap("Material_Map_HIST.root",1.1,2.2).Print()

df2 = df.Filter("MET_pt < 600").Define("SV_r","sqrt(SV_x * SV_x + SV_y * SV_y)")
#df2v = df1.Filter("MET_pt < 600").Define("SV_r","sqrt(SV_x * SV_x + SV_y * SV_y)")

svr = df2.Histo1D(("datar", "SV_r", 250, 0, 25), "SV_r")
#svrv = df2v.Histo1D(("datarv", "SV_r_veto", 250, 0, 25), "SV_r")
svxy = df2.Histo2D(("svxy", "SV_xy", 500, -25, 25, 500, -25, 25), "SV_x", "SV_y")

l_bp = ROOT.TLine(2.3, 0.0, 2.3, 4.0e+5)
#l_innershield = ROOT.TLine(3.7, 0.0, 3.7, 4.0e+5)
l_layer1 = ROOT.TLine(2.9, 0.0, 2.9, 4.0e+5)
l_layer2 = ROOT.TLine(6.8, 0.0, 6.8, 4.0e+5)
l_layer3 = ROOT.TLine(10.9, 0.0, 10.9, 4.0e+5)
l_layer4 = ROOT.TLine(16.0, 0.0, 16.0, 4.0e+5)

t1 = ROOT.TText(2.1, 4.5e+4, "Beam Pipe")
#t2 = ROOT.TText(3.6, 1.0e+4, "BPIX Detector Inner Shield")
t3 = ROOT.TText(3.6, 9.0e+3, "BPIX Detector Layer 1")
t4 = ROOT.TText(6.6, 9.0e+3, "BPIX Detector Layer 2")
t5 = ROOT.TText(10.7, 9.0e+3, "BPIX Detector Layer 3")
t6 = ROOT.TText(15.8, 9.0e+3, "BPIX Detector Layer 4")


c1 = ROOT.TCanvas("c1","c1",1600,1600)
#c1.SetRightMargin(5)
c1.Divide(2,2)

c1.cd(1)
ROOT.gPad.SetRightMargin(0.15)
svxy.Draw("Colz")
svxy.GetXaxis().SetTitle("Distance (cm)")
svxy.GetYaxis().SetTitle("Distance (cm)")
svxy.SetStats(0)
map_d.Draw("same")
ROOT.gPad.SetLogz(True)

c1.cd(2)
svr.Draw("h")
#svrv.Draw("same")
#svrv.SetLineColor(ROOT.kBlue)
svr.GetXaxis().SetTitle("Distance (cm)")
l_bp.SetLineStyle(2)
l_bp.SetLineWidth(2)
l_bp.Draw("same")
t1.SetTextSize(0.025)
t1.SetTextAngle(90)
t1.Draw()
#l_innershield.SetLineStyle(2)
#l_innershield.SetLineWidth(2)
#l_innershield.Draw("same")
#t2.SetTextSize(0.03)
#t2.SetTextAngle(90)
#t2.Draw()
l_layer1.SetLineStyle(2)
l_layer1.SetLineWidth(2)
l_layer1.Draw("same")
t3.SetTextSize(0.025)
t3.SetTextAngle(90)
t3.Draw()
l_layer2.SetLineStyle(2)
l_layer2.SetLineWidth(2)
l_layer2.Draw("same")
t4.SetTextSize(0.025)
t4.SetTextAngle(90)
t4.Draw()
l_layer3.SetLineStyle(2)
l_layer3.SetLineWidth(2)
l_layer3.Draw("same")
t5.SetTextSize(0.025)
t5.SetTextAngle(90)
t5.Draw()
l_layer4.SetLineStyle(2)
l_layer4.SetLineWidth(2)
l_layer4.Draw("same")
t6.SetTextSize(0.025)
t6.SetTextAngle(90)
t6.Draw()
ROOT.gPad.SetLogy(True)

c1.cd(3)
ROOT.gPad.SetRightMargin(0.15)
svxy.Draw("Colz")
svxy.GetXaxis().SetTitle("Distance (cm)")
svxy.GetYaxis().SetTitle("Distance (cm)")
svxy.SetStats(0)
#svxy.Draw("Lego2")
#svxy.Draw("Surf3")
ROOT.gPad.SetLogz(True)

c1.SaveAs("mp_veto.png")
#c1.SaveAs("mp.png")

