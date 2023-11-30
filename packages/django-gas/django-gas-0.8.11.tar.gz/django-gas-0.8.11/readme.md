GAS
===

Generic Administration Sistem, an alternative to django admin with a set
of generic views.


Instalation
-----------

1. Install `django-gas` package:

    pip install django-gas

2. Add `'gas'` to `INSTALLED_APPS`
3. Add `gas` urls to project's `urls.py`:

    import gas.sites

    urlpatterns = [
        path('control-panel/', include(gas.sites.site.urls)),
    ]

4. Run `python manage.py migrate`


Configuration
-------------

Project settings can customize the `gas` control panel:

* `GAS_TITLE`: Name of the control panel.
* `GAS_LOGO`: Icon for the control panel.
* `GAS_MEDIA`: A django form's Media like dict with css and js files.
  Overrides default css and javascript.
* `GAS_EXTRA_MEDIA`: A django form's Media like dict with css and js
  files. Extends current css and javascript instead of overriding.

The default values of those settings can be viewed in the
`gas/gas_settings.py` file.


Integration
-----------

Create a submodule `gas.config` in your django app. 

        -\ yourapp
            \gas
                __init__.py
                config.py
            admin.py
            models.py
            ...

Edit this `config.py` file to register your code into `gas`. For examples look
at `gas.gas.config` and `gas.gas.users` modules.

Gas comes with a basic user management. To enable this section, import
`gas.gas.users_config` from any `gas.config` of your installed apps.

To enable the urls but keep the section out of the menu, just add this to
your `gas.config`:

    site.register_urls('users', 'gas.gas.users.urls')


Licenses
--------

The license of the code is GPLv3, but in the `gas/static/vendor` folder there
is some external code with different licenses.
