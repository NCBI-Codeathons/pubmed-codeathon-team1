# take the list of all the pmid xmls and make easier to use json files

import pubmed_parser as pp
from lxml import etree
from Bio import Entrez
Entrez.email = 'brian.lee@cdc.gov'

def main():
    #dict_out = pp.parse_pubmed_xml('./data/out/pmid_xmls/61455.xml')
    path = './data/out/pmid_xmls/61455.xml'
    tree = etree.parse(path)
    print('hello')
    print(tree.find('.//ArticleId[@IdType="pubmed"]').text)

    res = Entrez.efetch(db="pubmed", id='61455', retmode="xml")
    print(res.read())

    print(tree.find(".//title-group/article-title"))

if __name__ == '__main__':
    main()