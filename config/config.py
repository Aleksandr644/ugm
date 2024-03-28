import os
from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))
__cfg = ConfigParser();
with open('config/db.ini') as fl:
    __cfg.read_file(fl);
__cfg = dict(__cfg.items('postgresql'));
driver = __cfg.get('driver', '');
host = __cfg.get('host', 'localhost');
database = __cfg.get('database', 'postgres');
password = __cfg.get('password', '');
user = __cfg.get('user', 'postgres');
port = __cfg.get('port', '');

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never-quess';
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"postgresql+{driver}://{user}:{password}@{host}{f':{port}' if port else ''}/{database}";
    SQLALCHEMY_TRACK_MODIFICATIONS = False;

# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'https://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'https://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]