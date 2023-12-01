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
Commands to manage settings
"""

import logging

from rattail import commands


log = logging.getLogger(__name__)


class ConfigSetting(commands.Subcommand):
    """
    Get a value from config file and/or settings table
    """
    name = 'config-setting'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('--section', help="Section name for the config setting.")
        parser.add_argument('--option', help="Option name for the config setting.")
        parser.add_argument('--name', help="Name of the config setting to get.  "
                            "This may be used instead of --section and --option.")

        parser.add_argument('--usedb', action='store_true',
                            help="Look for values in the DB (settings table).")
        parser.add_argument('--no-usedb', action='store_true',
                            help="Do not look for values in the DB (settings table).")

        parser.add_argument('--preferdb', action='store_true',
                            help="Prefer values from DB over those from config file.")
        parser.add_argument('--no-preferdb', action='store_true',
                            help="Prefer values from config file over those from DB.")

    def run(self, args):
        """
        Retrieves a config setting via simple call to
        :meth:`~rattail.config.RattailWuttaConfig.get()` and prints
        the value to :attr:`~rattail.commands.core.Command.stdout`.
        """
        # nb. we still may be using legacy config object, so must
        # convert name to (section, option) if applicable
        if args.section and args.option:
            section = args.section
            option = args.option
        elif args.name:
            section, option = legacy_split_setting(args.name)

        usedb = None
        if args.usedb:
            usedb = True
        elif args.no_usedb:
            usedb = False

        preferdb = None
        if args.preferdb:
            preferdb = True
        elif args.no_preferdb:
            preferdb = False

        value = self.config.get(section, option, usedb=usedb, preferdb=preferdb)
        if value is not None:
            self.stdout.write(f"{value}\n")


def legacy_split_setting(name):
    """
    Split a new-style setting ``name`` into a legacy 2-tuple of
    ``(section, option)``.
    """
    parts = name.split('.')
    if len(parts) > 2:
        log.debug("ambiguous legacy split for setting name: %s", name)
    return parts[0], '.'.join(parts[1:])


class SettingGet(commands.Subcommand):
    """
    Get a setting value from the DB
    """
    name = 'setting-get'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('name', help="Name of the setting to retrieve.")

    def run(self, args):
        session = self.make_session()
        value = self.app.get_setting(session, args.name)
        session.commit()
        session.close()
        self.stdout.write(value or '')


class SettingPut(commands.Subcommand):
    """
    Add or update a setting in the DB
    """
    name = 'setting-put'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('name', help="Name of the setting to save.")
        parser.add_argument('value', help="String value for the setting.")

    def run(self, args):
        session = self.make_session()
        self.app.save_setting(session, args.name, args.value)
        session.commit()
        session.close()
