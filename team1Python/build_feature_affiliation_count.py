# Generates feature files on the affiliation count for each publication
# Input:
# pmid_data.csv
# Output:
# affiliation_count.csv
#

import pandas as pd
from pathlib import Path

def main():

    # Load the dataset
    load_dest = Path("./data/out/")
    f_save = load_dest / "pmid_data.csv"

    df = pd.read_csv(f_save)

    df['affiliation_count'] = df.apply(lambda row: len(str(row['affiliations']).split(';')),axis=1)

    # Group by queries for later analysis, take the mean (we dropped values)
    group_keys = ["query", "search_type", "page"]
    df_out = df.groupby(group_keys).affiliation_count.median()

    # Save to feature set
    save_dest = Path("./data/features/")
    df_out.to_csv(save_dest / "affiliation_count.csv")

    print(df)

if __name__ == '__main__':
    main()
