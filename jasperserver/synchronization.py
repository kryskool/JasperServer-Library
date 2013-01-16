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
from fileresourcestat import Stat


class SyncResources(object):

    def __init__(self, js_session):
        self.js_session = js_session

    def update_mainreports(self, path_oerp_mainjrxml, path_js_mainjrxml='/openerp/reports', path_js_ruresource='/openerp/bases/openerp_demo'):
        '''
        Update main reports (jrxml and report units)
        '''
        statmainjrxml = Stat(path_oerp_mainjrxml, 'main_stats')
        cur_stats = statmainjrxml.get_stat()
        mainjrxml = Resource(self.js_session, path_js_mainjrxml)
        ru = Resource(self.js_session, path_js_ruresource)

        try:
            sav_stats = statmainjrxml.load_stat()
            diff_stats = filter(lambda a: sav_stats[a[0]] != a[1], cur_stats.items())
            print diff_stats
            for k, k_ext in cur_stats.keys():
                if not (k, k_ext) in sav_stats.keys():
                    mainjrxml.create(resource_name=k, wsType='jrxml', path_fileresource=path_oerp_mainjrxml + k_ext)
                    print 'jaiterminercreatejrxml'
                    ru.create(resource_name=k, wsType='reportUnit')

            for (k, k_ext), mtime in diff_stats:
                print 'fichier ', k_ext, ' modifié'
                mainjrxml.modify(resource_name=k, wsType='jrxml', path_fileresource=path_oerp_mainjrxml + k_ext)
                ru.modify(resource_name=k, wsType='reportUnit')

            for k, k_ext in sav_stats.keys():
                if not (k, k_ext) in cur_stats.keys():
                    ru.delete(k)
                    mainjrxml.delete(k)

        except:
            for k, k_ext in cur_stats.keys():
                mainjrxml.create(resource_name=k, wsType='jrxml', path_fileresource=path_oerp_mainjrxml + k_ext)
                ru.create(resource_name=k, wsType='reportUnit', uri_jrxmlfile=path_js_mainjrxml + '/' + k)

        statmainjrxml.serialize_stat()

    def update_subreports(self, path_oerp_subjrxml, path_js_subjrxml='/openerp/subreports'):
        statsubjrxml = Stat(path_oerp_subjrxml, 'sub_stats')
        try:
            sav_stats = statsubjrxml.load_stat()

        except:
            sav_stats = statsubjrxml.newflatfile()

        cur_stats = statsubjrxml.get_stat()
        diff_stats = filter(lambda a: sav_stats[a[0]] != a[1], cur_stats.items())
        print diff_stats
        subjrxml = Resource(self.js_session, path_js_subjrxml)
        for k, k_ext in cur_stats.keys():
            if not (k, k_ext) in sav_stats.keys():
                subjrxml.create(resource_name=k, wsType='jrxml', path_fileresource=path_oerp_mainjrxml)

            for (k, k_ext), mtime in diff_stats:
                print 'fichier ', k_ext, ' modifié'
                subjrxml.modify(resource_name=k, wsType='jrxml', path_fileresource=path_oerp_mainjrxml)

            for k, k_ext in sav_stats.keys():
                if not (k, k_ext) in cur_stats.keys():
                    subjrxml.delete(k)

        statsubjrxml.serialize_stat()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
