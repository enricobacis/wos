#!/usr/bin/env python

__all__ = ['doi_to_wos', 'query', 'single']

from xml.etree import ElementTree as _ET
from xml.dom import minidom as _minidom
import re as _re

def single(wosclient, wos_query, xml_query=None, count=5, offset=1):
    """Perform a single Web of Science query and then XML query the results."""
    result = wosclient.search(wos_query, count, offset)
    xml = _re.sub(' xmlns="[^"]+"', '', result.records, count=1).encode('utf-8')
    if xml_query:
        xml = _ET.fromstring(xml)
        return [el.text for el in xml.findall(xml_query)]
    else:
        return _minidom.parseString(xml).toprettyxml()

def query(wosclient, wos_query, xml_query=None, count=5, offset=1, limit=100):
    """Query Web of Science and XML query results with multiple requests."""
    results = [single(wosclient, wos_query, xml_query, min(limit, count-x+1), x)
               for x in range(offset, count+1, limit)]
    if xml_query:
        return [el for res in results for el in res]
    else:
        pattern = _re.compile(r'.*?<records>|</records>.*', _re.DOTALL)
        return ('<?xml version="1.0" ?>\n<records>' +
                '\n'.join(pattern.sub('', res) for res in results) +
                '</records>')

def doi_to_wos(wosclient, doi):
    """Convert DOI to WOS identifier."""
    results = query(wosclient, 'DO=%s' % doi, './REC/UID', count=1)
    return results[0].lstrip('WOS:') if results else None
