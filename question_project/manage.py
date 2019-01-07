from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import app
from ext import db
from model import User,Answer,Question


manager = Manager(app)      # 包装为命令行启动模式
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
