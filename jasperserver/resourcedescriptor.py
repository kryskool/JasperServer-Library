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
from lxml import etree


class ResourceDescriptor(etree.ElementBase):
    TAG = 'resourceDescriptor'

    def __init__(self, wsType, name='', uriString=''):
        super(ResourceDescriptor, self).__init__(name=name, wsType=wsType, uriString=uriString)


class Label(etree.ElementBase):
    TAG = 'label'

    def __init__(self, value):
        super(Label, self).__init__(value)


class ResourceProperty(etree.ElementBase):
    TAG = 'resourceProperty'

    def __init__(self, name, value):
        super(ResourceProperty, self).__init__(name=name)
        self.append(Value(value))


class Value(etree.ElementBase):
    TAG = 'value'

    def __init__(self, value):
        super(Value, self).__init__(value)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
