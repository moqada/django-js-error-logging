# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-js-error-logging',
    version='0.1.1',
    description='Logging Client-Side JavaScript errors for Django',
    long_description=open('README.rst').read(),
    author='Masahiko Okada',
    author_email='moqada@gmail.com',
    url='http://github.com/moqada/django-js-error-logging/',
    keywords=['django', 'javascript', 'logging', 'notify'],
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
