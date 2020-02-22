from flask import Flask, redirect, url_for, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads


from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_pagedown import PageDown
from flaskext.markdown import Markdown


from flask_admin.contrib.fileadmin import FileAdmin
import os
import os.path as op

from flask_security import SQLAlchemyUserDatastore, Security, current_user


app = Flask(__name__)
pagedown = PageDown(app)
Markdown(app)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

directory_uploads = Configuration.basedir + '/static/'




from models import *
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post, 'Tag': Tag, 'User': User, 'Role': Role, 'user_datastore': user_datastore}

#### ADMIN ####

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect( url_for('security.login', next=request.url ))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['id', 'title', 'description', 'body', 'tags', 'created', 'img_filename', 'author']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name']


class UserAdminView(AdminMixin, BaseModelView):
    form_columns = ['id', 'login', 'name', 'secname', 'email', 'password', 'active', 'roles']

admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'), template_mode='bootstrap3')
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

admin.add_view(UserAdminView(User, db.session))
admin.add_view(FileAdmin(directory_uploads, '/static/', name='Static Files'))

##### FLASK SECURITY #######

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

