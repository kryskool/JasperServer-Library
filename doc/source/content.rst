.. automodule:: jasperserver.rest
.. automodule:: jasperserver.admin
.. automodule:: jasperserver.services

====================
Developer Interface
====================

This part of the documentation covers all class and methods of the module

REST Authentification
=====================

When using web services, the calling application must provide a valid user ID and password to JasperReports Server. The special login service that allows authentication using a POST request to create a session and return a session ID that is used with subsequent requests.

.. automodule:: jasperserver.rest
    :members:
   
Administration service
======================

The web services for administration consists to administers users and roles for searching, editing, deleting and creating. Only administrative users may access these REST services.

.. automodule:: jasperserver.admin
    :members:

Resources service
=================

This service lets you browse or search the repository in JasperServer. The resources service is a read only service.
    
.. autoclass:: jasperserver.services.Resources
    :members:
    
Resource service
================
    
The resource service supports several HTTP methods to view, create, and modify resources in the repository.

.. autoclass:: jasperserver.services.Resource
    :members:
    
Report service
==============

This service simplifies the API for obtaining report output such as PDF or XLS.

.. autoclass:: jasperserver.services.Report
    :members:
         
Synchronization
===============

Synchronization allow update (create, modify, delete) all local JRXML files into JRXML Resource and report unit Resource to JasperServer.
 
.. automodule:: jasperserver.synchronization
    :members:

