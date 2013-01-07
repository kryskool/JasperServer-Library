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
from resourcedescriptor import *
from fileresourcestat import *

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
        params = urllib.urlencode(
            {'file': resource_name,
             'IC_GET_QUERY_DATA': uri_datasource,
        })
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
        self.rd.append(Mtime('12316545646'))
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


class ResourceReportUnit(object):

    def __init__(self, js_session, path_local_jrxmlresource, path_js_jrxmlresource, path_js_ruresource):
        self.js_session = js_session
        self.path_local_jrxmlresource = path_local_jrxmlresource
        self.path_js_jrxmlresource = path_js_jrxmlresource
        self.path_js_ruresource = path_js_ruresource
        self.filesresources = FilesResource(path_local_jrxmlresource, 'jrxml')

    def create_all(self):
        for filename, filename_ext in self.filesresources.get_statfilename().keys():
            self.create(filename, filename_ext)

    def create(self, filename, filename_ext):
        uri_jrxmlfile = self.path_js_jrxmlresource + '/' + filename
        resource_jrxml = Resource(self.js_session, self.path_js_jrxmlresource, isModified=False)
        resource_reportUnit = Resource(self.js_session, self.path_js_ruresource, isModified=False)

        rdjrxml = resource_jrxml.build_basicRD(filename, 'jrxml', hasData=True, isSingle=True)
        rdru = resource_reportUnit.build_reportUnitRD(filename, '/datasources/openerp_demo', uri_jrxmlfile)
        resource_jrxml.create(rdjrxml, self.path_local_jrxmlresource + filename_ext)
        resource_reportUnit.create(rdru)

    def modify(self, filename):
        uri_jrxmlfile = self.path_js_jrxmlresource + '/' + filename
        resource_jrxml = Resource(self.js_session, self.path_js_jrxmlresource + '/' + filename, isModified=True)
        resource_reportUnit = Resource(self.js_session, self.path_js_ruresource + '/' + filename, isModified=True)
        rdjrxml = resource_jrxml.build_basicRD(filename, 'jrxml', hasData=True, isSingle=True)
        rdru = resource_reportUnit.build_reportUnitRD(filename, '/datasources/openerp_demo', uri_jrxmlfile)

        resource_jrxml.modify(rdjrxml, self.path_local_jrxmlresource + filename_ext)
        resource_reportUnit.modify(rdru)

    def delete(self, filename):
        print 'jesuisdansdeletesync'
        Resource(self.js_session, self.path_js_ruresource).delete(filename)
        Resource(self.js_session, self.path_js_jrxmlresource).delete(filename)

    def update_all(self):
        try:
            new_files = self.filesresources.get_statfilename()
            old_files = self.filesresources.load_filestat('stat_filedata')
            diff_files = filter(lambda a: old_files[a[0]] != a[1], new_files.items())
            print diff_files
            for k, k_ext in new_files.keys():
                if not (k, k_ext) in old_files.keys():
                    self.create(k, k_ext)

            for (k, k_ext), mtime in diff_files:
                print 'fichier ', k_ext, ' modifié'
                self.modify(k, k_ext)

            for k, k_ext in old_files.keys():
                if not (k, k_ext) in new_files.keys():
                    self.delete(k)

        except:
            self.create_all()

        self.filesresources.serialize_filestat('stat_filedata')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
