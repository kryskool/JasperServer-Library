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

from StringIO import StringIO
import urllib

try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree


class Resources (object):

    def __init__(self, js_connect, path=''):
        self._connect = js_connect
        self.path = path
        self.url = js_connect._rest_url + '/resources' + path

    def search(self, description='', wstype='', recursive='0', item_max='0'):
        params = urllib.urlencode(
            {'q': description,
             'type': wstype,
             'recursive': recursive,
             'limit': item_max
        })
        res_xml = self._connect.get(self.url, 'application/x-www-form-urlencoded', params)
        print 'search resources', description, '=\n', res_xml


class Resource (Resources):

    def __init__(self, js_connect, path=''):
        self._connect = js_connect
        self.path = path
        self.url = js_connect._rest_url + '/resource' + path + '/'

    def create(self, path_xmltemplate, path_jrxmlresource=None):
        self._connect.put_post_multipart(self.url, path_xmltemplate, path_jrxmlresource, method='PUT')

    def modify(self, path_xmltemplate, path_jrxmlresource=None):
        self._connect.put_post_multipart(self.url, path_xmltemplate, path_jrxmlresource, method='POST')

    def get(file, query, param_p, param_pl):
        pass

    def delete(self, resource_name):
        urltodelete = self.url + resource_name
        print urltodelete
        self._connect.delete(urltodelete)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
