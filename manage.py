#!/usr/bin/env python
from __future__ import absolute_import

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from ybtheta import create_app


migrate = Migrate(None, None)


# This is a crufty workaround for Flask-Migrate and it's inability to use app
# factories. This is a subclass of the Manager that will be used as the root
# manager that overrides the __call__ method. The MigrateManager.__call__
# method initializes the app if needed, and then at the same time initializes
# the migration object (an instance of Migrate).
class MigrateManager(Manager):

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
manager.add_option('-c', '--config', dest='config', required=False)


if __name__ == '__main__':
    migrate.init_app
    manager.run()
