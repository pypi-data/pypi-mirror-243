Changelog
=========

1.0.0
-----

Breaking changes
~~~~~~~~~~~~~~~~

For the `runuwsgi` management command, This release rewrites the
configuration handling entirely. Internally, all options are now
passed in a generated INI file (with mostly the same defaults as before).

All special handling of environment variables was removed (meaning that
handling of these variables is now left to uWSGI itself.

Likewise, al lspecial meaning of command-line optiosn was removed. All
command-line options are now passed verbatim to the `uwsgi` command.

In general, all overrides should now be made in Django settings.
