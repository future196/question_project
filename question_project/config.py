DIALECT = "mysql"
DRIVER = "pymysql"
HOSTNAME = "localhost"
PORT = "3306"
USERNAME = "root"
PASSWORD = "root"
DATABASE = "actual"

format = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = format

SQLALCHEMY_TRACK_MODIFICATIONS = True
