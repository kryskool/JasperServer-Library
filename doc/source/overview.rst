.. _overview:

Overview
========

JasperServer Library use REST protocol to communicate with JasperServer for reports or BI.
This module defines classes which implement the HTTP methods (PUT, POST, DELETE, GET) and allow use basic services in JasperServer.

.. note::
   this module needs :mod:`requests` library.


Exemple:

.. code-block:: python

    import sys
    from jasperserver import Client
    from jasperserver.services import Resources
    from jasperserver.exceptions import JsException

    try:
        client = Client('http://localhost:8080/jasperserver/', 'jasperadmin', 'jasperadmin')
    except JsException:
        print 'Error Authentification FAIL!'
        sys.exit(1)

    try:
        # Must return a list with one record
        print Resources(client).search()
    except JsException:
        print 'Error when send search query'
        sys.exit(2)

