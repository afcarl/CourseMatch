import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db'))
WTF_CSRF_SECRET_KEY = 'random key for form'
LDAP_PROVIDER_URL = 'ldap://jet.earlham.edu:389'
LDAP_PROTOCOL_VERSION = 3
