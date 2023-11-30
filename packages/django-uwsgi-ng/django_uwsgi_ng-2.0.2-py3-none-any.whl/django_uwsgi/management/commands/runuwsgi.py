from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
import os
import sys
import multiprocessing
from tempfile import TemporaryDirectory

root = os.getcwd()
django_project = os.path.basename(root)


class Command(BaseCommand):
    help = "Runs this project as a uWSGI application. Requires the uwsgi binary in system path."

    def add_arguments(self, parser):
        parser.add_argument('uwsgi_options', nargs='*')

    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % django_project)

        # Define hard defaults
        UWSGI_OPTIONS = {
            "module": '%s.wsgi' % django_project,
            "http-socket": ":8000",
            "http-auto-chunked": True,
            "http-keepalive": 75,
            "http-timeout": 75,
            "no-defer-accept": True,
            "workers": int(multiprocessing.cpu_count() * 1.5),
            "auto-procname": True,
            "procname-prefix-spaced": "[uWSGI %s]" % django_project,
            "vacuum": True,
            "master": True,
            "virtualenv": sys.prefix,
            "pp": root,
            "post-buffering": 1048576,
            "buffer-size": 65535,
            "reload-on-rss": 300,
            "enable-threads": True,
            "lazy-apps": False,
            "thunder-lock": True,
            "autoload": True,
            "no-orphans": True,
            "memory-report": True,
            "disable-logging": True,
            "ignore-sigpipe": True,
            "ignore-write-errors": True,
            "disable-write-exception": True,
            "harakiri": 60,
            "harakiri-verbose": True,
            "cache2": "name=%s,items=20000,keysize=128,blocksize=4096" % django_project,
        }

        # Defien configuration-dependent defaults
        if UWSGI_OPTIONS.get("workers", 1) > 1 and not "cheaper" in UWSGI_OPTIONS:
            UWSGI_OPTIONS["cheaper"] = int(UWSGI_OPTIONS["workers"] / 1.5)
        if getattr(settings, "UWSGI_SERVE_STATIC", settings.DEBUG):
            UWSGI_OPTIONS.setdefault("static-map", []).append('%s=%s' % (settings.STATIC_URL, settings.STATIC_ROOT))
        if getattr(settings, "UWSGI_SERVE_MEDIA", settings.DEBUG) and hasattr(settings, "MEDIA_ROOT"):
            UWSGI_OPTIONS.setdefault("static-map", []).append('%s=%s' % (settings.MEDIA_URL, settings.MEDIA_ROOT))
        if settings.DEBUG:
            UWSGI_OPTIONS["py-autoreload"] = 2
        if 'django_uwsgi' in settings.EMAIL_BACKEND:
            UWSGI_OPTIONS["spooler"] = "/tmp"
            UWSGI_OPTIONS["spooler-import"] = "django_uwsgi.tasks"

        # Drop defaults that were set as environment variables
        for key in UWSGI_OPTIONS:
            if "UWSGI_%s" % key.upper().replace("-", "_") in os.environ:
                del UWSGI_OPTIONS[key]

        # Merge uWSGI options from settings
        opts = getattr(settings, "UWSGI_OPTIONS", {})
        legacy_opts = getattr(settings, "UWSGI", {})
        UWSGI_OPTIONS.update(legacy_opts)
        UWSGI_OPTIONS.update(opts)

        if apps.ready:
            argv = ['uwsgi']
            # Pass the config dict as INI file
            with TemporaryDirectory() as tmpdir:
                with open(os.path.join(tmpdir, "uwsgi.ini"), "w") as ini_out:
                    print("[uwsgi]", file=ini_out)
                    for option, values in UWSGI_OPTIONS.items():
                        if not isinstance(values, (list, tuple)):
                            values = [values]
                        for value in values:
                            if isinstance(value, bool):
                                value = "1" if value else "0"
                            elif not isinstance(value, str):
                                value = str(value)
                            if "\n" in value:
                                raise ImproperlyConfigured("Line breaks are not allowed in uWSGI options.")
                            print("%s = %s" % (option, value), file=ini_out)
                argv += ['--ini', os.path.join(tmpdir, "uwsgi.ini")]
                argv += options['uwsgi_options']
                os.execvp('uwsgi', argv)

    def usage(self, subcomand):
        return r"""
  run this project on the uWSGI server
  All command-line arguments are passed verbatim to the uwsgi command
        """
