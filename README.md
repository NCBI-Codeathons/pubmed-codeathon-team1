# pubmed-codeathon-team1 
  potential team/product name - JUST RETRIEVER?

## Data info

### pmids.csv

This is a list of all the pmids for the terms we're interested in. Here's what the fields mean:

* pmid
* query - query string, read in from [./data/in/team1_search_strats_search_terms.csv](data/in/team1_search_strats_search_terms.csv) (from Travis' google doc)
* search_type - relevant | pubdate_desc
* page - 1 | 2

## Team Members

* Sruthi Chari
* Travis Hoppe
* Alex Sticco
* Alexa M. Salsbury
* Ben Rogers
* Brian Lee
* Brooks Leitner
* Caroline Trier
* Linda M. Hartman
* Marlowe Bogino
* Preeti G. Kochar
* Sridhar Papagari Sangareddy

## ABSTRACT
The goal of PubMed JUST RETRIEVER is to describe any potential biases that exist in search results based on PubMed Best Search Algorithm in comparing the retrieved results between different pages as well as to search results from a different search algorithm (date sort algorithm) . The focus for this project is to answer the following research questions:

RQ1 Author attributes by Best Match rank
Is there a correlation between various author attributes and retrieved best match search results?
RQ2 Author attributes of Best Match vs date sort
Is there a difference between search results between best search vs. date order search by author attributes?
RQ3 Article attributes by Best Match rank
Is there a correlation between various publication attributes and retrieved best match search results?
RQ4 Article attributes of Best Match vs date sort
Is there a difference between search results between best search vs. date order search by Publication Attributes?

The author attributes that were considered are: gender, race, institutional affiliation, country of origin, and author authority (e.g. research impact based on number of hits). The publication attributes that were considered are: NIH funding, language of publication, reading level, diversity of references, associated data, and number of authors and affiliations.

## BASIC WORKFLOW


