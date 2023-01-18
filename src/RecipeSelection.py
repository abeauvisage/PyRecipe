import numpy as np
import pandas as pd

def make_selection(recipes: list, selection_array: np.array):
    df = pd.DataFrame(data=np.array(selection_array), index=recipes, columns=["days", "score"])
    df = df.sort_values(by=["days", "score"],ascending=False)
    
    return df[np.logical_and(df["days"] > 14, df["score"] >= 0.0)]