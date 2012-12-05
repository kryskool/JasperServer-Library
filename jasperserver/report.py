##############################################################################
#
#    ModuleName module for OpenERP, Description
#    Copyright (C) 200X Company (<http://website>) author
#
#    This file is a part of ModuleName
#
#    ModuleName is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ModuleName is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import urllib


class Report(object):
    def __init__(self, js_connect, path):
        self._connect = js_connect
        self.url = js_connect._rest_url + '/report' + path + '/'


    def run(self, reportname, output_format='PDF', num_page='',images='images', x_method_override='PUT', ignorepagination='', onepagepersheet=''):
        params = {'RUN_OUTPUT_FORMAT': output_format,
             'IMAGES_URI': images,
        }
        if num_page:
            params['PAGE'] = num_page

        if x_method_override:
            params['X-Method-Override'] = x_method_override

        if ignorepagination:
            params['ignorePagination'] = ignorepagination

        if onepagepersheet:
            params['onePagePerSheet'] = onepagepersheet

        for k,v in params.items():
            print '     ', k, ':', v

        params= urllib.urlencode(params)
        print params
        reportpath = self.url + reportname
        response, content = self._connect.put(reportpath, 'application/x-www-form-urlencoded', params)
        print 'reponse:', response
        print 'content:', content

    def download(self, uuid):
        pass

    def regenerating(self, output_format, images, page):
        pass


class Reportv2(Report):
    def __init__(self, js_connect, path):
        self._connect = js_connect
        self.url = js_connect._rest_url + '_v2/reports' + path + '/'

    def run(self, name, output_format, page='', onepagepersheet=''):
        if page:
        params = {'page' : page}
        if onepagepersheet:
            params['onePagePerSheet'] = onepagepersheet
        print self.url + name + '.' + output_format
        content = self._connect.get(self.url + name + '.' + output_format, params)
        with open('/tmp/%s.%s' % (name, output_format), 'w') as output_file:
            output_file.write(content)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
