from getpass import getuser
from os import getenv, path, SEEK_END
from fluent import sender
from fluent import event
from subprocess import call
from tempfile import TemporaryFile
from argparse import ArgumentParser
from sys import argv
from time import time
from .version import VERSION
import re
import argparse

MAX_MESSAGE_SIZE = 1000

parser = ArgumentParser(
    description='Wraps commands and reports failing ones to fluentd.',
    epilog='FLUENT_CONF can also be passed as an environment variable.',
)
parser.add_argument(
    '--config',
    metavar='FLUENT_CONFIG',
    default=getenv('FLUENT_CONFIG'),
    help='Fluentd logging configurations',
)
parser.add_argument(
    '--version',
    action='version',
    version=VERSION,
)
parser.add_argument(
    'cmd',
    nargs=argparse.REMAINDER,
    help='The command to run',
)

def update_config(opts):
    """Update the Sentry DSN stored in local configs

    It's assumed that the file contains a DSN endpoint like this:
    https://public_key:secret_key@app.getsentry.com/project_id

    It could easily be extended to override all settings if there
    were more use cases.
    """

    homedir = path.expanduser('~%s' % getuser())
    home_conf_file = path.join(homedir, '.fluent-cron')
    system_conf_file = '/etc/fluent-cron.conf'

    conf_precedence = [home_conf_file, system_conf_file]
    for conf_file in conf_precedence:
        if path.exists(conf_file):
            with open(conf_file, "r") as conf:
                opts.config = conf.read().rstrip()
            return

def run(args=argv[1:]):
    opts = parser.parse_args(args)

    # Command line takes precendence, otherwise check for local configs
    if not opts.config:
        update_config(opts)
    runner = CommandReporter(**vars(opts))
    runner.run()

class CommandReporter(object):
    def __init__(self, cmd, config):
        if len(cmd) <= 1:
            cmd = cmd[0]

        self.command = cmd

        if not config is None:
            pattern = re.compile('(\w+):(\w+|\([^)]+\));?')
            param = dict(pattern.findall(config))
        if param.get('host') is None:
            param['host'] = 'localhost'
        if param.get('port') is None:
            param['port'] = 24224
        sender.setup(param['tag'], host=param['host'], port=param['port'])

    def run(self):
        buf = TemporaryFile()
        start = time()

        exit_status = call(self.command, stdout=buf, stderr=buf, shell=True)
        
        if exit_status > 0:
            elapsed = int((time() - start) * 1000)
            self.report_fail(exit_status, buf, elapsed)

        buf.close()
        
    def report_fail(self, exit_status, buf, elapsed):
        # Hack to get the file size since the tempfile doesn't exist anymore
        buf.seek(0, SEEK_END)
        file_size = buf.tell()
        if file_size < MAX_MESSAGE_SIZE:
            buf.seek(0)
            last_lines = buf.read()
        else:
            buf.seek(-(MAX_MESSAGE_SIZE-3), SEEK_END)
            last_lines = '...' + buf.read()

        message="Command \"%s\" failed" % (self.command,)

        event.Event('', {
           'command':     self.command,
           'exit_status': exit_status,
           'message':     message,
           'last_lines':  last_lines,
           'time_spent': elapsed,
        })

