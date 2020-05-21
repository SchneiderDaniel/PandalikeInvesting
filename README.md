Pandalike Investing Homepage
===========

This is the code of my homepage.



Installation
------------

You should create a virtual environment and install the required packages with the following commands:

    windows:
    python -m venv env
    .\env\Scripts\activate    
    (env) $ pip install -r requirements.txt


    Linux:
    python3 -m venv env
    source env/bin/activate
    (env) $ pip install -r requirements.txt

Hints for uwsgi:
- For Windwos uncomment uwsgi  from the requirements and use differnt app server or use cgywin
- For Linux Ubuntu and Python3 you have to run to

    apt-get install build-essential python3-dev

General Hints:
- Don't forget to setup the enviroments variable if you are not using docker. See config.py.


Docker
------------

for using docker-compose you need to add a .env file parallel to the docker-compose.yml. This needs to contain the enviroment variables of your system. Like:

    ADMIN_MAIL='myniceemail@test.de'
    ...


Run
------------

In order to run it make sure that your venv is runnig and then

    Windows:
    $ .\env\Scripts\activate 
    (env) $ env:FLASK_APP="run.py"
    (env) $ flask run

    Linux:
    source env/bin/activate
    (env) $ env:FLASK_APP="run.py"
    (env) $ flask run


or

    Windows:
    $ .\env\Scripts\activate 
    (env) $ pyhton run.py

    Linux:
    source env/bin/activate
    (env) $ pyhton run.py

Contact
------------
   
If you have feedback, feel free to get in touch. Over the website or use github
