===============================
Trafidemo
===============================

CURRENT STATUS: UNDER DEVELOPMENT.

::

    This is demo app to show functionality of following features:
    1) Flask project created by using cookiecutter and .. _cookiecutter-flask: https://github.com/sloria/cookiecutter-flask template
    2) Using Pandas and Numpy to load data of 5M+ vehicles from finnish Trafi into local MongoDB.
    3) Grouping data by municipal and by municipal+year and calculating percentiles (quantile) for Co2, power and mileage
    4) Simple API to share grouped data
    5) Simple Angular 1 application to show data from API
    6) Simple React application to show data from API (UNDER DEVELOPMENT)


Installation
-------------

::

    git clone https://github.com/ylitormatech/trafidemo
    cd trafidemo
    pip install -r requirements/dev.txt
    bower install
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

    # Loads data from Trafi into local MongoDB
    python download_trafidata.py

    # Groups data and calculates percentile(quantile)
    python load_trafidata.py

    python manage.py server


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
