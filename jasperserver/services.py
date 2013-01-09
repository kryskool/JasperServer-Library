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
from resourcedescriptor import *


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
        params = {'q': description,
             'type': wstype,
             'recursive': recursive,
             'limit': item_max
        }
        res_xml = self._connect.get(self.url, 'application/x-www-form-urlencoded', params)
        print 'search resources', description, '=\n', res_xml


class Resource (object):

    def __init__(self, js_connect, path='/', isModified=True):
        self.isModified = isModified
        self._connect = js_connect
        self.path = path
        self.url = js_connect._rest_url + '/resource/' + path
        self.rd = ''
        self.resource_name = ''
        self.uri = ''

    def create(self, rd, path_fileresource=None):
        if path_fileresource:
            self._connect.put_post_multipart(self.url, rd, path_fileresource, method='PUT', uri=self.uri)

        else:
            self._connect.put(self.url, data=rd)

    def modify(self, rd, path_fileresource=None):
        if path_fileresource:
            self._connect.put_post_multipart(self.url, rd, path_fileresource, method='POST', uri=self.uri)

        else:
            self._connect.post(self.url, body=rd)

    def get(self, resource_name, uri_datasource=None, param_p=None, param_pl=None):
        params = {'file': resource_name}
        if uri_datasource:
            params['IC_GET_QUERY_DATA'] = uri_datasource

            if param_p:
                params['param_p'] = param_p

            if param_pl:
                params['param_pl'] = param_pl

        self._connect.get(self.url, 'application/x-www-form-urlencoded', params)

    def delete(self, resource_name):
        urltodelete = self.url + '/' + resource_name
        print 'url a supprimer', urltodelete
        self._connect.delete(urltodelete)

    def build_basicRD(self, resource_name, wsType, hasData, isSingle):
        '''resource_name : the name of the resource
           wsType : type of the resource (see jasper web service documentation)
           hasData : boolean. True means the resource is a file resource
           isSingle : boolean. False means the builder is called by another builder.
        '''
        self.resource_name = resource_name
        if self.isModified:
            self.uri = self.path

        elif self.path == '/':
            self.uri = self.path + self.resource_name

        else:
            self.uri = self.path + '/' + self.resource_name

        self.rd = ResourceDescriptor(name=self.resource_name, wsType=wsType, uriString=self.uri)
        self.rd.append(Label(self.resource_name))
        self.rd.append(ResourceProperty('PROP_PARENT_FOLDER', self.path))
        if hasData:
            self.rd.append(ResourceProperty('PROP_HAS_DATA', 'true'))

        if isSingle:
            simpleRD = etree.tostring(self.rd, pretty_print=True)
            return simpleRD

    def build_jdbcRD(self, resource_name, ds_username, ds_password, ds_url, driverClass='org.postgresql.Driver'):
        self.build_basicRD(resource_name=resource_name, wsType='jdbc', hasData=False, isSingle=False)
        self.rd.append(ResourceProperty('PROP_DATASOURCE_DRIVER_CLASS', driverClass))
        self.rd.append(ResourceProperty('PROP_DATASOURCE_USERNAME', ds_username))
        self.rd.append(ResourceProperty('PROP_DATASOURCE_PASSWORD', ds_password))
        self.rd.append(ResourceProperty('PROP_DATASOURCE_CONNECTION_URL', ds_url))

        jdbcRD = etree.tostring(self.rd, pretty_print=True)
        return jdbcRD

    def build_reportUnitRD(self, resource_name, uri_datasource, uri_jrxmlfile):
        self.build_basicRD(resource_name=resource_name, hasData=False, wsType='reportUnit', isSingle=False)
        self.rd.append(ResourceProperty('PROP_RU_ALWAYS_PROPMT_CONTROLS', 'true'))
        self.rd.append(ResourceProperty('PROP_RU_CONTROLS_LAYOUT', '1'))
        rdds = ResourceDescriptor(wsType='datasource')
        rdds.append(ResourceProperty('PROP_REFERENCE_URI', uri_datasource))
        rdds.append(ResourceProperty('PROP_IS_REFERENCE', 'true'))
        self.rd.append(rdds)

        rdjrxml = ResourceDescriptor(name=resource_name, wsType='jrxml', uriString=uri_jrxmlfile)
        rdjrxml.append(ResourceProperty('PROP_IS_REFERENCE', 'true'))
        rdjrxml.append(ResourceProperty('PROP_REFERENCE_URI', uri_jrxmlfile))
        rdjrxml.append(ResourceProperty('PROP_RU_IS_MAIN_REPORT', 'true'))
        self.rd.append(rdjrxml)

        reportUnitRD = etree.tostring(self.rd, pretty_print=True)
        return reportUnitRD


class Report(object):

    def __init__(self, js_connect, path):
        self._connect = js_connect
        self.url = js_connect._rest_url + '_v2/reports' + path + '/'

    def run(self, name, output_format, page='', onepagepersheet=''):
        params = None
        if page:
            params = {'page': page}
        if onepagepersheet:
            params['onePagePerSheet'] = onepagepersheet
        print self.url + name + '.' + output_format
        content = self._connect.get(self.url + name + '.' + output_format, params=params)
        with open('/tmp/%s.%s' % (name, output_format), 'w') as output_file:
            output_file.write(content)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
