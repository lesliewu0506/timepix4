import uproot
import pandas as pd

def ConvertFitData(root_file_path, csv_file_path):
    file = uproot.open(root_file_path)
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
    df_data.to_csv(csv_file_path, index=False)

def ConvertManualCalibrationData(root_file_path, csv_file_path):
    file = uproot.open(root_file_path)
    tree_name = "clusterTree"

    # Access the tree
    tree = file[tree_name]

    # Convert the TTree data into a Pandas DataFrame
    # The `arrays()` function reads the specified branches; specifying library="pd" returns a DataFrame.
    df = tree.arrays(["nhits", "col", "row", "tot", "charge"], library="pd")

    # # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    # Specify the ROOT file path
    root_file_path = "Am-241 Runs/N10-250404-143700.root"
    csv_file_path = "N10-250404-143700_normal.csv"

    ConvertManualCalibrationData(root_file_path, csv_file_path)
