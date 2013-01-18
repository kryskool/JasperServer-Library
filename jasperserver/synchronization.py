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

    def __init__(self, js_session):
        self.js_session = js_session

    def oerp_res(self, path, ext='*.jrxml'):
        list_oerp = []
        os.chdir(path)
        for filename_ext in glob.glob(ext):
            filename, _ext = os.path.splitext(filename_ext)
            list_oerp.append(filename)

        return list_oerp

    def update_mainreports(self, path_oerp_mainjrxml, path_js_mainjrxml='/openerp/reports', path_js_ruresource='/openerp/bases/openerp_demo'):
        '''
        Update main reports (jrxml and report units)
        '''
        mainjrxml = Resource(self.js_session, path_js_mainjrxml)
        ru = Resource(self.js_session, path_js_ruresource)
        listjs = Resources(self.js_session, path_js_ruresource).search()
        listjsjrxml = Resources(self.js_session, path_js_mainjrxml).search()
        listoerp = self.oerp_res(path_oerp_mainjrxml)

        # look for resource in js but not in path oerp
        for resource in set(listjs).difference(listoerp):
            print resource
            ru.delete(resource)
            mainjrxml.delete(resource)

        # look for modification
        for resource in set(listjs).intersection(listoerp):
            mainjrxml.modify(resource_name=resource, wsType='jrxml', path_fileresource=path_oerp_mainjrxml + resource + '.jrxml')
            ru.modify(resource_name=resource, wsType='reportUnit', uri_jrxmlfile=path_js_mainjrxml)

        # look for resource to add in js
        for resource in set(listoerp).difference(listjs):
            if resource in set(listoerp).difference(listjsjrxml):
                mainjrxml.create(resource_name=resource, wsType='jrxml', path_fileresource=path_oerp_mainjrxml + resource + '.jrxml')

            ru.create(resource_name=resource, wsType='reportUnit', uri_jrxmlfile=path_js_mainjrxml)

    def update_subreports(self, path_oerp_subjrxml, path_js_subjrxml='/openerp/subreports'):
        '''
        Update subreports (jrxml only)
        '''
        subjrxml = Resource(self.js_session, path_js_subjrxml)
        listjssubjrxml = Resources(self.js_session, path_js_subjrxml).search()
        listoerpsub = self.oerp_res(path_oerp_subjrxml)

        # look for resource in js but not in path oerp
        for resource in set(listjssubjrxml).difference(listoerpsub):
            subjrxml.delete(resource)

        # look for modification
        for resource in set(listjssubjrxml).intersection(listoerpsub):
            subjrxml.modify(resource_name=resource, wsType='jrxml', path_fileresource=path_oerp_subjrxml + resource + '.jrxml')

        # look for resource to add in js
        for resource in set(listoerpsub).difference(listjssubjrxml):
            subjrxml.create(resource_name=resource, wsType='jrxml', path_fileresource=path_oerp_subjrxml + resource + '.jrxml')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
