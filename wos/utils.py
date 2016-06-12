#!/usr/bin/env python

__all__ = ['doi_to_wos', 'query']

from xml.etree import ElementTree as _ET
from xml.dom import minidom as _minidom
import re as _re

def query(wosclient, wos_query, xml_query=None, count=5, offset=1):
    """Query Web of Science and then XML query the results."""
    # wos returns 100 documents metadata per query.
    limit_per_query=100
    results = []

    _count = count
    _offset = offset

    while _count > 0:
        num_results = min(limit_per_query, _count)
        result = wosclient.search(wos_query, num_results, _offset)
        _count -= num_results
        _offset += num_results

        xml = _re.sub(' xmlns="[^"]+"', '', result.records, count=1)
        results.append(xml)

    # remove <records> </records> tags and concat the result with them later
    results = map (lambda x: x.replace('<records>', ''), results)
    results = map (lambda x: x.replace('</records>', ''), results)
    results = u'<records>\n' + reduce (lambda s, elem: s + elem + '\n', results, u'') + u'</records>'

    if xml_query:
        xml = _ET.fromstring(xml)
        return [el.text for el in xml.findall(xml_query)]
    else:
        return _minidom.parseString(xml).toprettyxml()

def doi_to_wos(wosclient, doi):
    """Convert DOI to WOS identifier."""
    results = query(wosclient, 'DO=%s' % doi, './REC/UID', count=1)
    return results[0].lstrip('WOS:') if results else None
