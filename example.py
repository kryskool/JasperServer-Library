# -*- coding: utf-8 -*-
import sys
from jasperserver.rest import Client
from jasperserver.admin import User
from jasperserver.services import Resources
from jasperserver.exceptions import *

try:
    client = Client('http://localhost:8080/jasperserver', 'jasperadmin', 'jasperadmin')
except JsException:
    print 'Error Authentification FAIL!'
    sys.exit(1)


user = User(client)
rs = Resources(client)

try:
    # creating ad setting a new user
    user.create('myusername', 'mylogin', 'mypwd', roles=['ROLE_ADMINISTRATOR'])
    print user.search('myusername')

    # searching a resource in JRS
    print rs.search('resourcename')

except Forbidden:
    print 'Error, Existent Resource'

except Unauthorized:
    print 'Non Valide Request'

except NotFound:
    print 'Resource Not found'



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
