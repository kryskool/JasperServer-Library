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

try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree

class User(object):
    """
    Manage user inside the JasperServer
    """

    def __init__(self, js_connect):
        self._connect = js_connect
        self.url = js_connect._rest_url + '/user/'

    def search(self, query=''):
        """
        The GET method for the user service returns descriptors for all users
        that match the search string
        """
        res = []
        res_xml = self._connect.get(self.url + query)
        if res_xml:
            fp = StringIO(res_xml)
            tree = etree.parse(fp)
            for node in tree.findall('//user'):
                n = {}
                n['roles'] = []
                for i in node:
                    if i.tag in ('enabled', 'fullName', 'username'):
                        n[i.tag] = i.text
                    elif i.tag == 'roles':
                        for j in i.getchildren():
                            if j.tag == 'roleName':
                                n[i.tag].append(j.text)
                res.append(n)
        print res

    def create(self, name, login, password, roles=['ROLE_USER']):
        """
        Create a new user, if exists it return status 403
        """
        # ROLE_USER is necessary to display root folder (/) in jasperserver
        if 'ROLE_USER' not in roles:
            roles.append('ROLE_USER')
        root = etree.Element('user')
        etree.SubElement(root, 'enabled').text = 'true'
        etree.SubElement(root, 'fullName').text = name
        etree.SubElement(root, 'username').text = login
        etree.SubElement(root, 'password').text = password
        for r in roles:
            role = etree.SubElement(root, 'roles')
            etree.SubElement(role, 'roleName').text = r
        return self._connect.put(self.url, 'text/plain', etree.tostring(root))



class Role(object):
    """
    Manage role inside the JasperServer
    """

    def __init__(self, js_connect):
        pass

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
