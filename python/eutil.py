# From Team 4

from requests.adapters import HTTPAdapter
from urllib.parse import quote
from types import MethodType
import re
from collections import OrderedDict
from lxml import etree
from io import BytesIO

from tokenbucket import RateLimitedSession


# Hostname for eutils
EUTILS_PREFIX = 'https://eutilspreview.ncbi.nlm.nih.gov/entrez'

# Base URL for eutils
EUTILS_URL = '{}/eutils/{}'


def process_medline_record(rawrecord):
    result = OrderedDict()
    expr = re.compile(r'^([A-Z]+) *- (.*)$')
    cont = re.compile(r'^      (.*)$')
    key = None
    for line in rawrecord.split('\n'):
        m = expr.match(line)
        if m:
            key = m.group(1)
            value = m.group(2)
            if key in result:
                result[key].append(value)
            else:
                result[key] = [value]
        else:
            m = cont.match(line)
            if m:
                contvalue = m.group(1)
                result[key][-1] += contvalue
    return result


def process_medline(data):
    """
    Breaks up the content of an efetch response in medline format into multiple records,
    each with multiple felds
    """
    records = []
    for rawrecord in data.split('\n\n'):
        records.append(process_medline_record(rawrecord))
    return records


def extract_medline(self):
    """
    Monkey patch for response of efetch
    :param self: instance of response
    :return: records
    """
    return process_medline(self.content.decode('utf-8'))


def extract_xml(self):
    """
    Monkey patch for parsing XML response
    :param self: instance of response
    :return: records
    """
    return etree.parse(BytesIO(self.content))


class EUtils(object):
    """
    An abstraction that wraps the NCBI E-Utilities
    """
    def __init__(self, apikey=None, email=None, rate=3, prefix=None, session=None):
        self.apikey = apikey
        self.email = email
        self.rate = rate
        self.prefix = prefix if prefix else EUTILS_PREFIX
        if not session:
            session = RateLimitedSession(rate=rate, tokens=rate, capacity=rate)
            session.mount('https://', HTTPAdapter(max_retries=3, pool_maxsize=10))
        self.session = session

    def params(self, db=None, **kwargs):
        params = dict((k,v) for k,v in kwargs.items())
        if db:
            params['db'] = db
        if self.apikey:
            params['api_key'] = self.apikey
        return '&'.join('{}={}'.format(key, quote(value)) for key, value in params.items())

    def einfo(self, db=None, **kwargs):
        url = EUTILS_URL.format(self.prefix, 'einfo.fcgi') + '?' + self.params(db, **kwargs)
        r = self.session.get(url)
        r.xml = MethodType(extract_xml, r)
        return r

    def esearch(self, db, **kwargs):
        url = EUTILS_URL.format(self.prefix, 'esearch.fcgi') + '?' + self.params(db, **kwargs)
        print("url", url)
        r = self.session.get(url)
        r.xml = MethodType(extract_xml, r)
        return r

    def efetch(self, db, *args, **kwargs):
        if len(args) > 0:
            idlist = ','.join(str(arg) for arg in args)
            params = self.params(db, id=idlist, **kwargs)
        else:
            params = self.params(db, **kwargs)
        url = EUTILS_URL.format(self.prefix, 'efetch.fcgi') + '?' + params
        r = self.session.get(url)
        r.xml = MethodType(extract_xml, r)
        if kwargs.get('rettype', '') == 'medline':
            r.medline = MethodType(extract_medline, r)
        return r