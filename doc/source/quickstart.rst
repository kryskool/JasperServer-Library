QuickStart
**********

JasperServer Library use REST protocol to communicate with JasperServer for reports or BI.
This module defines classes which implement the HTTP methods (PUT, POST, DELETE, GET) and allow use basic services in JasperServer.

First, make sure that the Requests library is installed ::

    >>> pip install requests


Let's get started with some examples

Opening a session
=================

To make an HTTP request in JasperReport Server, you must be connected to JRS 

.. code-block:: python

    >>> from jasperserver.rest import Client
    >>> client = Client('http://localhost:8080/jasperserver', 'jasperadmin', 'jasperadmin')
    

You have a Client object. Now, we can get all REST method from this open session.


Searching an existent User or Role
==================================

You can browse for all user

.. code-block:: python

    >>> from jasperserver.admin import User, Role
    >>> users = User(client).search()
    >>> users
    [{'username': 'anonymousUser', 'fullName': 'anonymousUser', 'enabled': 'true', 'roles': ['ROLE_ANONYMOUS']}, ...
    
    
Or search by terms

.. code-block:: python

    >>> users = User(client).search('joe')
    >>> users
    [{'username': 'joeuser', 'fullName': 'Joe User', 'enabled': 'true', 'roles': ['ROLE_USER']}]
    

and you can do the same with the Role service

.. code-block:: python

    >>> role = Role(client).search()
    >>> role
    ['ROLE_ADMINISTRATOR', 'ROLE_ANONYMOUS', 'ROLE_USER']
    

Searching Resources
===================

If you want listed all existent resources in JRS in a specified path, you could follow this example :

.. code-block:: python

    >>> from jasperserver.services import Resources
    >>> Resources(client, '/openerp/bases/openerp_demo').search('Product')
    
You'll obtain a list with all resources containing the specified terms.

    
Create, Modify or Delete a Content
==================================

To create or modify you must instanciate a Resource object with the working directory.
Keep in mind, you need sufficient permission to send this following requests.

.. code-block:: python

    >>> from jasperserver.services import Resource
    >>> jrxml = Resource(client, '/openerp/bases/reports')
    
And send your query (with or without attached file) to JRS like this :

.. code-block:: python

    >>> srcfile_path = '/the/local/file/resource/path/'
    >>> resource_name = 'myresource'
    >>> rtype = 'jrxml'
    >>> jrxml.create(resource_name, rtype, path_fileresource=srcfile_path)
    
To modify it (eventually !):

.. code-block:: python

    >>> jrxml.modify(resource_name, rtype, path_fileresource=srcfile_path)
    
Ah, you don't need it anymore :

.. code-block:: python

    >>> jrxml.delete(resource_name)
    
If your resource is a reference to another one, you won't be able to delete it.

The Report Unit Case
====================

Report Unit is a more complicated resource in wich there a several resource as datasources and jrxml.

So, to create a report unit just modify some informations to add it, as a datasource corresponding to jdbc source and the jrxml resource wich is now in JRS.

.. code-block:: python

    >>> reportunit = Resource(client, '/openerp/bases/openerp_demo')
    
    >>> rtype = 'reportUnit'
    >>> resource_name = 'myreport'
    >>> datasource = '/datasources/openerp_demo'
    >>> jrxmlsource = '/openerp/bases/reports/myresource'
    
    >>> reportunit.create(resource_name, rtype,  uri_datasource=datasource, uri_jrxmlfile=jrxmlsource)
    
Maybe, you could need run it :

.. code-block:: python

    >>> from jasperserver.services import Report
    >>> report = Report(client, '/openerp/bases/openerp_demo')
    >>> report.run('myreport')
    
It will return a binary data stream of a pdf file by default. Just write it in a file.
But, you can export the report in XLS :

.. code-block:: python

    >>> report.run('myreport', output_format='xls')
    
JRS can export report in different output format.
Please read the web service documentation of JRS to know all supported format.


    

   
    
