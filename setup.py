
import sys

from setuptools import setup, find_packages

extra_setup = {}
if sys.version_info >= (3,):
    extra_setup['use_2to3'] = True

setup(
    name='nosenicedots',
    version='0.2',
    description="Nose plugin that prints nicer dots grouped by class/module.",
    long_description=open('./README.rst').read(),
    author='Kumar McMillan',
    author_email='kumar.mcmillan@gmail.com',
    license="Apache License",
    packages=find_packages(exclude=['ez_setup']),
    install_requires=[r for r in open('requirements.txt')
                      if r.strip() and not r.startswith('#')
                      and not r.startswith('-e')],
    url='https://github.com/kumar303/nose-nicedots/',
    include_package_data=True,
    entry_points="""
        [nose.plugins.0.10]
        nicedots = nosenicedots:NiceDots
        """,
    classifiers = [
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 2'
        ],
    **extra_setup
    )
