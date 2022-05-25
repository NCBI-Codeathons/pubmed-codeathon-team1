import pandas as pd
from pathlib import Path
from tqdm import tqdm
from mapaffil import mapaffil

tqdm.pandas()


def affiliation(x):
    # split affilations string into a list
    x = x.split(";")

    # take first author's affiliation
    x = x[0]

    return x


def location(x):
    return mapaffil(x).get("country", "")


def build_affiliations(df, group_keys, dest):
    df = df.dropna(subset=["affiliations"])
    df['affiliations'] = df.affiliations.progress_apply(affiliation)
    dx = df.groupby(group_keys).affiliations.max()
    dx.to_csv(dest / "author_affiliation.csv")


def build_countries(df, group_keys, dest):
    #df['country'] = df.pmid.progress_apply(location)
    df.country = df.country.fillna("")
    #df = df.dropna(subset=["country"])
    dy = df.groupby(group_keys).country.max()
    dy.to_csv(save_dest / "author_country.csv")


# Load the dataset
load_dest = Path("../data/out/")
f_save = load_dest / "pmid_data.csv"
df = pd.read_csv(f_save)

group_keys = ["query", "search_type", "page"]
save_dest = Path("../data/features/")
#build_affiliations(df, group_keys, save_dest)

df = pd.read_csv("tmp.csv") #tmp
print(df.country.value_counts()) #tmp
build_countries(df, group_keys, save_dest)





