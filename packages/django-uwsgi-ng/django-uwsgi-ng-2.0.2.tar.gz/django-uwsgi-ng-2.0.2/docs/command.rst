Management Command
==================

runuwsgi
--------

.. code-block:: sh

   python manage.py runuwsgi

Configuration
~~~~~~~~~~~~~

uWSGI is configured with a set of defaults, which can be overridden in
the Django settings by defininge a dictionary named `UWSGI_OPTIONS`.
It can contain any uWSGI options; multi-value options are given as
a list as value.

.. code-block:: python

   UWSGI_OPTIONS = {
       "module": "my.project.wsgi",
       "attach-daemon": ["memcached -p 11311", "celery -A my.project.tasks worker"]
   }

If an option is found the the process environment, it is removed from the
default settings, to ensure that environment variables take precedence.
Settings explicitly set in the Django settings dict are not stripped
in favour of environment variables.

Additionally, all command-line options to `runuwsgi` are passed verbatim
to the forked `uwsgi` command.
