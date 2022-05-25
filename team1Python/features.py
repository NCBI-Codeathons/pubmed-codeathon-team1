import pandas as pd
import numpy as np
from pathlib import Path

from mapaffil import mapaffil


def affiliation(x):
    # split affilations string into a list
    x = x.split(";")

    # take first author's affiliation
    x = x[0]

    return x


def location(x):
    return mapaffil(x)["country"]


# Load the dataset
load_dest = Path("../data/out/")
f_save = load_dest / "pmid_data.csv"

df = pd.read_csv(f_save)

# Drop missing values
df = df.dropna(subset=["affiliations"])
df['affiliations'] = df.affiliations.apply(affiliation())
df['country'] = df.pmid.apply(location)
print(df.country)



# Language is saved as list.
# If English is the only language it will look like this
df["is_english_only"] = df["languages"] == "eng"

# Group by queries for later analysis, take the mean (we dropped values)
group_keys = ["query", "search_type", "page"]
dx = df.groupby(group_keys).is_english_only.mean()

# Save to feature set
save_dest = Path("../data/features/")
dx.to_csv(save_dest / "author_affiliation_and_country.csv")
