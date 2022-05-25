# Generates feature files on the author count for each publication
# Input:
# pmid_data.csv
# Output:
# author_count.csv
#

import pandas as pd
from pathlib import Path

def main():
    print('hello')
    # Load the dataset
    load_dest = Path("./data/out/")
    f_save = load_dest / "pmid_data.csv"

    df = pd.read_csv(f_save)

    df['author_count'] = df.apply(lambda row: len(str(row['authors']).split(';')),axis=1)

    # Group by queries for later analysis, take the mean (we dropped values)
    group_keys = ["query", "search_type", "page"]
    df_out = df.groupby(group_keys).author_count.median()

    # Save to feature set
    save_dest = Path("./data/features/")
    df_out.to_csv(save_dest / "author_count.csv")

    print(df)

if __name__ == '__main__':
    main()
