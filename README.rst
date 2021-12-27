wos
===

*SOAP Client for querying the Web of Science database*

Description
-----------

|travis| |readthedocs| |license| |version| |downloads| |stars|

.. |travis| image:: https://travis-ci.org/enricobacis/wos.svg?branch=master
   :target: https://travis-ci.org/enricobacis/wos
.. |readthedocs| image:: https://readthedocs.org/projects/wos/badge/
   :target: https://wos.readthedocs.io/
.. |license| image:: https://img.shields.io/github/license/enricobacis/wos
   :target: https://github.com/enricobacis/wos/blob/master/LICENSE
.. |version| image:: https://img.shields.io/pypi/v/wos?color=blue
   :target: https://pypi.org/project/wos/
.. |downloads| image:: https://img.shields.io/pypi/dm/wos
   :target: https://pypi.org/project/wos/
.. |stars| image:: https://img.shields.io/github/stars/enricobacis/wos?style=social
   :target: https://github.com/enricobacis/wos

Web of Science (previously Web of Knowledge) is an online subscription-based
scientific citation indexing service maintained by Clarivate.

``wos`` is a python SOAP Client (both API and command-line tool) to query the
WOS database in order to get XML data from a query using the WWS access.

Installation
------------

The package has been uploaded to `PyPI`_, so you can
install the package using pip:

    pip install wos

Documentation
-------------

This README and the documentation for the classes and methods can be accessed
on `ReadTheDocs`_.

Usage
-----

You can use the ``wos`` command to query the Web of Science API. If you want to
access data that needs to be accessed using the premium API, you also have to
authenticate using your username and password.


    usage: wos [-h] [--close] [-l] [-u USER] [-p PASSWORD] [-s SID]
               {query,doi,connect} ...

    Query the Web of Science.

    positional arguments:
      {query,doi,connect}   sub-command help
        query               query the Web of Science.
        doi                 get the WOS ID from the DOI.
        connect             connect and get an SID.

    optional arguments:
      -h, --help            show this help message and exit
      --close               Close session.
      --proxy PROXY         HTTP proxy
      --timeout TIMEOUT     API timeout
      -l, --lite            Wos Lite
      -v, --verbose         Verbose

    authentication:
      API credentials for premium access.

      -u USER, --user USER
      -p PASSWORD, --password PASSWORD
      -s SID, --sid SID

You can use the WOS Lite API using the ``--lite`` parameter (for each query).

You can also authenticate using the session id (SID). In fact the sessions are
not closed by the command line utility. Example:

.. code::

    $ wos --user JohnDoe --password 12345 connect
    Authenticated using SID: ABCDEFGHIJKLM

    $ wos --sid ABCDEFGHIJKLM query 'AU=Knuth Donald' -c1
    Authenticated using SID: ABCDEFGHIJKLM
    <?xml version="1.0" ?>
    <records>
        <REC r_id_disclaimer="ResearcherID data provided by Clarivate Analytics">
            <UID>WOS:000287850200007</UID>
            <static_data>
                <summary>
                    <EWUID>
                        <WUID coll_id="WOS"/>
                        <edition value="WOS.SCI"/>
                    </EWUID>
                    <pub_info coverdate="MAR 2011" has_abstract="N" issue="1"
                              pubmonth="MAR" pubtype="Journal" pubyear="2011"
                              sortdate="2011-03-01" vol="33">
                        <page begin="33" end="45" page_count="13">33-45</page>
                    </pub_info>
                    <titles count="6">
                        <title type="source">MATHEMATICAL INTELLIGENCER</title>
    ....

    $ wos --sid ABCDEFGHIJKLM doi '10.1007/s00283-010-9170-7'
    10.1007/s00283-010-9170-7

Check the `user_query`_ documentation to understand how to create query strings.

Example
-------

Obviously you can also use the python client programmatically:

.. code:: python

    from wos import WosClient
    import wos.utils

    with WosClient('JohnDoe', '12345') as client:
        print(wos.utils.query(client, 'AU=Knuth Donald'))

APIs
----

In ``wos`` 0.1.11+, the ``WosClient`` class can access the following APIs.

 - ``retrieve`` [`lite <https://help.incites.clarivate.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/retrieve.html>`__ / `premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/retrieve.html>`__]

 - ``retrieveById`` [`lite <https://help.incites.clarivate.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/retrieveById.html>`__ / `premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/retrieveById.html>`__]

 - ``search`` [`lite <https://help.incites.clarivate.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/search.html>`__ / `premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/search.html>`__]

 - ``citedReferences`` [`premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citedReferences.html>`__]

 - ``citedReferencesRetrieve`` [`premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citedRefRetrieve.html>`__]

 - ``citingArticles`` [`premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citingArticles.html>`__]

 - ``relatedRecords`` [`premium <https://help.incites.clarivate.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/relatedRecords.html>`__]

[FAQ] I cannot connect ...
--------------------------

I am not affiliated with Clarivate. The library leverages the Web of Science `WWS`_ API (Web Services Premium or Lite), which is a paid service offered by Clarivate. This means that your institution has to pay for the Web of Science Core Collection access. The simple registration to Web of Knowledge / Web of Science does not entitle you to access the WWS API service.

So if you receive errors like ``No matches returned for Username`` or ``No matches returned for IP``, these errors are thrown directly by the WWS API server. This means that the library is correctly communicating with the server, but you do not have access to the Web Services API. I do understand that you can access the WOS website from your network, but the website access and the API access (used in this project) are two separated products, and the website access does not imply the API access, since Clarivate bills them separately. This project does not scrape the website (which would violate the terms of usage) but invokes the WWS APIs offered by Clarivate. Thus there is nothing this project can do to help you.

**If you think this is an error and you should be entitled to access the services, please contact Clarivate support first and verify if you have the WWS access. Please open an issue ONLY when you have (1) verified with Clarivate support that you have WWS access; (2) verified that you are connected from the correct network.**

Disclaimer
----------

All product names, trademarks, and registered trademarks are the property of their respective owners. All company, product, and service names used in this document are for identification purposes only. The use of these names, trademarks, and brands do not constitute an endorsement or recommendation by the companies.


.. _ReadTheDocs: https://wos.readthedocs.io/
.. _PyPI: https://pypi.python.org/project/wos
.. _user_query: https://help.incites.clarivate.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/user_query.html
.. _WWS: https://clarivate.com/webofsciencegroup/solutions/xml-and-apis/

