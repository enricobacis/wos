wos
===

*SOAP Client for querying the Web of Science database*

Description
-----------

.. image:: https://travis-ci.org/enricobacis/wos.svg?branch=master
    :target: https://travis-ci.org/enricobacis/wos

Web of Science (previously Web of Knowledge) is an online subscription-based
scientific citation indexing service maintained by Thomson Reuters.

``wos`` is a python SOAP Client (both API and command-line tool) to query the
WOS database in order to get XML data from a query using the WWS access.

Installation
------------

The package has been uploaded to `PyPI`_, so you can
install the package using pip:

    pip install wos

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
        <REC r_id_disclaimer="ResearcherID data provided by Thomson Reuters">
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

 - ``retrieve`` [`lite <http://ipscience-help.thomsonreuters.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/retrieve.html>`__ / `premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/retrieve.html>`__]

 - ``retrieveById`` [`lite <http://ipscience-help.thomsonreuters.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/retrieveById.html>`__ / `premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/retrieveById.html>`__]

 - ``search`` [`lite <http://ipscience-help.thomsonreuters.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/search.html>`__ / `premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/search.html>`__]

 - ``citedReferences`` [`premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citedReferences.html>`__]

 - ``citedReferencesRetrieve`` [`premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citedRefRetrieve.html>`__]

 - ``citingArticles`` [`premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/citingArticles.html>`__]

 - ``relatedRecords`` [`premium <http://ipscience-help.thomsonreuters.com/wosWebServicesExpanded/WebServiceOperationsGroup/WSPremiumOperations/wokSearchGroup/relatedRecords.html>`__]

[FAQ] I cannot connect ...
--------------------------

I am not affiliated with Thomson Reuters. The library leverages the Web of Science `WWS`_ API (Web Services Premium or Lite), which is a paid service offered by Thomson Reuters. This means that your institution has to pay for the Web of Science Core Collection access. The simple registration to Web of Knowledge / Web of Science does not entitle you to access the WWS API service.

So if you receive errors like ``No matches returned for Username`` or ``No matches returned for IP``, these errors are thrown directly by the WWS API server. This means that the library is correctly communicating with the server, but you do not have access to the Web Services API. I do understand that you can access the WOS website from your network, but the website access and the API access (used in this project) are two separated products, and the website access does not imply the API access, since Thomson Reuters bills them separately. This project does not scrape the website (which would violate the terms of usage) but invokes the WWS APIs offered by Thomson Reuters. Thus there is nothing this project can do to help you. 

**If you think this is an error and you should be entitled to access the services, please contact Thomson Reuters support first and verify if you have the WWS access. Please open an issue ONLY when you have (1) verified with Thomson Reuters support that you have WWS access; (2) verified that you are connected from the correct network.**


.. _PyPI: https://pypi.python.org/project/wos
.. _user_query: http://ipscience-help.thomsonreuters.com/wosWebServicesLite/WebServiceOperationsGroup/WebServiceOperations/g2/user_query.html
.. _WWS: http://wokinfo.com/products_tools/products/related/webservices/
