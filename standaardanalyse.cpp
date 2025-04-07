//Dit script maakt een hitmap en drie histogrammen van clustersize, ToA and clusterToT

// ===============Headers=================
#include <iostream>
#include <vector>
#include <tuple> 
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
const char* filename="N10-250404-133629";
const char* filename2="N116-250403-150114";
const char* N10_Long = "N10-250404-143700";

// Constants
const int HistogramArraySize=3;
const char* variable[HistogramArraySize]={"N hits","ToA","Cluster ToT"};
const char* x_axis[HistogramArraySize]={"Cluster Size","ToA [s]","Cluster ToT [25 ns]"};
const int array_length= 10000;

// // Create histograms
// TH1D* hist[HistogramArraySize];
// TH1D* histcharge;
// TH1D* tot_plot;
// TH1D* singlepixelplot;
// TH2D* hitmap;
// int N_hits[448][512]={0};

// ================Function prototypes===============
std::tuple<TH2D*, std::array<TH1D*, HistogramArraySize>, TH1D*, TH1D*, TH1D*> get_file_data(const char* filename);
// void FindPixelWithMostHits (void);
void makehist4(std::array <TH1D*, HistogramArraySize > HistogramArray, TH2D* hitmap);
void MakeChargeAndToTHistograms(TH1D* histcharge, TH1D* tot_plot);
void MakeSinglePixelHistogram(TH1D* singlepixelplot);
void OverlapToTHistograms(TH1D* hist1, TH1D* hist2);
void MakeChargeHistogramWithFit(TH1D* histcharge);
// ================Function prototypes===============

// Main function
int standaardanalyse()
{
    time_t start_time = time(NULL);

    // Get Data from ROOT file
    // auto [hitmap1, HistogramArray1, histcharge1, tot_plot1, singlepixelplot1] = get_file_data(Form("%s.root", filename));
    // auto [hitmap2, HistogramArray2, histcharge2, tot_plot2, singlepixelplot2] = get_file_data(Form("%s.root", filename2));
    auto [hitmap3, HistogramArray3, histcharge3, tot_plot3, singlepixelplot3] = get_file_data(Form("%s.root", N10_Long));

    // Make Histograms
    // makehist4(HistogramArray3, hitmap3);
    // MakeChargeAndToTHistograms(histcharge3, tot_plot3);
    // MakeSinglePixelHistogram(singlepixelplot);
    // OverlapToTHistograms(tot_plot1, tot_plot2);
    MakeChargeHistogramWithFit(histcharge3);
    time_t end_time=time(NULL)-start_time;
    return end_time;
}

std::tuple<TH2D*, std::array<TH1D*, HistogramArraySize>, TH1D*, TH1D*, TH1D*> get_file_data(const char* filename)
{
    // Create histograms
    std::array<TH1D*, HistogramArraySize> HistogramArray;
    TH1D* histcharge;
    TH1D* tot_plot;
    TH1D* singlepixelplot;
    TH2D* hitmap;
    int N_hits[448][512]={0};

    double tosec=1000000000;
    double toa_sec; 

    TFile* file = new TFile(filename, "READ");
    TTree* rawtree = (TTree*)file->Get("clusterTree");
    
    // rawtree->Print();
    int length_hits = rawtree->GetEntries();
    // cout<<"number of events "<<length_hits<<endl;

    // Plots the standard analysis histograms
    hitmap=new TH2D("hitmap",Form("hitmap %s",filename),448,-0.5,447.5,512,-0.5,511.5);

    // Plots for histogram ToT and Charge
    histcharge=new TH1D("histcharge", "Histogram of Charge Americium Source", 200, 0 , 20);
    tot_plot = new TH1D("tot_plot", "ToT", 100, 0 , 300);
    singlepixelplot = new TH1D("singlepixelplot", "Single Pixel Charge Histogram", 100, 0 , 20);

    for(int i=0;i<HistogramArraySize;i++){
        if (i==0){HistogramArray[i] = new TH1D(Form("HistogramArray[%i]",i), Form("%s ",variable[i]), 20, 0.5, 20.5);}
        else if (i==1){HistogramArray[i] = new TH1D(Form("HistogramArray[%i]",i), Form("%s per 1 sec",variable[i]), 1550, 0, 3600);}
        else if (i==2){HistogramArray[i] = new TH1D(Form("HistogramArray[%i]",i), Form("%s ",variable[i]), 800, -0.5,799.5);}
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

    for (long event=0;event<length_hits;event++)
    {
        rawtree->GetEntry(event);
        if (event%1000000==0 and event>0){cout<<event<<endl;}
        
        toa_sec=toa[0]/(tosec)*25/128;
        HistogramArray[0]->Fill(nhits);
        HistogramArray[2]->Fill(clusterTot);

        histcharge->Fill(charge[0]/1000);
        tot_plot->Fill(tot[0]);

        for(int n=0;n<nhits;n++)
        {
            // Save values of pixel with most hits for further analysis
            // if (col[n] == 85 && row[n] == 510) 
            // {
            //     singlepixelplot->Fill(charge[n]/1000);
            // }

            toa_sec=toa[n]/(tosec)*25/128;
            HistogramArray[1]->Fill(toa_sec);
            N_hits[col[n]][row[n]]+=1;
        }
    }

    // Fill hitmap array
    for (int i=0;i<448; i++){
        for (int j=0;j<512;j++)
            if (N_hits[i][j] == 0){
                hitmap->Fill(i,j,0);
            }
            else
            {
                hitmap->Fill(i, j, N_hits[i][j]);

                // Filter noisy pixels
                if (N_hits[i][j]>6000)
                {
                    cout<<i<<","<<j<<","<<N_hits[i][j]<<endl;
                }
            }
    }

    // FindPixelWithMostHits();

    return std::make_tuple(hitmap, HistogramArray, histcharge, tot_plot, singlepixelplot);
}

// void FindPixelWithMostHits (void)
// {
//     // Find the pixel with the most hits
//     int max_hits = 0;
//     int max_row = -1;
//     int max_col = -1;
//     for (int i = 0; i < 448; i++) {
//         for (int j = 0; j < 512; j++)
//         {
//             if (N_hits[i][j] > max_hits && N_hits[i][j] < 6000)
//             {
//                 max_hits = N_hits[i][j];
//                 max_col = i;
//                 max_row = j;
//             }
//         }
//     }
//     cout<<"Pixel with most hits: (" << max_row << ", " << max_col << ") with " << max_hits << " hits." << endl;
// }

void makehist4(std::array <TH1D*, HistogramArraySize > HistogramArray, TH2D* hitmap)
{
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
    hitmap->SetMaximum(100);
    hitmap->SetMinimum(0);

    hitmap->Draw("COLZ");

    for (int i = 0; i < HistogramArraySize; i++)
    {
        canv->cd(i+2);
        HistogramArray[i]->SetXTitle(x_axis[i]);
        HistogramArray[i]->SetYTitle("Entries");
        HistogramArray[i]->SetLineWidth(3);   // nice thick line
        HistogramArray[i]->SetFillColor(5);   // yellow fill color
        HistogramArray[i]->Draw();
        if (i == 1) 
        {
            // double mean = HistogramArray[1]->GetMean();
            // TLine* meanLine = new TLine(HistogramArray[1]->GetXaxis()->GetXmin(), mean,
            //                             HistogramArray[1]->GetXaxis()->GetXmax(), mean);
            // meanLine->SetLineColor(kRed);
            // meanLine->SetLineStyle(2); // dashed
            // meanLine->SetLineWidth(2);
            // meanLine->Draw("same");
            gPad->SetLogy(); // Set logarithmic y-axis for the current pad
        }
        canv->cd((i+1)*2);
    }

    canv->SaveAs(Form("%s_standaardanalyse.png", N10_Long));
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
    ChargeToTCanvas->SaveAs("N10 Charge and ToT Histograms.png");

    // Clear the canvas and close it
    ChargeToTCanvas-> Clear();
    ChargeToTCanvas-> Close();
}

void MakeSinglePixelHistogram(TH1D* singlepixelplot) 
{
    // Create single pixel charge histogram
    TCanvas* PixelCanvas = new TCanvas("pixelCanvas", "Charge at Single Pixel with highest hits", 1800, 1200);
    
    // Set histogram properties
    singlepixelplot->SetXTitle("Charge [ke]");
    singlepixelplot->SetYTitle("Entries");
    singlepixelplot->SetLineWidth(2);
    singlepixelplot->SetFillColor(4);
    
    // Draw the histogram
    singlepixelplot->Draw();
    PixelCanvas->SaveAs("N10 Single Pixel Charge Histogram.png");

    PixelCanvas-> Clear();
    PixelCanvas-> Close();
}

void OverlapToTHistograms(TH1D* hist1, TH1D* hist2)
{
    TCanvas* OverlapCanvas = new TCanvas("OverlapCanvas", "Overlap ToT Histograms", 1800, 1200);
    hist1->SetXTitle("ToT");
    hist1->SetYTitle("Entries");
    hist1->SetLineWidth(2);
    hist1->SetFillColor(38);
    hist1->Draw();

    hist2->SetLineWidth(2);
    hist2->SetFillColor(48);
    hist2->Draw("same");

    TLegend* legend = new TLegend(0.7, 0.7, 0.9, 0.9);
    legend->AddEntry(hist1, "N10 Data", "f");
    legend->AddEntry(hist2, "N116 Data", "f");
    legend->Draw();

    // Save the combined image
    OverlapCanvas->SaveAs("N10 and N116 Overlap ToT Histograms.png");

    // Clear the canvas and close it
    OverlapCanvas-> Clear();
    OverlapCanvas-> Close();
}

void MakeChargeHistogramWithFit(TH1D* histcharge)
{
    // Create a new histogram with a scaled x-axis (convert from original units to keV)
    int nbins = histcharge->GetNbinsX();
    double old_min = histcharge->GetXaxis()->GetXmin();
    double old_max = histcharge->GetXaxis()->GetXmax();
    double new_min = old_min * 3.6;
    double new_max = old_max * 3.6;
    TH1D* histcharge_scaled = new TH1D("histcharge_scaled", "Histogram of Charge Americium Source", nbins, new_min, new_max);

    // Copy bin contents and errors from the original histogram into the new scaled histogram
    for (int i = 1; i <= nbins; i++)
    {
        double content = histcharge->GetBinContent(i);
        double error = histcharge->GetBinError(i);
        histcharge_scaled->SetBinContent(i, content);
        histcharge_scaled->SetBinError(i, error);
    }

    // Update the x-axis title to reflect the new units (keV)
    histcharge_scaled->SetXTitle("Charge [keV]");
    histcharge_scaled->SetLineWidth(3);
    histcharge_scaled->SetFillColor(5);
    // Create a canvas for drawing the histogram with fits
    TCanvas* fitCanvas = new TCanvas("fitCanvas", "Charge Histogram with Gaussian Fits", 1600, 1200);
    histcharge_scaled->Draw();

    // Define the peak centers (in keV) for Americium-241 decay and its decay products
    double peaks[6] = {8.01, 13.9, 17.7, 20.7, 26.3, 59.5};

    // Loop over each peak and perform a Gaussian fit in a narrow window around the peak
    for (int i = 0; i < 6; i++) 
    {
        double peak = peaks[i];
        double range_min = peak - 1.0;
        double range_max = peak + 1.0;
        // The "R+" options restrict the fit to the range and add the fit to the list
        histcharge_scaled->Fit("gaus", "R+", "", range_min, range_max);
    }
    // Save the canvas as an image file
    fitCanvas->SaveAs("ChargeHistogramWithFits.png");
    // Clean up the canvas
    fitCanvas->Clear();
    fitCanvas->Close();
}