REST Authentification and Web Services
======================================

    When using web services, the calling application must provide a valid user ID and password to JasperReports Server. The special login service that allows authentication using a POST request to create a session and return a session ID that is used with subsequent requests.
    
.. class:: Client(url [, username [, password]])

    an :class:`Client` instance implements Login service in JasperServer using the session cookie and the RESTful interface.
    Default *username* and *password* are jasperadmin.
    
.. method:: Client._login(username, password)
    
    Send POST authentification and retrieve the cookie. this is called by the ``__init__`` method.
 
.. method:: Client.get(url [, content_type [, params]])

    Send a http GET query
    
.. method:: Client.put(url [, content_type [, data]])

    Send a single content

.. method:: Client.post(url [, content_type [, data]])

    Send a single content

.. method:: Client.delete(url)

    Remove resource in *url*

.. method:: Client.put_post_multipart(self, url, rd, path_fileresource, method, uri)

    Send a multipart/form-data to create a resource with a file resource.


Resources service
=================

    This service lets you browse or search the repository in JasperServer. The resources service is a read only service.

.. class:: Resources(js_connect [,path])

    an :class:`Resources` instance implements resources service in JasperServer. You need an open session *js_connect* to use this service. *path* is the URI to browse.
    

.. method:: Resources.search([description [, wstype [, recursive [, item_max]]]])
   
    When used without arguments, it gives the list of resources in the folder specified in the URL.
    With the arguments, you can search for terms in the resource names or descriptions, search for all resources of a given *wstype*, and specify whether to search in subfolders.
    This method return an XML resourceDescriptor in a string.  

Resource service
================
    
    The resource service supports several HTTP methods to view, create, and modify resources in the repository.
    
.. class:: Resource (js_connect [, path [, isModified]])

    an :class:`Resource` instance implements resource service in JasperServer. you need an open session *js_connect* to use this service. *path* is the folder where methods will be used.


.. method:: Resource.get(resource_name [, uri_datasource [, param_p [, param_pl]]])

    This method is used to show the information about a specific resource. Getting a resource can serve several purposes:
    In the case of JasperReports, also known as report units, this service returns the structure of the JasperReport, including resourceDescriptors for any linked resources.
    Specifying a JasperReport and a file identifier returns the file itself.
    Specifying a query-based input control with arguments for running the query returns the dynamic values for the control.

.. method:: Resource.create(rd [, path_fileresource])
    
    This method is used to create a new resource. *rd* must be an XML resource descriptor. You need *path_fileresource* if the resource has a file resource.
    
.. method:: Resource.modify(rd [, path_fileresource])

    This method is used to modify a resource. *rd* must be an XML resource descriptor. You need *path_fileresource* if the resource has a file resource.
    
.. method:: Resource.delete(resource_name)

    This method delete a resource.
    
.. method:: Resource.build_basicRD(resource_name, wsType, hasData, isSingle)

    This method is an XML resource descriptor builder. To build this XML you need name and wstype. If the resource has a file data you must set *hasData* to True. If the resource is not a complex resource (reportUnit type) set *isSingle* to True.
    
.. method:: Resource.build_reportUnitRD(resource_name, uri_datasource, uri_jrxmlfile)

    This method build an XML report unit resourceDescriptor. reports units need linked resource. You must have a datasource resource and jrxml resource.
    
 
Synchronization
===============

    Synchronization allow update (create, modify, delete) all local JRXML files into JRXML Resource and report unit Resource to JasperServer
 
.. class:: SyncRU(js_session, path_local_jrxmlresource, path_js_jrxmlresource, path_js_ruresource)

    an :class:`SyncRU` instance allow update local Resource with *path_local_jrxmlresource*, Resource JasperServer in the following repository : *path_js_jrxmlresource* and *path_js_ru_resource*

.. method:: SyncRU.update_all()

    This method update each Resource in JasperServer.
    

Synchronization Example
_______________________

.. code-block:: python

    import sys
    from jasperserver.rest import Client
    from jasperserver.admin import User
    from jasperserver.services  import *
    from jasperserver.synchronization import *
    
    
    path_js_jrxmlresource = '/my/jrxml/jasperserver/repository'
    path_js_reportUnit = '/my/reportUnit/jasperserver/repository'
    path_local_jrxmlresource = '/my/jrxml/repository/'
    
    client = Client('http://localhost:8080/jasperserver', 'jasperadmin', 'jasperadmin')
    
    ru = SyncRU(client, path_local_jrxmlresource, path_jrxmlresource, path_reportUnit)
    ru.update_all()


