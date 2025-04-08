import uproot
import pandas as pd

# Open the ROOT file
# file = uproot.open("N10-250404-131220.root")
# file = uproot.open("N112-250407-151119.root")
file = uproot.open("Test Pulse Data/N113-250408-094415.root")

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
df_data.to_csv("Test Pulse Data/fitData_N113.csv", index=False)
print("Export complete: fitData.csv")