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
from services import *
import glob
import os.path


class SyncResources(object):
    '''
    a SyncResources class instance allow update local Resource to Resource JasperServer. You need an authentified client *js_connect*.
    '''

    def __init__(self, js_session):
        self.js_session = js_session

    def src_res(self, path, ext='*.jrxml'):
        # Return a list of files resource name in source path
        list_src = []
        os.chdir(path)
        for filename_ext in glob.glob(ext):
            filename, _ext = os.path.splitext(filename_ext)
            list_src.append(filename)

        return list_src

    def filter_resource_name(self, resources_list):
        l = []
        for r in resources_list:
            for k, v in r.items():
                if k == 'name':
                    l.append(v)

        return l

    def update_mainreports(self, path_src_mainjrxml, path_js_mainjrxml='/openerp/reports', path_js_ruresource='/openerp/bases/openerp_demo'):
        '''
        Update main reports (jrxml and report units)
        This method allows update local Resource with *path_src_jrxmlresource* to Resource JasperServer in the following repository :
        *path_js_jrxmlresource* and *path_js_ru_resource*.
        '''
        listjs = []
        mainjrxml = Resource(self.js_session, path_js_mainjrxml)
        ru = Resource(self.js_session, path_js_ruresource)
        listjs = self.filter_resource_name(Resources(self.js_session, path_js_ruresource).search())
        listjsjrxml = self.filter_resource_name(Resources(self.js_session, path_js_mainjrxml).search())
        listsrc = self.src_res(path_src_mainjrxml)

        # look for resource in js but not in path oerp
        for resource in set(listjs).difference(listsrc):
            ru.delete(resource)
            mainjrxml.delete(resource)

        # look for modification
        for resource in set(listjs).intersection(listsrc):
            mainjrxml.modify(resource_name=resource, wsType='jrxml', path_fileresource=path_src_mainjrxml + resource + '.jrxml')
            ru.modify(resource_name=resource, wsType='reportUnit', uri_jrxmlfile=path_js_mainjrxml)

        # look for resource to add in js
        for resource in set(listsrc).difference(listjs):
            if resource in set(listsrc).difference(listjsjrxml):
                mainjrxml.create(resource_name=resource, wsType='jrxml', path_fileresource=path_src_mainjrxml + resource + '.jrxml')

            ru.create(resource_name=resource, wsType='reportUnit', uri_jrxmlfile=path_js_mainjrxml)

    def update_subreports(self, path_src_subjrxml, path_js_subjrxml='/openerp/subreports'):
        '''
        Update subreports (jrxml only)
        This method allows update local Resource with *path_src_subjrxml* to Resource JasperServer in *path_js_subjrxml*
        '''
        subjrxml = Resource(self.js_session, path_js_subjrxml)
        listjssubjrxml = self.filter_resource_name(Resources(self.js_session, path_js_subjrxml).search())
        listsrcsub = self.src_res(path_src_subjrxml)

        # look for resource in js but not in path oerp
        for resource in set(listjssubjrxml).difference(listsrcsub):
            subjrxml.delete(resource)

        # look for modification
        for resource in set(listjssubjrxml).intersection(listsrcsub):
            subjrxml.modify(resource_name=resource, wsType='jrxml', path_fileresource=path_src_subjrxml + resource + '.jrxml')

        # look for resource to add in js
        for resource in set(listsrcsub).difference(listjssubjrxml):
            subjrxml.create(resource_name=resource, wsType='jrxml', path_fileresource=path_src_subjrxml + resource + '.jrxml')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
