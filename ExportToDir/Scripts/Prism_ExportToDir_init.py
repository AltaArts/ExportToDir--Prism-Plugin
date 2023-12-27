# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2021 Richard Frangenberg
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


from Prism_ExportToDir_Variables import Prism_ExportToDir_Variables
from Prism_ExportToDir_Functions import Prism_ExportToDir_Functions


class Prism_ExportToDir(Prism_ExportToDir_Variables, Prism_ExportToDir_Functions):
    def __init__(self, core):
        Prism_ExportToDir_Variables.__init__(self, core, self)
        Prism_ExportToDir_Functions.__init__(self, core, self)