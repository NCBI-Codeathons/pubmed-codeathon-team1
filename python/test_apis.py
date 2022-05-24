#conda create --name pubmed python=3.9
#pip install biopython
#testing entrez with 3 search terms: asthma, pubmed best match, monkeypox
#the GUI is the gold standard so we will compare the web search results with the eutils results with the python package
# test #1 asthma
#   web (207013 results)- https://pubmed.ncbi.nlm.nih.gov/?term=asthma
#   eutils api (207013 results)- https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=asthma&sort=relevance&retmax=10
# test #2 pubmed best match
#   web (150)- https://pubmed.ncbi.nlm.nih.gov/?term=pubmed+best+match
#   eutils api (150)- https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=pubmed+best+match&sort=relevance&retmax=10
# test #3 monkeypox
#   web (864)- https://pubmed.ncbi.nlm.nih.gov/?term=monkeypox
#   eutils api(864)- https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=monkeypox&sort=relevance&retmax=10
#
# package docs- https://biopython.org/docs/1.75/api/Bio.Entrez.html

from Bio import Entrez
from eutil import EUtils
from diagnose import print_element


def main():

    # Entrez results
    Entrez.email = 'brian.lee@cdc.gov'

    handle = Entrez.esearch(db='pubmed', 
                            retmax='10',
                            retmode='xml', 
                            term='pubmed best match',
                            sort='relevance')
    papers = Entrez.read(handle)
    print(papers, "\n")

    # Team 4 approach
    eutils = EUtils(
        '8d4c4f67f2a663e9d0ef6ed4d60a4eedd609',  # API key
        'dansmood@gmail.com',  # Email address - unused
        10,  # API calls per second
        'https://eutilspreview.ncbi.nlm.nih.gov/entrez'
        # URL prefix for preview - normally not needed
    )

    r = eutils.esearch(db='pubmed',
                       retmax='10',
                       retmode='xml',
                       term='pubmed best match',
                       sort='relevance')
    print_element(r.xml(), "\n")


if __name__ == '__main__':
    main()

