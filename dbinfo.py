from homepage import create_app
import sys

app = create_app()
app.app_context().push()

from homepage import db, bcrypt
from homepage.models import User, Post, Role, UserRoles, Comment

print('Users in the Database:', file=sys.stderr)
print(User.query.all() , file=sys.stderr)

print('Posts in the Database:', file=sys.stderr)
print(Post.query.all() , file=sys.stderr)

print('Roles in the Database:', file=sys.stderr)
print(Role.query.all(), file=sys.stderr)
 
print('UserRoles in the Database:', file=sys.stderr)
print(UserRoles.query.all(), file=sys.stderr)


# comment = Comment(content = 'askdjbasökjdnalöskfdnalsd', author_comment = 0, post_comment = 0)
# comment = Comment(content = 'askdjbasökjdnalöskfdnalsd', uid = 0, pid = 0)
# db.session.add(comment)
# db.session.commit()

print('Comments in the Database:', file=sys.stderr)
print(Comment.query.all(), file=sys.stderr)
