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


class JsException(Exception):
    """
    Global error for JasperQuery
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

###
## Error start with 4XX
##


class BadRequest(JsException):
    """
    Error 400
    """
    def __init__(self, value='Bad Request'):
        self.value = value


class Unauthorized(JsException):
    """
    Error 401
    """
    def __init__(self, value='Bad Request'):
        self.value = value


class Forbidden(JsException):
    """
    Error 403
    """
    def __init__(self, value='Forbidden'):
        self.value = value


class NotFound(JsException):
    """
    Raise this when error 404
    """
    def __init__(self, value='Not Found'):
        self.value = value

# We can use StatusException as:
# status = '404'
# if status in StatusException:
#    raise StatusException[status]()
StatusException = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
