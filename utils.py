from xml.etree import ElementTree as ET
from config import username, password
from wos import WosClient
from re import sub

def query(wosclient, wos_query, xml_query, count=5):
    result = wosclient.search(wos_query, count=1)
    xml = sub(' xmlns="[^"]+"', '', result.records, count=1)
    results = ET.fromstring(xml).findall(xml_query)
    return [el.text for el in results]

def doi_to_wos(wosclient, doi):
    results = query(wosclient, 'DO=%s' % doi, './REC/UID', count=1)
    return results[0].lstrip('WOS:') if results else None

if __name__ == '__main__':
    with WosClient(username=username, password=password) as wos:
        print doi_to_wos(wos, '10.1145/2180861.2180863')
