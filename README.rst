#######################
Django JS Error Logging
#######################

The Django JS Error Logging is logging for Client-Side JavaScript errors.
You can log by the following three ways.

* Save to Django model
* Notify by Email
* Logging by python logger


Installation
============

#. Add the ``jserrorlogging`` directory to your Python path.

   Can use pip command::

       $ pip install django-js-error-logging

#. Add ``jserrorlogging`` to your ``INSTALLED_APPS``.::

       INSTALLED_APPS = (
           # ...
           'jserrorlogging',
           # ...
       )

#. Add the following context processor to your ``TEMPLATE_CONTEXT_PROCESSORS``.::

       TEMPLATE_CONTEXT_PROCESSORS = (
           # ...
           'jserrorlogging.context_processors.static',
           # ...
       )

#. Add the following configuration to your ``urls.py``.::

       urlpatterns = patterns(
           # ...
           url(r'^jserr/$', include('jserrorlogging.urls', namespace='jserrorlogging')),
           # ...
       )

#. Add the following templatetag to head tag in your template.::

       <head>
       # ...
       {% include "jserrorlogging/includes/script.html" %}
       # ...
       </head>

   About more information of static files for Django,
   you can see at https://docs.djangoproject.com/en/dev/howto/static-files/.

#. Add the following static files.

   Copy ``static/jserrorlogging`` directory to ``STATIC_ROOT`` or run the following command::

       $ python manage.py collectstatic

#. Run syncdb.::

       $ python manage.py syncdb

   **Note**: When your project use South, run the following command.::

       $ python manage.py migrate jserrorlogging

   If you don't want to save to django model, don't you run these commands.


Configuration
=============

Django JS Error Logging has the following optional settings. 

Save to Django model
--------------------

You can see results of logging in Admin site.

This option is default enabled.
When you don't need to this option, ``JSERRORLOGGING_ENABLE_MODEL`` set to False.

Notify by Email
---------------

You can send results of logging to Email.

This option is default enabled.
When you don't need to this option, ``JSERRORLOGGING_ENABLE_MAIL`` set to False.

``JSERRORLOGGING_MAIL_TO``
   Default: ``settings.MANAGERS``

   You can set the custom recipients for notification::

       JSERRORLOGGING_MAIL_TO = (
           ('someone', 'someone@example.com'),
       )

``JSERRORLOGGING_MAIL_NOTIFY_INTERVAL``
   Default: ``3600``

   When the same errors occurred,
   you can stop notification for the duration of this setting (seconds).

Logging by python logger
------------------------

You can use Python's builtin logger.

This option is default disabled. 
When you need to this option, ``JSERRORLOGGING_ENABLE_LOGGER`` set to True.
And ``JSERRORLOGGING_LOGGER_NAME`` set to your custom logger name.

Example::

   LOGGING = {
       # ...
       'loggers': {
           # ...
           'jserror': {
               'handlers': ['console', 'mail_admins'],
               'level': 'INFO',
               'filters': ['special']
           },
           # ...
       }
       # ...
   }

   # ...

   JSERRORLOGGING_ENABLE_MODEL = 'jserror'

   # ...

About more information of logging for Django,
you can see at https://docs.djangoproject.com/en/dev/topics/logging/.

Logging additional data
-----------------------

You can log your custom data.

For example, Django JS Error Logging has another template for the following additional data.

* ``django.contrib.auth.User.id``
* ``request.session.session_key``

When you want to log user_id and session_key, set the following templatetag::

   <head>
   # ...
   {% include "jserrorlogging/includes/script_with_user.html" %}
   # ...
   </head>

If you want to log another data, 
Create a template that extends ``jserrorlogging/includes/script.html`` and 
edit ``meta_data`` block.

Example (path_to_your_template_dir/script_with_more_data.html)::

   {% extends "jserrorlogging/includes/script.html" %}
   {% block meta_data %}
   djjserr.meta = {
       username: '{{ user.username }}',
       always_true: true
   };
   {% endblock %}

Others
------

other configuration options.

``JSERRORLOGGING_LOG_MODEL``
   Default: 'jserrorlogging.Log'
    
   A name of model to save log.

``JSERRORLOGGING_STATIC_URL``
   Default: settings.STATIC_URL + 'jserrorlogging/'
    
   A URL of script files for Django JS Error Logging.
