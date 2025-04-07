import uproot
import pandas as pd

# Open the ROOT file
# file = uproot.open("N10-250404-131220.root")
file = uproot.open("N112-250407-151119.root")
### ----------- FIT RESULTS -------------
tree_results = file["fitResults"]
arrays_results = tree_results.arrays()

# Convert to DataFrame
df_results = pd.DataFrame({
    "col": arrays_results["col"].to_numpy(),
    "row": arrays_results["row"].to_numpy(),
    "chi2": arrays_results["chi2"].to_numpy(),
    "ndof": arrays_results["ndof"].to_numpy(),
    "pars": arrays_results["pars"].to_list(),
    "errs": arrays_results["errs"].to_list(),
})

# Expand fit parameters and errors
pars_df = pd.DataFrame(df_results["pars"].tolist(), columns=["p0", "p1", "p2", "p3"])
errs_df = pd.DataFrame(df_results["errs"].tolist(), columns=["p0_err", "p1_err", "p2_err", "p3_err"])
df_results = df_results.drop(columns=["pars", "errs"])
df_results_expanded = pd.concat([df_results, pars_df, errs_df], axis=1)

# Save to CSV
df_results_expanded.to_csv("fitResults_expanded_N112.csv", index=False)
print("Export complete: fitResults_expanded.csv")

### ----------- FIT DATA -------------
tree_data = file["fitData"]
arrays_data = tree_data.arrays()

# Convert to DataFrame
df_data = pd.DataFrame({
    "col": arrays_data["col"].to_numpy(),
    "row": arrays_data["row"].to_numpy(),
    "charge": arrays_data["charge"].to_numpy(),
    "meanTot": arrays_data["meanTot"].to_numpy(),
    "stdvTot": arrays_data["stdvTot"].to_numpy(),
    "nhits": arrays_data["nhits"].to_numpy(),
})

# Save to CSV
df_data.to_csv("fitData_N112.csv", index=False)
print("Export complete: fitData.csv")