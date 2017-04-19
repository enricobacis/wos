#!/usr/bin/env python

__all__ = ['WosClient']

import suds as _suds
import functools as _functools
from base64 import b64encode as _b64encode
from collections import OrderedDict as _OrderedDict

class WosClient():
    """Query the Web of Science.
       You must provide user and password only to user premium WWS service.

       with WosClient() as wos:
           results = wos.search(...)"""

    base_url = 'http://search.webofknowledge.com'
    auth_url = base_url + '/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
    search_url = base_url + '/esti/wokmws/ws/WokSearch?wsdl'
    searchlite_url = base_url + '/esti/wokmws/ws/WokSearchLite?wsdl'

    def __init__(self, user=None, password=None, SID=None, close_on_exit=True,
                 lite=False, proxy=None):
        """Create the SOAP clients. user and password for premium access."""

        self._SID = SID
        self._lite = lite
        self._close_on_exit = close_on_exit
        proxy = {'http': proxy} if proxy else None
        search_wsdl = self.searchlite_url if lite else self.search_url
        self._auth = _suds.client.Client(self.auth_url, proxy=proxy)
        self._search = _suds.client.Client(search_wsdl, proxy=proxy)

        if user and password:
            auth = '%s:%s' % (user, password)
            auth = _b64encode(auth.encode('utf-8')).decode('utf-8')
            headers = {'Authorization': ('Basic %s' % auth).strip()}
            self._auth.set_options(headers=headers)

    def __enter__(self):
        """Automatically connect when used with 'with' statements."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection after closing the 'with' statement."""
        if self._close_on_exit:
            self.close()

    def __del__(self):
        """Close connection when deleting the object."""
        if self._close_on_exit:
            self.close()

    def _api(fn):
        """API decorator for common tests (sessions open, etc.)."""
        @_functools.wraps(fn)
        def _fn(self, *args, **kwargs):
            if not self._SID:
                raise RuntimeError('Session not open. Invoke connect() before.')
            return fn(self, *args, **kwargs)
        return _fn

    def _premium(fn):
        """Premium decorator for APIs that require premium access level."""
        @_functools.wraps(fn)
        def _fn(self, *args, **kwargs):
            if self._lite:
                raise RuntimeError('Premium API, not available in lite access.')
            return fn(self, *args, **kwargs)
        return _fn

    def connect(self):
        """Authenticate to WOS and set the SID cookie."""
        if not self._SID:
            self._SID = self._auth.service.authenticate()
            print('Authenticated (SID: %s)' % self._SID)

        self._search.set_options(headers={'Cookie': 'SID="%s"' % self._SID})
        self._auth.options.headers.update({'Cookie': 'SID="%s"' % self._SID})
        return self._SID

    def close(self):
        """Close the session."""
        if self._SID:
            self._auth.service.closeSession()
            self._SID = None

    @_api
    def search(self, query, count=5, offset=1):
        """Perform a query. Check the WOS documentation for v3 syntax."""
        return self._search.service.search(
                queryParameters=_OrderedDict([
                    ('databaseId', 'WOS'),
                    ('userQuery', query),
                    ('queryLanguage', 'en')
                ]),
                retrieveParameters=_OrderedDict([
                    ('firstRecord', offset),
                    ('count', count),
                    ('sortField', _OrderedDict([('name', 'RS'), ('sort', 'D')]))
                ])
        )

    @_api
    @_premium
    def citedReferences(self, uid, count=100, offset=1):
        """Get cited references from wos uid. Check WOS v3 documentation."""
        return self._search.service.citedReferences(
                databaseId='WOS',
                uid=uid,
                queryLanguage='en',
                retrieveParameters=_OrderedDict([
                    ('firstRecord', offset),
                    ('count', count),
                    ('sortField', _OrderedDict([('name', 'RS'), ('sort', 'D')]))
                ])
        )
