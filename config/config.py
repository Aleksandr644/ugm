import os
from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))
__cfg = ConfigParser();
with open('config/db.ini') as fl:
    __cfg.read_file(fl);
__cfg_db = dict(__cfg.items('postgresql'));
driver = __cfg_db.get('driver', '');
host = __cfg_db.get('host', 'localhost');
database = __cfg_db.get('database', 'postgres');
password = __cfg_db.get('password', '');
user = __cfg_db.get('user', 'postgres');
port = __cfg_db.get('port', '');
__cfg_debug = dict(__cfg.items('debug'));
mail_server = __cfg_debug.get('server', 'localhost');
mail_port = __cfg_debug.get('port', 8025);
mail_use_tls = __cfg_debug.get('use_tls', 1);
mail_username = __cfg_debug.get('username', '');
mail_password = __cfg_debug.get('password', '');
admins = __cfg_debug.get('email', 'admin@example.com');

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never-quess';
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"postgresql+{driver}://{user}:{password}@{host}{f':{port}' if port else ''}/{database}";
    SQLALCHEMY_TRACK_MODIFICATIONS = False;
    MAIL_SERVER = mail_server;
    MAIL_PORT = int(mail_port);
    MAIL_USE_TLS = mail_use_tls;
    MAIL_USERNAME = mail_username;
    MAIL_PASSWORD = mail_password;
    ADMINS = admins;

# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'https://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'https://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]