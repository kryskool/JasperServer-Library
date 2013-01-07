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

import os
import glob
import pickle


class FilesResource(object):

    def __init__(self, path_src, ext):
        os.chdir(path_src)
        self.ext = '*' + ext
        self.statfilename = {}

    def get_statfilename(self):
        for filename_ext in glob.glob(self.ext):
            filename, _ext = os.path.splitext(filename_ext)
            mtime = os.stat(filename_ext).st_mtime
            self.statfilename[filename, filename_ext] = mtime

        return self.statfilename

    def serialize_filestat(self, txt_file):
        with open(txt_file, 'w') as f:
            pickle.dump(self.statfilename, f)
            f.close()

    def load_filestat(self, txt_file):
        with open(txt_file, 'r') as f:
            stat = pickle.load(f)

        return stat

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
