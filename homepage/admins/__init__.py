import  sys

from flask_admin.contrib.sqla import ModelView
from homepage import admin, db
from homepage.models import User, Post, Comment, Discussion, Report, Newsletter, Role, Tag, UserRoles, PostLikes, PostTags, CommentLikes, Portfolio
from flask_admin import Admin, BaseView, expose
from flask_login import current_user
from homepage import login_manager, login_required_author 


class MyAdminView(ModelView):
    

    def is_accessible(self):
        return current_user.is_authenticated

    @login_required_author('admin')
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():

            return redirect(url_for('main.index', next=request.url))


admin.add_view(MyAdminView(User, db.session))
admin.add_view(MyAdminView(Post, db.session))
admin.add_view(MyAdminView(Comment, db.session))
admin.add_view(MyAdminView(Discussion, db.session))
admin.add_view(MyAdminView(Report, db.session))
admin.add_view(MyAdminView(Newsletter, db.session))
admin.add_view(MyAdminView(Role, db.session))
admin.add_view(MyAdminView(Tag, db.session))
admin.add_view(MyAdminView(UserRoles, db.session))
admin.add_view(MyAdminView(PostLikes, db.session))
admin.add_view(MyAdminView(PostTags, db.session))
admin.add_view(MyAdminView(CommentLikes, db.session))
admin.add_view(MyAdminView(Portfolio, db.session))
