#!/usr/bin/env python
from __future__ import absolute_import

import argparse
import os
import os.path

from flask import Flask
from flask.ext import script
from flask.ext.migrate import Migrate, MigrateCommand

from ybtheta import create_app


migrate = Migrate(None, None)


# This is a crufty workaround for Flask-Migrate and it's inability to use app
# factories. This is a subclass of the Manager that will be used as the root
# manager that overrides the __call__ method. The MigrateManager.__call__
# method initializes the app if needed, and then at the same time initializes
# the migration object (an instance of Migrate).
class MigrateManager(script.Manager):

    def __call__(self, app=None, **kwargs):
        if app is None:
            migrate_app = self.app
        else:
            migrate_app = app
        is_factory = not isinstance(migrate_app, Flask)
        new_app = super(MigrateManager, self).__call__(app=app, **kwargs)
        if is_factory:
            db = new_app.extensions['sqlalchemy'].db
            migrate.init_app(new_app, db)
        return new_app


manager = MigrateManager(create_app)
manager.add_command('db', MigrateCommand)


class AbsolutePathAction(argparse.Action):
    """Custom argparse.Action that transforms path strings into absolute paths.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        current_absolute = os.path.abspath(os.getcwd())
        if isinstance(values, str):
            new_values = os.path.join(current_absolute, values)
        else:
            new_values = []
            for value in values:
                real_path = os.path.join(current_absolute, values)
                new_values.append(real_path)
        setattr(namespace, self.dest, new_values)


# Monkeypatch Flask-Script to consider my custom path action 'safe'
safe_actions = list(script.safe_actions)
safe_actions.append(AbsolutePathAction)
script.safe_actions = safe_actions
# Add option for pointing to a configuration file
manager.add_option('-c', '--config', dest='config', required=False,
        action=AbsolutePathAction)


if __name__ == '__main__':
    manager.run()
