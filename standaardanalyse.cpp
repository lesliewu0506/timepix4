//Dit script maakt een hitmap en drie histogrammen van clustersize, ToA and clusterToT

// ===============Headers=================
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
// ===============Headers=================

// Add filename here without extension
const char* filename="N116-250403-150114";

// Constants
const int hist1d=3;
const char* variable[hist1d]={"N hits","ToA","Cluster ToT"};
const char* x_axis[hist1d]={"Cluster Size","ToA [s]","Cluster ToT [25 ns]"};

// Create histograms
TH1D* hist[hist1d];
TH1D* histcharge;
TH1D* tot_plot;
TH1D* singlepixelplot;
TH2D* hitmap;
int N_hits[448][512]={0};

double tosec=1000000000;
double toa_sec;

// ================Function prototypes===============
int get_file_data(const char* filename);
void makehist4(TH1D* hist[3], TH2D* hitmap);
void MakeChargeAndToTHistograms(TH1D* histcharge, TH1D* tot_plot);
void MakeSinglePixelHistogram(TH1D* singlepixelplot);
// ================Function prototypes===============

// Main function
int standaardanalyse(){
    time_t start_time = time(NULL);
    // Get Data from ROOT file
    get_file_data(Form("%s.root",filename));

    // Make Histograms
    // makehist4(hist,hitmap);
    MakeChargeAndToTHistograms(histcharge, tot_plot);
    // MakeSinglePixelHistogram(singlepixelplot);
    time_t end_time=time(NULL)-start_time;
    return end_time;
}

int get_file_data(const char* filename){
    TFile* file = new TFile(filename, "READ");
    TTree* rawtree = (TTree*)file->Get("clusterTree");
    
    // rawtree->Print();
    // int length_hits = rawtree->GetEntries();
    // cout<<"number of events "<<length_hits<<endl;
    int array_length=2000;

    // Plots the standard analysis histograms
    hitmap=new TH2D("hitmap",Form("hitmap %s",filename),448,-0.5,447.5,512,-0.5,511.5);

    // Plots for histogram ToT and Charge
    histcharge=new TH1D("histcharge", "Histogram of Charge Americium Source", 200, 0 , 20);
    tot_plot = new TH1D("tot_plot", "ToT", 100, 0 , 300);
    singlepixelplot = new TH1D("singlepixelplot", "Single Pixel Charge Histogram", 100, 0 , 20);

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

    // Add charge array
    double charge[array_length];
    rawtree->SetBranchAddress("charge",  &charge);
    
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

        histcharge->Fill(charge[0]/1000);
        tot_plot->Fill(tot[0]);

        for(int n=0;n<nhits;n++)
        {
            // Save values of pixel with most hits for further analysis
            if (col[n] == 70 && row[n] == 26) 
            {
                singlepixelplot->Fill(charge[n]/1000);
            }

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

    // Find the pixel with the most hits
    int max_hits = 0;
    int max_row = -1;
    int max_col = -1;
    for (int i = 0; i < 448; i++) {
        for (int j = 0; j < 512; j++) {
            if (N_hits[i][j] > max_hits) {
                max_hits = N_hits[i][j];
                max_row = i;
                max_col = j;
            }
        }
    }
    std::cout << "Pixel with most hits: (" << max_col << ", " << max_row << ") with " << max_hits << " hits." << std::endl;
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

    // Set the limits for the gradient of N hits
    hitmap->SetMaximum(60);
    hitmap->SetMinimum(0);

    hitmap->Draw("COLZ");

    for (int i=0;i<3;i++)
    {
        canv->cd(i+2);
        hist[i]->SetXTitle(x_axis[i]);
        hist[i]->SetYTitle("Entries");
        hist[i]->SetLineWidth(3);   // nice thick line
        hist[i]->SetFillColor(5);   // yellow fill color
        hist[i]->Draw();
        if (i == 1) 
        {
            double mean = hist[1]->GetMean();
            TLine* meanLine = new TLine(hist[1]->GetXaxis()->GetXmin(), mean,
                                        hist[1]->GetXaxis()->GetXmax(), mean);
            meanLine->SetLineColor(kRed);
            meanLine->SetLineStyle(2); // dashed
            meanLine->SetLineWidth(2);
            meanLine->Draw("same");
            gPad->SetLogy(); // Set logarithmic y-axis for the current pad
        }
        canv->cd((i+1)*2);
    }

    canv->SaveAs(Form("%s_standaardanalyse.png",filename));
    canv->Clear();
    canv->Close();
}

void MakeChargeAndToTHistograms(TH1D* histcharge, TH1D* tot_plot)
{
    TCanvas* ChargeToTCanvas = new TCanvas("ChargeToTCanvas", "Charge and ToT Histograms", 1600, 1200);
    ChargeToTCanvas -> Divide(1,2); // 1 column, 2 rows

    // First Plot: Charge Histogram
    ChargeToTCanvas -> cd(1);
    histcharge->SetXTitle("Charge [ke]");
    histcharge->SetYTitle("Entries");
    histcharge->SetLineWidth(2);
    histcharge->SetFillColor(38);
    histcharge->Draw();

    // Second Plot: ToT Histogram
    ChargeToTCanvas->cd(2);
    tot_plot->SetXTitle("ToT");
    tot_plot->SetYTitle("Entries");
    tot_plot->SetLineWidth(2);
    tot_plot->SetFillColor(46);
    tot_plot->Draw();

    // Save the combined image
    ChargeToTCanvas->SaveAs("Charge and ToT Histograms.png");

    // Clear the canvas and close it
    ChargeToTCanvas-> Clear();
    ChargeToTCanvas-> Close();
}

void MakeSinglePixelHistogram(TH1D* singlepixelplot) 
{
    // Create single pixel charge histogram
    TCanvas* PixelCanvas = new TCanvas("pixelCanvas", "Charge at Single Pixel with highest hits", 800, 600);
    
    // Set histogram properties
    singlepixelplot->SetXTitle("Charge [ke]");
    singlepixelplot->SetYTitle("Entries");
    singlepixelplot->SetLineWidth(2);
    singlepixelplot->SetFillColor(4);
    
    // Draw the histogram
    singlepixelplot->Draw();
    PixelCanvas->SaveAs("singlepixelplot.png");

    PixelCanvas-> Clear();
    PixelCanvas-> Close();
}