#!/usr/bin/env python
from setuptools import setup, find_packages

from raven_cron.version import VERSION

setup(
    name='raven-cron',
    version=VERSION,
    author='Jonas Pfenniger',
    author_email='zimbatm@zimbatm.com',
    description='Raven-cron is a command-line wrapper that reports unsuccessful runs to Sentry (https://www.getsentry.com)',
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    url='http://github.com/mediacore/raven-cron',
    packages=find_packages(),
    install_requires=['raven'],
    data_files=[],
    entry_points={
        'console_scripts': [
            'raven-cron = raven_cron.runner:run',
        ]
    }
)
