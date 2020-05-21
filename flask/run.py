from homepage import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5001, debug=True, threaded=True)


#Cheats
#  print('POSTI!', file=sys.stderr)
# from run import app
# from homepage import db
# db.drop_all()
# db.create_all()
# User.query.all()

#from homepage import create_app
#app = create_app()
#app.app_context().push()
#from homepage import db