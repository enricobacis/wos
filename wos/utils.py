#!/usr/bin/env python

__all__ = ['doi_to_wos', 'query']

from xml.etree import ElementTree as _ET
import re as _re

def query(wosclient, wos_query, xml_query, count=5):
    """Query Web of Science and then XML query the results."""
    result = wosclient.search(wos_query, count=1)
    xml = _re.sub(' xmlns="[^"]+"', '', result.records, count=1)
    results = _ET.fromstring(xml).findall(xml_query)
    return [el.text for el in results]

def doi_to_wos(wosclient, doi):
    """Convert DOI to WOS identifier."""
    results = query(wosclient, 'DO=%s' % doi, './REC/UID', count=1)
    return results[0].lstrip('WOS:') if results else None
