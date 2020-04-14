from homepage import create_app
import sys

app = create_app()
app.app_context().push()

from homepage import db, bcrypt
from homepage.models import User, Post, Role, UserRoles

print('Users in the Database:', file=sys.stderr)
print(User.query.all() , file=sys.stderr)

print('Posts in the Database:', file=sys.stderr)
print(Post.query.all() , file=sys.stderr)

print('Roles in the Database:', file=sys.stderr)
print(Role.query.all(), file=sys.stderr)
 
print('UserRoles in the Database:', file=sys.stderr)
print(UserRoles.query.all(), file=sys.stderr)