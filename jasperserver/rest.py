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
import requests
from poster.encode import multipart_encode
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
        #pass

    def _login(self, username, password):
        """
        Send POST authentification and retrieve the cookie
        """
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        headers.update(self.headers)
        params = {
                'j_username': username,
                'j_password': password,
        }

        response = requests.post(self._rest_url + '/login', params=params, headers=headers)
        if response.raise_for_status():
            raise JsException('Login Error')

        self.headers['Cookie'] = response.headers['set-cookie']

    def get(self, url, content_type='text/plain', params=''):
        """
        Send a http GET query
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        response = requests.get(url, params=params, headers=headers)
        if response.raise_for_status():
            raise StatusException[response['status']]()

        return response.text

    def put(self, url, content_type='text/plain', data=''):
        """
        send a single content
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        response = requests.put(url, data=data, headers=headers)
        if response.raise_for_status():
            raise StatusException[response['status']]()

        print response.text
        return response.headers['status'], response.text

    def post(self, url, content_type='text/plain', data=''):
        """
        send a single content
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        response = requests.post(self._clean_url(url), data=data, headers=headers)
        if response.raise_for_status():
            raise StatusException[response['status']]()

        return response.headers['status'], response.text

    def delete(self, url):
        headers = {}
        headers.update(self.headers)
        response = requests.delete(self._clean_url(url), headers=headers)
        if response.raise_for_status():
            raise StatusException[response['status']]()

        # return response.header['status'], response.text

    def put_post_multipart(self, url, rd, path_fileresource, method, uri):
        f = open(path_fileresource, 'r')
        values = [
            ('ResourceDescriptor', rd),
            (uri, f)
        ]
        data, headers = multipart_encode(values)
        data = ''.join(data)

        headers.update(self.headers)
        print 'put in this url =', url
        print 'headers ='
        for k, v in headers.items():
            print '    ', k, ':', v
        response, content = self.http.request(url, method=method, headers=headers, body=data)
        print 'Reponse ='
        for k, v in response.items():
            print '    ', k, ':', v

        print content

    @staticmethod
    def _clean_url(url):
        return urllib.quote(url.replace('//', '/').replace('http:/', 'http://'), safe=':/')

    def __str__(self, ):
        return '%s Cookie: %s' % (self._url, self.headers.get('Cookie', ''))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
