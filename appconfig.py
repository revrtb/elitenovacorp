
class Config():
    TESTING = False
    SECRET_KEY = '\x01\xc8$\x97\xd9\x1a\x13\xd9\x9eE\xabS\xc8\x17\xa4\xc3\x14\xe8Re\x94\x8cKR'


class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = ""
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'support@EliteNovaCorp.com'
    MAIL_PASSWORD = ''
    RECAPTCHA2_PUBLIC_KEY=''
    RECAPTCHA2_PRIVATE_KEY=''
    RECAPTCHA2_DATA_ATTRS = {'theme': 'dark'}

class MailData():
	FROM = 'support@EliteNovaCorp.com'
	TO = ['support@EliteNovaCorp.com']

class Domain():
    DOMAIN = ""

class MYSQLDB():
    USER = 'root'
    PASSWORD = ''
    DB = 'test'
    HOST = '127.0.0.1' 
    PORT = 3306    
