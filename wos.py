#!/usr/bin/env python

from suds.client import Client

class WosClient():
    """Query the Web of Science.
       You must provide username and password only to user premium WWS service.

       with WosClient() as wos:
           results = wos.search(...)"""

    auth_url = 'http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl'
    search_url = 'http://search.webofknowledge.com/esti/wokmws/ws/WokSearch?wsdl'

    def __init__(self, username=None, password=None):
        """Create the SOAP clients. username and password for premium access."""
        self._auth = Client(self.auth_url)
        self._search = Client(self.search_url)
        self._open = False

        if username and password:
            authorization = ('%s:%s' % (username, password)).encode('base64')
            headers = {'Authorization': ('Basic %s' % authorization).strip()}
            self._auth.set_options(headers=headers)

    def __enter__(self):
        """Automatically connect when used with 'with' statements."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection after closing the 'with' statement."""
        self.close()

    def __del__(self):
        """Close connection when deleting the object."""
        self.close()

    def connect(self):
        """Authenticate to WOS and set the SID cookie."""
        SID = self._auth.service.authenticate()
        self._search.set_options(headers={'Cookie': 'SID="%s"' % SID})
        self._auth.options.headers.update({'Cookie': 'SID="%s"' % SID})
        self._open = True

    def close(self):
        """Close the session."""
        if self._open:
            self._auth.service.closeSession()
            self._open = False

    def search(self, query, count=5):
        """Perform a query. Check the WOS documentation for v3 syntax."""
        if not self._open:
            raise RuntimeError('Session not open. Invoke .connect() before.')

        qparams = {'databaseId': 'WOS',
                   'userQuery': query,
                   'queryLanguage': 'en'}

        rparams = {'firstRecord': 1,
                   'count': count,
                   'sortField': {'name': 'RS', 'sort': 'D'}}

        return self._search.service.search(qparams, rparams)
