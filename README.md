# fluent-cron : error reporting for cron commands

fluent-cron is a small command-line wrapper that reports errors to
[Fluentd](http://fluentd.org) if the script exits with an exit status other
than zero.

It has forked from [raven-cron](https://github.com/mediacore/raven-cron).

## Install

Install with following commands. Dependent packages will be installed `fluent-logger` and `msgpack-python` at the same time.

```sh
$ sudo pip install git+https://github.com/y-ken/fluent-cron.git
```

## Usage

```
usage: fluent-cron [-h] [--config FLUENT_CONFIG] [--version] cmd [cmd ...]

Wraps commands and reports failing ones to Fluentd.

positional arguments:
  cmd                     The command to run

optional arguments:
  -h, --help              show this help message and exit
  --config FLUENT_CONFIG  Fluentd connection options
  --version               show program's version number and exit

FLUENT_CONFIG can also be passed as an environment variable.
```

## Example

`crontab -e`


```
30 * * * * fluent-cron --config "tag:myapp.cron" /path/to/some-task.sh

FLUENT_CONFIG="tag:myapp.cron;host:localhost;port:24224"
30 * * * * fluent-cron /path/to/some-task.sh

FLUENT_CONFIG="tag:myapp.cron;host:localhost;port:24224"
30 * * * * fluent-cron "php /path/to/some-task.php"
```

## data structure

* command: executed commands
* exit_status: 1 or more number
* message: e.g. `Command foo failed`
* last_lines: last 1000 lines of script stdout and stderr
* time_spent: execution elapsed time as micro seconds

## Restrictions

Pull requests are very welcome!!
I'm awaiting pull requests like below.

* support multiple commands like below.<br>
It works: `fluent-cron "script1.sh && script2.sh"`<br>
It won't works: `fluent-cron script1.sh && script2.sh`

## Copyright

Copyright © 2014- Kentaro Yoshida (@yoshi_ken)

## License

* MIT License http://www.opensource.org/licenses/mit-license.php
