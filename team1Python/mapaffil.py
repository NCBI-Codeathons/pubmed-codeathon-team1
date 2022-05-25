
from bs4 import BeautifulSoup
import requests


def mapaffil(pmid):
    url = "http://abel.lis.illinois.edu/cgi-bin/mapaffil/search.pl?desired_offset=0&desired_row_cnt=10&pmid={}&year=&affiliation=&found_str=&country=&state=".format(pmid)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find('table')
    table_body = table.find('tbody')
    first_row = table_body.find_all('tr')[0]

    d = {}
    header = ["pmid", "year", "affiliation", "insti",
              "ambig", "extract", "country", "state", "geocode"]
    for id, ele in zip(header, first_row.find_all('td')):
        d.update({id: ele.text.strip()})

    return d



