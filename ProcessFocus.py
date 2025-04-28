import os, uproot, ast
import pandas as pd
import matplotlib.pyplot as plt

def parse_list(x):
    if isinstance(x, str):
        parsed = ast.literal_eval(x)
        if isinstance(parsed, (list, tuple)):
            return list(parsed)
        else:
            return [parsed]
    elif isinstance(x, (list, tuple)):
        return list(x)
    else:
        return [x]


def FilterAndUnwrap(df: pd.DataFrame) -> pd.DataFrame:
    # Parse each cell into a list
    for c in ["col", "row", "tot"]:
        df[c] = df[c].apply(parse_list)

    # Zip the three lists together so they explode in parallel
    df["combined"] = df.apply(lambda r: list(zip(r["row"], r["col"], r["tot"])), axis=1)
    df_exploded = df.explode("combined")

    # Unpack the tuples back into separate columns
    df_exploded[["row", "col", "tot"]] = pd.DataFrame(
        df_exploded["combined"].tolist(), index=df_exploded.index
    )
    df_exploded = df_exploded.drop(columns=["combined"])

    # df_exploded.to_csv(f"Data/Focus/cluster42_{z}.csv", index=False)
    return df_exploded


def process_folder(folder_path: str):
    # derive height string and numeric
    basename = os.path.basename(folder_path)
    height_str = basename.split("_", 1)[1]  # e.g. "42p700"
    height_num = height_str.replace("p", "_")  # e.g. "42.700"
    height_num2 = height_str.replace("p", ".") # e.g. 42.700
    # find root file
    root_files = [f for f in os.listdir(folder_path) if f.endswith(".root")]
    if not root_files:
        print(f"No root file in {folder_path}, skipping")
        return
    root_file = os.path.join(folder_path, root_files[0])

    # open tree
    file = uproot.open(root_file)
    tree = file["clusterTree"]

    # 1) CLTOT CSV
    df_cl = pd.DataFrame(
        {"cltot": tree.arrays(["cltot"], library="pd")["cltot"].to_numpy()}
    )
    mean_cl = df_cl["cltot"].mean()

    arrays = tree.arrays(["col", "row", "tot"], library="pd")
    df_data = pd.DataFrame(
        {
            "col": arrays["col"].to_numpy(),
            "row": arrays["row"].to_numpy(),
            "tot": arrays["tot"].to_numpy(),
        }
    )
    df_exp = FilterAndUnwrap(df_data)
    df_mean = df_exp.groupby(["row", "col"])["tot"].mean().reset_index()
    df_mean = df_mean.sort_values("tot", ascending=False)
    df_mean.to_csv(f"Data/ProcessedFocus/tot_{height_num}.csv", index=False)
    max_tot = df_mean["tot"].max()
    return height_num2, mean_cl, max_tot


def ZScanPlot():
    df= pd.read_csv("Data/ProcessedFocus/Results.csv")

    # Load aggregated results
    df = pd.read_csv("Data/ProcessedFocus/Results.csv")

    # Plot mean_cltot and max_tot vs height
    plt.figure(figsize=(10, 6))
    plt.plot(df["height"], df["mean_cltot"], marker = "o", label="Mean cltot")
    plt.plot(df["height"], df["max_tot"], marker = "o", label="Mean tot")
    # Highlight global maximum of max_tot
    max_idx = df["max_tot"].idxmax()
    max_height = df.loc[max_idx, "height"]
    max_value = df.loc[max_idx, "max_tot"]
    plt.scatter(
        max_height,
        max_value,
        marker='o',
        color='red',
        s=100,
        label=f"Max ToT at z = {max_height} mm",
        zorder = 3
    )
    plt.xlabel("Z Position Stage [mm]")
    plt.ylabel("ToT [25ns]")
    plt.title("Mean clToT and ToT vs Z Position")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ZScanPlot.png", dpi = 600)
    plt.show()
    
if __name__ == "__main__":
    data_root = "Data/Focus2"
    results = []
    for d in os.listdir(data_root):
        if d.startswith("focus_"):
            result= process_folder(os.path.join(data_root, d))
            if result:
                results.append(result)
    # Write the aggregate cltot means for all heights
    df_results = pd.DataFrame(results, columns=["height", "mean_cltot", "max_tot"])
    df_results = df_results.sort_values("height")
    df_results.to_csv("Data/ProcessedFocus/Results.csv", index=False)

    ZScanPlot()
