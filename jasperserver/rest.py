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
import urllib2
import httplib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from exceptions import JsException, StatusException


class Client(object):
    """
    Create a REST connection, with authentification
    """
    http = None
    headers = {
       'User-Agent': 'JasperServer-Python',
       #'User-Agent': 'Apache-HttpClient/4.1.1'
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
        params = urllib.urlencode({
                'j_username': username,
                'j_password': password,
        })

        response, content = self.http.request(self._rest_url + '/login', 'POST', params, headers=headers)
        if response.get('status', '500') != '200':
            raise JsException('Login Error')

        self.headers['Cookie'] = response.get('set-cookie', False)

    def get(self, url, content_type='text/plain', params=''):
        """
        Send a http GET query
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        if params:
            url = url + '?%s' % params
        response, content = self.http.request(url, method="GET", body=params, headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return content

    def put(self, url, content_type='text/plain', body=''):
        """
        send a single content
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        print headers
        print url
        print body
        response, content = self.http.request(url, method='PUT', body=body, headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return (response.get('status'), content)

    def post(self, url, content_type='text/plain', body=''):
        """
        send a single content
        """
        headers = {'content-type': content_type}
        headers.update(self.headers)
        response, content = self.http.request(self._clean_url(url), method='POST', body=body, headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return (response.get('status'), content)

    def delete(self, url):
        headers = {}
        headers.update(self.headers)
        response, content = self.http.request(self._clean_url(url), method='DELETE', headers=headers)
        if response.get('status', '500') in StatusException:
            raise StatusException[response['status']]()

        return (response.get('status'), content)

    def put_post_multipart(self, url, path_xmltemplate, path_jrxmlresource, method):
        register_openers()
        print 'path_xmltemplate =', path_xmltemplate
        xmltemplate = open(path_xmltemplate, 'r').read()
        print 'xmltemplate : ', xmltemplate
        values = {
            'ResourceDescriptor': xmltemplate
        }
        if path_jrxmlresource:
            jrxml = open(path_jrxmlresource, 'r')
            values['jrxmlfile'] = jrxml
        data, headers = multipart_encode(values)
        data = ''.join(data)
        headers['Content-Length'] = str(len(xmltemplate))
        headers.update(self.headers)
        print 'put in this url =', url
        print 'headers ='
        for k, v in headers.items():
            print '    ', k, ':', v
        print 'data =\n', data
        response, content = self.http.request(url, method=method, body=data, headers=headers)
        print 'Reponse ='
        for k, v in response.items():
            print '    ', k, ':', v
        print 'Content =\n', content

    @staticmethod
    def _clean_url(url):
        return urllib.quote(url.replace('//', '/').replace('http:/', 'http://'), safe=':/')

    def __str__(self, ):
        return '%s Cookie: %s' % (self._url, self.headers.get('Cookie', ''))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
