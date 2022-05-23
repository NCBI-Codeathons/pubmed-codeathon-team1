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

def main():
    Entrez.email = 'brian.lee@cdc.gov'

    handle = Entrez.esearch(db='pubmed', 
                            retmax='10',
                            retmode='xml', 
                            term='asthma')
    papers = Entrez.read(handle)
    print(papers)
    print('Number of results: ' + papers['Count']) #this is off from the preview server and GUI
    #can't figure out how to have this package use the preview/beta search so the counts match the GUI, it seems hard coded in the python package https://github.com/biopython/biopython/blob/5a675c1bf7ef6cca0de5541c672d2a9aec537946/Bio/Entrez/__init__.py#L237

if __name__ == '__main__':
    main()

