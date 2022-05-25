
"""
Author: Caroline Trier, Trier_Caroline@bah.com

Web scraper for tool for http://abel.lis.illinois.edu/cgi-bin/mapaffil/search.pl
Torvik VI (2015). MapAffil: A bibliographic tool for mapping author affiliation
strings to cities and their geocodes worldwide. D-Lib Magazine, 21(11/12).
"""
from bs4 import BeautifulSoup
import requests


def mapaffil(pmid):
    """

    :param pmid: pubmed id string
    :return: dictionary of information on the first author's institutional
    affiliation and location, empty dict if mapaffil returns nothing
    """
    url = "http://abel.lis.illinois.edu/cgi-bin/mapaffil/search.pl?desired_offset=0&desired_row_cnt=10&pmid={}&year=&affiliation=&found_str=&country=&state=".format(pmid)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('table')
    table_body = table.find('tbody')
    d = {}

    if table_body:
        first_row = table_body.find_all('tr')[0]

        header = ["pmid", "year", "affiliation", "insti",
                "ambig", "extract", "country", "state", "geocode"]
        for id, ele in zip(header, first_row.find_all('td')):
            d.update({id: ele.text.strip()})

    return d



