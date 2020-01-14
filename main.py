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


def _add_seed_data():
    db.session.add(User(username='user1', password='user1'))
    db.session.add(User(username='user2', password='user2'))
    db.session.add(User(username='user3', password='user3'))
    db.session.add(Todo(user_id=1, description='Vivamus tempus'))
    db.session.add(Todo(user_id=1, description='lorem ac odio'))
    db.session.add(Todo(user_id=1, description='Ut congue odio'))
    db.session.add(Todo(user_id=1, description='Sodales finibus'))
    db.session.add(Todo(user_id=1, description='Accumsan nunc vitae'))
    db.session.add(Todo(user_id=2, description='Lorem ipsum'))
    db.session.add(Todo(user_id=2, description='In lacinia est'))
    db.session.add(Todo(user_id=2, description='Odio varius gravida'))
    db.session.commit()


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        _add_seed_data()
        print("AlayaTodo: Database initialized.")
    else:
        app.run(use_reloader=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Todo': Todo}
