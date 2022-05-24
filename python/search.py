import pandas as pd
from eutil import EUtils
from diagnose import print_element
import math
from tqdm import tqdm


eutils = EUtils(
        '8d4c4f67f2a663e9d0ef6ed4d60a4eedd609',  # API key
        'brian.lee@cdc.gov',  # Email address - unused
        20,  # API calls per second
        'https://eutilspreview.ncbi.nlm.nih.gov/entrez'
        # URL prefix for preview - normally not needed
    )


def paginate(idx):
    """

    :param idx:
    :return:
    """
    page_len = 10
    return math.floor(idx/page_len) + 1


def search(query, search_type):
    """

    :param query:
    :param search_type:
    :return:
    """
    docs = []
    r = eutils.esearch(db='pubmed',
                       retmax='20',
                       retmode='xml',
                       term=query,
                       sort=search_type)
    #print_element(r.xml(), "\n")
    pmids = [element.text for element in r.xml().xpath('//IdList/Id')]

    for idx, pmid in enumerate(pmids):
        docs.append({"pmid": pmid,
                     "query": query,
                     "search_type": search_type,
                     "page": paginate(idx)})
    return pd.DataFrame(docs)


def main():

    #csv: pmid, query, search_type, page
    #   search_type: best_match, pub_date
    #   query:
    #   pmid:
    #   page: 1, 2
    df = pd.DataFrame(columns=["pmid", "query", "search_type", "page"])

    print("iterating through designated queries")
    df_term = pd.read_csv("../data/in/team1_search_strats_search_terms.csv")
    for query in tqdm(df_term["Query"]):
        df = pd.concat([df,
                        search(query, search_type="relevance"),
                        search(query, search_type="pubdate_desc")],
                        ignore_index=True)
        df.to_csv("../data/out/pmids.csv", index=False)


if __name__ == '__main__':
    main()

