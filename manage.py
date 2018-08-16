from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand, Migrate

app = create_app()
manager = Manager(app)
shell = Shell(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
