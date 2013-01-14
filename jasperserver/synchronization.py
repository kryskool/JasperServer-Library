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
from fileresourcestat import *


class SyncRU(object):

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
