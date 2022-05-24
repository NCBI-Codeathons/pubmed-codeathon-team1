# I can't get this file to work, so I went over to ../notebooks/fetch_articles_from_pmids.ipynb
import pandas as pd
from eutil import EUtils
from diagnose import print_element
import math
from tqdm import tqdm

import sys
sys.path.append('./teamp1Python')

eutils = EUtils(
        '8d4c4f67f2a663e9d0ef6ed4d60a4eedd609',  # API key
        'brian.lee@cdc.gov',  # Email address - unused
        20,  # API calls per second
        'https://eutilspreview.ncbi.nlm.nih.gov/entrez'
        # URL prefix for preview - normally not needed
    )

def main():

#csv: pmid, query, search_type, page
#   search_type: best_match, pub_date
#   query:
#   pmid:
#   page: 1, 2
#df = pd.DataFrame(columns=["pmid", "query", "search_type", "page"])

    print("iterating through designated queries")
    df_pmids = pd.read_csv("../data/out/pmids.csv")
    for pmid in tqdm(df_term["pmid"]):
        print(pmid)


if __name__ == '__main__':
    main()

