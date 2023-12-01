# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Rattail - subcommand ``make-appdir``
"""

from wuttjamaican.commands import make_appdir as base

from rattail.commands import RattailSubcommand


class MakeAppDir(base.MakeAppDir, RattailSubcommand):
    """
    Make or refresh the "app dir" for virtual environment
    """
    name = 'make-appdir'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('-U', '--user', metavar='USERNAME',
                            help="Linux username which should be given ownership to the various "
                            "data folders which are to be created.  This is used when the app(s) "
                            "are to normally be ran as the 'rattail' user for instance.  Use "
                            "of this option probably requires 'sudo' or equivalent.")

    def make_appdir(self, appdir, args):
        """ """
        super().make_appdir(appdir, args)

        # TODO: this bit should probably be part of app method
        if args.user:
            import pwd
            pwdata = pwd.getpwnam(args.user)
            folders = [
                'data',
                os.path.join('data', 'uploads'),
                'log',
                'sessions',
                'work',
            ]
            for name in folders:
                path = os.path.join(app_path, name)
                os.chown(path, pwdata.pw_uid, pwdata.pw_gid)
