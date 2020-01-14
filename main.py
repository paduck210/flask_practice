"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
import subprocess
import os
from alayatodo import app
from alayatodo import db
from alayatodo.models import Todo, User
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


MIGRATION_DIR = os.path.join('resources/migrations')
migrate = Migrate(app, db, directory=MIGRATION_DIR)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Todo': Todo}
