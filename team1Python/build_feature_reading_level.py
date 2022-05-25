# Generates feature files on the readability stats using the flesch-kincaid score
# Input:
# pmid_data.csv
# Output:
# readability_fk_score_title.csv
# readability_fk_score_abstract.csv
# readability_fk_score_title_abstract_combined.csv
#

import pandas as pd
from pathlib import Path
import fkscore #this seemed as good as any, but may want to swap out at some point, tried readability, textstat

def main():

    # Load the dataset
    load_dest = Path("./data/out/")
    f_save = load_dest / "pmid_data.csv"

    df = pd.read_csv(f_save)
    
    df['fkscore_title'] = df.apply(lambda row : pd.NA if pd.isna(row['title']) or len(row['title'])<2 else fkscore.fkscore(row['title']).score['readability'], axis=1)
    df['fkscore_abstract'] = df.apply(lambda row : pd.NA if pd.isna(row['abstract']) or len(row['abstract'])<2 else fkscore.fkscore(row['abstract']).score['readability'], axis=1)
    df['title_abstract_combined'] = df.apply(lambda row: squish_title_abstract(row['title'],row['abstract']), axis=1)
    df['fkscore_title_abstract_combined'] = df.apply(lambda row : pd.NA if pd.isna(row['title_abstract_combined']) or len(row['title_abstract_combined'])<2 else fkscore.fkscore(row['title_abstract_combined']).score['readability'], axis=1)
    
    # Group by queries for later analysis, take the mean (we dropped values)
    group_keys = ["query", "search_type", "page"]
    df_title_median = df.groupby(group_keys).fkscore_title.median()
    df_abstract_median = df.groupby(group_keys).fkscore_abstract.median()
    df_title_abstract_median = df.groupby(group_keys).fkscore_title_abstract_combined.median()

    # Save to feature set
    save_dest = Path("./data/features/")
    df_title_median.to_csv(save_dest / "readability_fk_score_title.csv")
    df_abstract_median.to_csv(save_dest / "readability_fk_score_abstract.csv")
    df_title_abstract_median.to_csv(save_dest / "readability_fk_score_title_abstract_combined.csv")

def squish_title_abstract(title, abstract):
    """
    Given a title and abstract give me a string of both, but handle nulls so if one is missing it doesn't null out.
    """
    if pd.isna(title) and pd.isna(abstract):
        return pd.NA
    elif pd.isna(title):
        return abstract
    elif pd.isna(abstract):
        return title
    else:
        return title+abstract

if __name__ == '__main__':
    main()