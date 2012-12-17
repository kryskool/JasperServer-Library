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


class Resource (object):

    def __init__(self, js_connect, path=''):
        self._connect = js_connect
        self.path = path
        self.url = js_connect._rest_url + '/resource/' + path
        self.rd = ''
        self.resource_name = ''
        self.uri = ''

    def create(self, path_xmltemplate, path_fileresource=None):
        self._connect.put_post_multipart(self.url, path_xmltemplate, path_fileresource, method='PUT', uri=self.uri)

    def modify(self, path_xmltemplate, path_jrxmlresource=None):
        self._connect.put_post_multipart(self.url, path_xmltemplate, path_jrxmlresource, method='POST', uri=self.uri)

    def get(self, resource_name, uri_datasource=None, param_p=None, param_pl=None):
        params = urllib.urlencode(
            {'file': resource_name,
             'IC_GET_QUERY_DATA': uri_datasource,
        })
        self._connect.get(self.url, 'application/x-www-form-urlencoded', params)

    def delete(self, resource_name):
        urltodelete = self.url + resource_name
        print urltodelete
        self._connect.delete(urltodelete)

    def build_basicRD(self, resource_name, wsType, isData, isSingle):
        '''resource_name : the name of the resource
           wsType : type of the resource (see jasper web service documentation)
        '''
        self.resource_name = resource_name
        self.uri = self.path + self.resource_name
        self.rd = etree.Element('resourceDescriptor', name=resource_name, uriString=self.uri, wsType=wsType)
        etree.SubElement(self.rd, 'label').text = resource_name
        prop_parentElt = etree.SubElement(self.rd, 'resourceProperty', name='PROP_PARENT_FOLDER')
        etree.SubElement(prop_parentElt, 'value').text = self.path
        if isData:
            prop_dataElt = etree.SubElement(self.rd, 'resourceProperty', name='PROP_HAS_DATA')
            etree.SubElement(prop_dataElt, 'value').text = 'true'

        if isSingle:
            simpleRD = etree.tostring(self.rd, pretty_print=True)
            print simpleRD
            return simpleRD

    def build_jdbcRD(self, resource_name, ds_username, ds_password, ds_url, driverClass='org.postgresql.Driver'):
        self.build_basicRD(resource_name=resource_name, wsType='jdbc', isData=False, isSingle=False)
        prop_driverClass = etree.SubElement(self.rd, 'resourceProperty', name='PROP_DATASOURCE_DRIVER_CLASS')
        etree.SubElement(prop_driverClass, 'value').text = driverClass
        prop_dsusername = etree.SubElement(self.rd, 'resourceProperty', name='PROP_DATASOURCE_USERNAME')
        etree.SubElement(prop_dsusername, 'value').text = ds_username
        prop_dspasswd = etree.SubElement(self.rd, 'resourceProperty', name='PROP_DATASOURCE_PASSWORD')
        etree.SubElement(prop_dspasswd, 'value').text = ds_password
        prop_dsurl = etree.SubElement(self.rd, 'resourceProperty', name='PROP_DATASOURCE_CONNECTION_URL')
        etree.SubElement(prop_dsurl, 'value').text = ds_url

        jdbcRD = etree.tostring(self.rd, pretty_print=True)
        print jdbcRD
        return jdbcRD

    def build_reportUnitRD(self, resource_name, uri_datasource, uri_jrxml, path_other1=None, path_other2=None):
        self.build_basicRD(resource_name=resource_name, isData=False, wsType='reportUnit', isSingle=False)
        rdds = etree.SubElement(self.rd, 'resourceDescriptor', wsType='datasource')
        prop_refuri = etree.SubElement(rdds, 'resourceProperty', name='PROP_REFERENCE_URI')
        etree.SubElement(prop_refuri, 'value').text = uri_datasource
        prop_isref = etree.SubElement(rdds, 'resourceProperty', name='PROP_IS_REFERENCE')
        etree.SubElement(prop_isref, 'value').text = 'true'
        etree1 = etree.tostring(rdds, pretty_print=True)

        rdjrxml = etree.SubElement(self.rd, 'resourceDescriptor', wsType='jrxml', uriString=uri_jrxml)
        prop_isref = etree.SubElement(rdjrxml, 'resourceProperty', name='PROP_IS_REFERENCE')
        etree.SubElement(prop_isref, 'value').text = 'true'

        etree2 = etree.tostring(rdjrxml, pretty_print=True)

        reportUnitRD = etree1 + etree1

        print reportUnitRD
        return reportUnitRD

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
