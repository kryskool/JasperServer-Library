============
JasperServer
============

The goal of this project is to create a JasperServer REST client for Python.

Exemple
-------

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


