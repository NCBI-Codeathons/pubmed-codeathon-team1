# -*- coding: utf-8 -*-
"""
Created on Wed May 25 17:36:50 2022

@author: sticcojc
"""
import pandas as pd
import os
import re
import numpy as np
from  medline_parser import parse_medline_xml, parse_medline_grant_id
from utils import read_xml

#%% prep list of xml files
files = os.listdir('pmid_xmls')
filepath = "pmid_xmls/{}"

#%% strip blank lines at the end of xml files and correct encoding
def strip_blanks(files):
    for file in files:
        with open(filepath.format(file), encoding = 'ISO-8859-1') as f_input:
            data = f_input.read().rstrip('\n')
        with open(filepath.format(file), 'w', encoding = 'utf-8') as f_output:    
            f_output.write(data)

#strip_blanks(files) #only needs to be run once
#%% Find files where xml has been accidentally duplicated
problems = []
for file in files:
    with open(filepath.format(file), encoding = 'utf-8') as f:
        data = f.read()
        doctypes = data.count('!DOCTYPE')
        if doctypes > 1:
            problems.append(file)
#%% Delete duplicated XML
for file in problems:
    with open(filepath.format(file), encoding = 'utf-8') as f:
        data = f.read()
        splits = re.split(r'(</PubmedArticleSet>)', data)
        keep = splits[0]+splits[1]
    with open(filepath.format(file), 'w', encoding = 'utf-8') as f_output:    
        f_output.write(keep)   
#%% parse xml for each file
pubmed_data = [parse_medline_xml(filepath.format(file), author_list=True) for file in files]
#%% remove empty rows
data_revised = [row for row in pubmed_data if row != []]
data_revised = [row[0] for row in data_revised]
#%% convert to dataframe
colnames = ["title",
            "abstract",
            "journal",
            "authors",
            "affiliations",
            "pubdate",
            "pmid",
            "doi",
            "other_id",
            "pmc",
            "mesh_terms",
            "keywords",
            "publication_types",
            "chemical_list",
            "delete",
            "medline_ta",
            "nlm_unique_id",
            "issn_linking",
            "country",
            "references",
            "issue",
            "pages",
            "languages",
            "vernacular_title"]
df = pd.DataFrame(data_revised, columns = colnames)
df = df[['pmid', 'title', 'abstract', 'nlm_unique_id', 'authors', 'affiliations', 'pubdate', 
         'publication_types', 'languages']]
#%% parse grants info out for each file and remove empty rows
grants_data = [parse_medline_grant_id(filepath.format(file)) for file in files]
grants_revised = [row for row in grants_data if row != []]
grants_revised = [row[0] for row in grants_revised]

#%% convert to dataframe
grants_df = pd.DataFrame(grants_revised)
#%%
data_df = pd.merge(df, grants_df, 'left', on = 'pmid')
#%% set null values to empty strings to avoid NaN problems
data_df = data_df.fillna('')
#%% Set funding status based on publication type entries
"""
Possible funding tags: 
    All US Gov:
        'D057689:Research Support, U.S. Government'
        "D013487:Research Support, U.S. Gov't, P.H.S." 
        'D052060:Research Support, N.I.H., Intramural'
        'D052061:Research Support, N.I.H., Extramural'
        "D013486:Research Support, U.S. Gov't, Non-P.H.S."
        "D057666:Research Support, American Recovery and Reinvestment Act"
    Non US-Gov
        "D013485:Research Support, Non-U.S. Gov't"
Note that Non US-Gov includes non-federal American sources 
(societies, institutes, state governments, universities, private organizations, etc.) 
as well as foreign sources 
(national, departmental, provincial, academic & private organizations, etc)
"""
us_gov = re.compile("D057689|D013487|D013487|D052060|D052061|D013486|D057666")

data_df['us_gov_funding'] = np.where(data_df['publication_types'].str.contains(us_gov), True, False) 
data_df['other_funding'] = np.where(data_df['publication_types'].str.contains("D013485"), True, False) 

#%% Clarify column names
data_df = data_df.rename(columns = {'country':'grant_country', 'agency':'grant_agency'})

#%% Update funding status based on grant data
data_df.loc[data_df.grant_country == "United States", 'us_gov_funding'] = True
data_df['other_funding'] = np.where(((data_df.grant_country != "United States") & (data_df.grant_country != "" )), True, data_df['test'])

#%% Simplify and export to csv
data_df = data_df[['pmid', 'publication_types', 'grant_id','grant_acronym', 
                  'grant_country', 'grant_agency', 'us_gov_funding','other_funding']]
data_df.to_csv('funding_data.tsv', sep = '\t', index=False)

#%% Check for covid terms in TIAB
pattern = re.compile(r'SARS Coronavirus 2|SARS-CoV-2|SARS-CoV2|COVID-19|COVID 19|2019 Novel Coronavirus|2019-nCoV',
                     flags=re.I)
df['covid'] = np.where(((df.title.str.contains(pattern)) | (df.abstract.str.contains(pattern))), True, False)
covid = df[['pmid', 'covid']]
data_df = pd.merge(data_df, covid, 'left', on = 'pmid')

data_df.to_csv('funding_and_covid_data.tsv', sep = '\t', index=False)







