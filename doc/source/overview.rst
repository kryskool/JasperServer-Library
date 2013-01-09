.. _overview:

Overview
========

JasperServer Library use REST protocol to communicate with JasperServer for reports or BI.
This module defines classes which implement the HTTP methods (PUT, POST, DELETE, GET) and allow use basic services in JasperServer.

.. note::
   this module needs :mod:`poster` and :mod:`requests` library.


Exemple:

.. code-block:: python

    import sys
    from jasperserver import Client
    from jasperserver.admin import User
    from jasperserver.exceptions import JsException

    try:
        client = Client('http://localhost:8080/jasperserver/', 'jasperadmin', 'jasperadmin')
    except JsException:
        print 'Error Authentification FAIL!'
        sys.exit(1)

    try:
        # Must return a list with one record
        print User(client).get('joe')
    except JsException:
        print 'Error when send user query'
        sys.exit(2)

