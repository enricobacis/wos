#!/usr/bin/env python

__all__ = ['doi_to_wos', 'query', 'single']

from xml.etree import ElementTree as _ET
from xml.dom import minidom as _minidom
import re as _re


def _get_records(wosclient, wos_query, count=5, offset=1):
    """Get the XML records for both WOS lite and premium."""
    if wosclient.is_lite():
        result = wosclient.search(wos_query, count, offset)
        pattern = r'<{0}>.*?</{0}>'.format('return')
        return _re.search(pattern, result, _re.S).group(0)
    else:
        return wosclient.search(wos_query, count, offset).records

def prettify(xml):
    xml = _minidom.parseString(xml).toprettyxml(indent=' '*4)
    return '\n'.join([line for line in xml.split('\n') if line.strip()])

def single(wosclient, wos_query, xml_query=None, count=5, offset=1):
    """Perform a single Web of Science query and then XML query the results."""
    records = _get_records(wosclient, wos_query, count, offset)
    xml = _re.sub(' xmlns="[^"]+"', '', records, count=1).encode('utf-8')
    if not xml_query: return prettify(xml)
    xml = _ET.fromstring(xml)
    return [el.text for el in xml.findall(xml_query)]


def query(wosclient, wos_query, xml_query=None, count=5, offset=1, limit=100):
    """Query Web of Science and XML query results with multiple requests."""
    results = [single(wosclient, wos_query, xml_query, min(limit, count-x+1), x)
               for x in range(offset, count+1, limit)]
    if xml_query:
        return [el for res in results for el in res]

    if wosclient.is_lite():
        pattern = _re.compile(r'.*?<return>|</return>.*', _re.DOTALL)
        res_string = '<?xml version="1.0" ?>\n<return>%s</return>'
    else:
        pattern = _re.compile(r'^<\?xml.*?\n<records>\n|\n</records>$.*')
        res_string = '<?xml version="1.0" ?>\n<records>%s</records>'
    return res_string % '\n'.join(pattern.sub('', res) for res in results)


def doi_to_wos(wosclient, doi):
    """Convert DOI to WOS identifier."""
    if wosclient.is_lite():
        raise NotImplementedError('Not implemented for WOS Lite')

    results = query(wosclient, 'DO="%s"' % doi, './REC/UID', count=1)
    return results[0].lstrip('WOS:') if results else None
