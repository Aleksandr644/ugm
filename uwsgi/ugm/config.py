import os
from configparser import ConfigParser

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never-quess'

basedir = os.path.abspath(os.path.dirname(__file__))

cfg = ConfigParser();
with open('db.ini') as fl:
    cfg.read_file(fl)
cfg = dict(cfg.items('postgresql'))
driver = cfg.get('driver', '')
host = cfg.get('host', 'localhost')
database = cfg.get('database', 'postgres')
password = cfg.get('password', '')
user = cfg.get('user', 'postgres')
port = cfg.get('port', '')

SQLALCHEMY_DATABASE_URI = f"postgresql+{driver}://{user}:{password}@{host}{f':{port}' if port else ''}/{database}"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'https://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'https://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]