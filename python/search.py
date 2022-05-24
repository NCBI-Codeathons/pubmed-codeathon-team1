import pandas as pd
from eutil import EUtils
from diagnose import print_element


def main():

    eutils = EUtils(
        '8d4c4f67f2a663e9d0ef6ed4d60a4eedd609',  # API key
        'brian.lee@cdc.gov',  # Email address - unused
        20,  # API calls per second
        'https://eutilspreview.ncbi.nlm.nih.gov/entrez'
        # URL prefix for preview - normally not needed
    )



    #csv: pmid, query, search_type, page
    #   search_type: best_match, pub_date
    #   query:
    #   pmid:
    #   page: 1, 2
    df = pd.Dataframe(cols=["pmid", "query", "search_type", "page"])

    #read in queries from list
    df_term = pd.from_csv("")
    for query in queries:

        handle = Entrez.esearch(db='pubmed',
                            retmax='20',
                            retmode='xml', 
                            term='pubmed best match',
                            sort='relevance')
        papers = Entrez.read(handle)
        print(papers, "\n")

        for result in paper:
            row = {}
            pmids = [element.text for element in doc.xpath('//IdList/Id')]

        # divide pg 1 and 2



    # Team 4 approach


    r = eutils.esearch(db='pubmed',
                       retmax='10',
                       retmode='xml',
                       term='pubmed best match',
                       sort='relevance')
    print_element(r.xml(), "\n")
    doc = r.xml()


if __name__ == '__main__':
    main()

