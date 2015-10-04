# talktoyourapp
"Porozmawiaj ze swoją aplikacją" application related to PyCon PL talk


# Local installation:

    mkvirtualenv talk -p /usr/local/bin/python3.4
    echo "cd `pwd`" >> ~/.virtualenvs/talk/bin/postactivate
    echo "source ./env.local.sh" >> ~/.virtualenvs/talk/bin/postactivate

    workon talk
    pip install -r requirements.txt
    heroku git:remote --app talktoyourapp
    cp env.example.sh env.local.sh
    # Edit env.local.sh


# Deployment:

Push / merge your changes to master and Heroku will automatically deploy it. Afterwards, the only thing you need to do is running migrations::

    heroku run "python manage.py migrate"

