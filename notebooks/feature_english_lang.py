import pandas as pd
import numpy as np
from pathlib import Path


# Load the dataset
load_dest = Path("../data/out/")
f_save = load_dest / "pmid_data.csv"

df = pd.read_csv(f_save)

# Drop missing values
df = df.dropna(subset=["languages"])

# Language is saved as list.
# If English is the only language it will look like this
df["is_english_only"] = df["languages"] == "eng"

# Group by queries for later analysis, take the mean (we dropped values)
group_keys = ["query", "search_type", "page"]
dx = df.groupby(group_keys).is_english_only.mean()

# Save to feature set
save_dest = Path("../data/features/")
dx.to_csv(save_dest / "is_english_only.csv")
