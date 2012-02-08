# -*- coding: utf-8 -*-
##############################################################################
#
#    jasperserver library module for OpenERP
#    Copyright (C) 2012 SYLEAM ([http://www.syleam.fr]) Christophe CHAUVET
#
#    This file is a part of jasperserver library
#
#    jasperserver library is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    jasperserver library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see [http://www.gnu.org/licenses/].
#
##############################################################################

import urllib
import httplib2
from exceptions import JsException, StatusException

class Client(object):
    """
    Create a REST connection, with authentification
    """
    http = None
    headers = {
        'User-Agent': 'JasperServer-Python',
    }

    def __init__(self, url, username='jasperadmin', password='jasperadmin'):
        self._url = url
        self._rest_url = url + '/rest'
        self.http = httplib2.Http()
        self._login(username, password)
        pass

    def _login(self, username, password):
        """
        Send POST authentification and retrieve the cookie
        """
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        headers.update(self.headers)
        params = urllib.urlencode({
                'j_username': username,
                'j_password': password,
        })

        response, content = self.http.request(self._rest_url + '/login', 'POST', params, headers=headers)
        if response.get('status', '500') != '200':
            raise JsException('Login Error')

        self.headers['Cookie'] = response.get('set-cookie',False)

    def get(self, url, args=None):
        """
        Send a http GET query
        """
        headers = {}
        headers.update(self.headers)
        response, content = self.http.request(url, headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return content

    def put(self, url, content_type='text/plain', body=''):
        """
        Send a single content
        """
        headers = {'Content-type': content_type}
        headers.update(self.headers)
        response, content = self.http.request(url, method='PUT', body=body, headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return (response.get('status'), content)

    def __str__(self,):
        return '%s Cookie: %s' % (self._url, self.headers.get('Cookie',''))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
