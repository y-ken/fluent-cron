Raven-cron : error reporting for cron commands
================================================

Raven-cron is a small command-line wrapper that reports errors to
[Sentry](http://getsentry.com) if the script exits with an exit status other
than zero.

Install
-------

`pip install raven-cron`

Usage
-----

```
usage: raven-cron [-h] [--dsn SENTRY_DSN] [--version] cmd [cmd ...]

Wraps commands and reports failing ones to sentry.

positional arguments:
  cmd               The command to run

optional arguments:
  -h, --help        show this help message and exit
  --dsn SENTRY_DSN  Sentry server address
  --version         show program's version number and exit

SENTRY_DSN can also be passed as an environment variable.
```

Example
-------

`crontab -e`
```
SENTRY_DSN=https://<your_key>:<your_secret>@app.getsentry.com/<your_project_id>
@reboot raven-cron ./my-process
```

Misc
----

Copyright 2013 to MediaCore Technologies and licensed under the MIT license.

