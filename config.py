import os
import os.path as op


class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    directory_img = basedir + '/static/images/posts_img/'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


    ### Flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    # 
    UPLOADS_DEFAULT_DEST = basedir + '/static/'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/uploadimages/'
    
    UPLOADS_DEFAULT_DEST_IMG = UPLOADS_DEFAULT_DEST + '/images/'
    UPLOADED_IMAGES_DEST = directory_img
    UPLOADED_IMAGES_URL = 'http://localhost:5000/uploadimages/'
    UPLOAD_FOLDER = UPLOADED_IMAGES_DEST