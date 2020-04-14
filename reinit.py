from homepage import create_app
import sys

app = create_app()
app.app_context().push()

from homepage import db, bcrypt

print('Dropping Database...', file=sys.stderr)
db.drop_all()
print('Database dropped!', file=sys.stderr)

print('Reinitializing Database..', file=sys.stderr)
db.create_all()
print('Database reinitialized!', file=sys.stderr)

from homepage.models import User, Post, Role, UserRoles

#Create User Roles
role_default = Role( id = 0, name = 'default')
role_member = Role( id = 1, name = 'member')
role_admin  = Role( id = 2, name = 'admin')
db.session.add(role_default)
db.session.add(role_member)
db.session.add(role_admin)

#Create the admin User

admin_mail = app.config['ADMIN_MAIL']
admin_name = app.config['ADMIN_NAME']
hashed_password = bcrypt.generate_password_hash(app.config['ADMIN_PASSWORD']).decode('utf-8')

user_admin = User(username = admin_name, email=admin_mail,password=hashed_password)
user_admin.roles.append(Role.query[2])
db.session.add(user_admin)


#________Rdy______
db.session.commit() 

print('Users in the Database:', file=sys.stderr)
print(User.query.all() , file=sys.stderr)

print('Posts in the Database:', file=sys.stderr)
print(Post.query.all() , file=sys.stderr)

print('Roles in the Database:', file=sys.stderr)
print(Role.query.all(), file=sys.stderr)
 
print('UserRoles in the Database:', file=sys.stderr)
print(UserRoles.query.all(), file=sys.stderr)
 



