import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import uproot, ast

class HitmapVisualizer:
    def __init__(self, RootFilePath: str) -> None:
        self.RootFilePath = RootFilePath

    def CreateHitmap(self) -> None:
        file = uproot.open(self.RootFilePath)
        tree = file["clusterTree"]

        arrays_data = tree.arrays(["col", "row", "tot"], library="pd")

        df_data = pd.DataFrame(
            {
                "col": arrays_data["col"].to_list(),
                "row": arrays_data["row"].to_list(),
                "tot": arrays_data["tot"].to_list(),
            }
        )

        df_filtered = self._FilterAndUnwrap(df_data)
        mean_tots = df_filtered.groupby(["row", "col"])["tot"].mean().reset_index()

        # Determine center pixel (highest mean ToT)
        center = mean_tots.loc[mean_tots["tot"].idxmax()]
        center_row, center_col = int(center["row"]), int(center["col"])

        # Define 5x5 neighborhood bounds
        row_min, row_max = center_row - 3, center_row + 3
        col_min, col_max = center_col - 3, center_col + 3

        # Filter for the 5×5 area around center
        mean_tots = mean_tots[
            mean_tots["row"].between(row_min, row_max)
            & mean_tots["col"].between(col_min, col_max)
        ]

        # Pivot only the 5×5 region
        heatmap_data = mean_tots.pivot(index="row", columns="col", values="tot")
        # Ensure a complete 5×5 grid and fill missing pixels with zero
        rows = list(range(row_min, row_max + 1))
        cols = list(range(col_min, col_max + 1))
        heatmap_data = heatmap_data.reindex(index=rows, columns=cols, fill_value=np.nan)
        plt.figure(figsize=(10, 8))
        ax = sns.heatmap(
            heatmap_data,
            cmap="viridis",
            cbar_kws={"label": "ToT [25ns]"},
            square=True,
            annot=True,
            annot_kws={"size": 18},
            fmt=".2f",
        )
        # Draw a black border around the heatmap frame
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(1)
            spine.set_color("black")
        ax.set_title(f"ToT per pixel")
        plt.tight_layout()
        plt.savefig(f"Focus at ({center_col}, {center_row}).png", dpi=600)
        plt.show()

    def _FilterAndUnwrap(self, df: pd.DataFrame) -> pd.DataFrame:
        for c in ["col", "row", "tot"]:
            df[c] = df[c].apply(self._ParseList)

        df["combined"] = df.apply(
            lambda r: list(zip(r["row"], r["col"], r["tot"])), axis=1
        )
        df_exploded = df.explode("combined")

        # Unpack the tuples back into separate columns
        df_exploded[["row", "col", "tot"]] = pd.DataFrame(
            df_exploded["combined"].tolist(), index=df_exploded.index
        )
        df_exploded = df_exploded.drop(columns=["combined"])
        return df_exploded

    def _ParseList(self, x: str | list | tuple) -> list:
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