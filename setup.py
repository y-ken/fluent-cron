#!/usr/bin/env python
from setuptools import setup, find_packages

from fluent_cron.version import VERSION

setup(
    name='fluent-cron',
    version=VERSION,
    author='Kentaro Yoshida',
    author_email='y.ken.studio@gmail.com',
    description='Fluent-cron is a command-line wrapper that reports unsuccessful runs to Fluentd (http://fluentd.org)',
    license='MIT',
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    url='http://github.com/y-ken/fluent-cron',
    packages=find_packages(),
    install_requires=['fluent-logger'],
    data_files=[],
    entry_points={
        'console_scripts': [
            'fluent-cron = fluent_cron.runner:run',
        ]
    }
)
