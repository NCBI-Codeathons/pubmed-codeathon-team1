import pandas as pd
from pathlib import Path

# Custom module that extends pandas to help download PMID data
import bibcodex

# Load the pmid list into memory
save_dest = Path("../data/out/")
f_pmids = save_dest / "pmids.csv"

# Set the PMIDs to string type (needed by bibcodex)
df = pd.read_csv(f_pmids, dtype={"pmid": str}).set_index("pmid")

icite_columns = [
    "relative_citation_ratio",  # RCR measure of influence
    "human",  # Prediction from MeSH on human subject
    "animal",  # Prediction from MeSH on animal subjects
    "molecular_cellular",  # Prediction from MeSH on cellular subjects
    "apt",  # Approx. potential to clinically translate
    "is_clinical",  # Bool, clinical or guideline
    "citation_count",  # Raw # of citations
    "cited_by",  # PMIDs of citations
    "references",  # PMIDs of references
]

# Download and copy data into the dataframe (only use selected columns)
info1 = df.bibcodex.download("icite")
for col in icite_columns:
    df[col] = info1[col]

info2 = df.bibcodex.download("pubmed")
pubmed_columns = [
    "title",
    "abstract",
    "journal",
    "authors",
    "affiliations",
    "pubdate",
    "mesh_terms",
    "publication_types",
    "chemical_list",
    "keywords",
    "languages",
    "country",
]

# Download and copy data into the dataframe (only use selected columns)
for col in pubmed_columns:
    df[col] = info2[col]

# Save the data into the 'data/out' directory
f_save = save_dest / "pmid_data.csv"
df.to_csv(f_save)

print(df)
