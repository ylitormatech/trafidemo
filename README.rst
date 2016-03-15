===============================
Trafidemo
===============================

CURRENT STATUS: UNDER DEVELOPMENT. DEMO NOT FULLY WORKING

This is demo app to show functionality of several features:
1. Flask with cookiecutter-flask project template
2. Loading vehicle data (zip, csv and excel formats) from finnish Trafi into local MongoDB
3. Publishing data with API
4. Simple Angular 1 and ReactJS UI that uses API

Rest of information in Finnish...

Asennusohjeet
-------------

    git clone https://github.com/ylitormatech/trafidemo
    cd trafidemo
    pip install -r requirements/dev.txt
    bower install
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server
    python load_trafidata_localMongoDB.py



Deployment
----------

In your production environment, make sure the ``TRAFIDEMO_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
