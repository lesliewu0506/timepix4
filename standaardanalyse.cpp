//Dit script maakt een hitmap en drie histogrammen van clustersize, ToA and clusterToT,   
//run met: root standaardanalyse.cpp  
#include <iostream>
#include <vector>
#include<tuple> 
#include <list>
#include <fstream>
#include <ctime>
#include <array>
#include "TROOT.h"
#include "TFile.h" 
#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TClass.h"

const char* filename="N116-250401-115615"; // without extension, file in map /localstore/tpx4/data/trees/

const int hist1d=3;
TH1D* hist[hist1d];
TH2D* hitmap;
const char* variable[hist1d]={"nhits","ToA","cltot"};
const char* x_axis[hist1d]={"Cluster Size","ToA [s]","cltot [25 ns]"};
int N_hits[448][512]={0};
int N_hitshigh[448][512]={0};
int threshold;
double tosec=1000000000;
double toa_sec;

int get_file_data(const char* filename);
void makehist4(TH1D* hist[3], TH2D* hitmap);

// the main function
int standaardanalyse(){
    time_t start_time = time(NULL);
    get_file_data(Form("%s.root",filename));
    makehist4(hist,hitmap);
    time_t end_time=time(NULL)-start_time;
    return end_time;
}

int get_file_data(const char* filename){
    TFile* file = new TFile(filename, "READ");
    TTree* rawtree = (TTree*)file->Get("clusterTree");
    
    rawtree->Print();
    int length_hits = rawtree->GetEntries();
    cout<<"number of events "<<length_hits<<endl;
    int array_length=250000;
    int x=10;

    hitmap=new TH2D("hitmap",Form("hitmap %s",filename),448,-0.5,447.5,512,-0.5,511.5);
    for(int i=0;i<hist1d;i++){
        if (i==0){hist[i] = new TH1D(Form("hist[%i]",i), Form("%s ",variable[i]), 20, 0.5, 20.5);}
        else if (i==1){hist[i] = new TH1D(Form("hist[%i]",i), Form("%s per 1 sec",variable[i]), 1550, 0, 1800);}
        else if (i==2){hist[i] = new TH1D(Form("hist[%i]",i), Form("%s ",variable[i]), 800, -0.5,799.5);}
    }

    int nhits;
    double tot[array_length];
    int row[array_length];
    int col[array_length];
    int ftoa[array_length];
    long toa[array_length];
    double clusterTot;

    rawtree->SetBranchAddress("row",   &row);
    rawtree->SetBranchAddress("col",   &col);
    rawtree->SetBranchAddress("nhits",    &nhits);
    rawtree->SetBranchAddress("tot",   &tot);
    rawtree->SetBranchAddress("cltot",   &clusterTot);
    rawtree->SetBranchAddress("ftoaRise",    &ftoa);
    rawtree->SetBranchAddress("toa",    &toa);
    
    for (long event=0;event<length_hits;event++){
        rawtree->GetEntry(event);
        if (event%1000000==0 and event>0){cout<<event<<endl;}
        
        toa_sec=toa[0]/(tosec)*25/128;
        hist[0]->Fill(nhits);
        hist[2]->Fill(clusterTot);

        for(int n=0;n<nhits;n++){
                toa_sec=toa[n]/(tosec)*25/128;
                hist[1]->Fill(toa_sec);
                N_hits[col[n]][row[n]]+=1;
            }
        

    }

    for (int i=0;i<448; i++){
        for (int j=0;j<512;j++)
            if (N_hits[i][j] == 0){
                hitmap->Fill(i,j,0);
            }
            else{
                hitmap->Fill(i, j, N_hits[i][j]);
                if (N_hits[i][j]>6000){
                    cout<<i<<","<<j<<","<<N_hits[i][j]<<endl;
                }
            }
    }
    return 0;
}

void makehist4(TH1D* hist[3], TH2D* hitmap){
    TCanvas *canv = new TCanvas("c1","c1",1600,1200);
    //gStyle->SetOptStat(0);
    gStyle->SetPadLeftMargin(0.13);
    gStyle->SetPadRightMargin(0.13);
    gStyle->SetPalette(kRainBow); //other color palette 
    canv->Divide(2,2);
    canv->cd(1);
    hitmap->GetZaxis()->SetTitle("Entries");
    hitmap->GetYaxis()->SetTitle("Row");
    hitmap->GetXaxis()->SetTitle("Col");
    hitmap->SetMaximum(30);
    hitmap->SetMinimum(0);
    hitmap->Draw("COLZ");
    for (int i=0;i<3;i++){
        canv->cd(i+2);
        hist[i]->SetXTitle(x_axis[i]);
        hist[i]->SetYTitle("Entries");
        hist[i]->SetLineWidth(3);   // nice thick line
        hist[i]->SetFillColor(5);   // yellow fill color
        hist[i]->Draw();
        if (i == 1) {
            double mean = hist[1]->GetMean();
            TLine* meanLine = new TLine(hist[1]->GetXaxis()->GetXmin(), mean,
                                        hist[1]->GetXaxis()->GetXmax(), mean);
            meanLine->SetLineColor(kRed);
            meanLine->SetLineStyle(2); // dashed
            meanLine->SetLineWidth(2);
            meanLine->Draw("same");
            gPad->SetLogy(); // Set logarithmic y-axis for the current pad
        }
        else if (i == 2) {
            // Start creating fit
            hist[i]->Fit("landau");
        }
        canv->cd((i+1)*2);
    }

    canv->SaveAs(Form("%s_standaardanalyse.png",filename));
    canv->Clear();
    canv->Close();
    return;
}