Changelog
=========

0.8.11
------

* Add preview widget in Image Field Form (thanks Leo!)

0.8.10
-----

* New templatetag to check if user has role

0.8.9
-----

* Bugfix

0.8.8
-----

* Support Django 4.2
* Use DeleteView.form_valid instead of DeleteView.delete
* Add no-cache headers to login redirects

0.8.7
-----

* Update jquery

0.8.6
-----

* Allow overriding home url

0.8.5
-----

* Limit split_datetime_field time widget to minutes

0.8.4
-----

* Allow setting form id or class on base_form.html
* Use time input_type on split_datetime_field

0.8.3
-----

* Fix password change views
* Show errors on delete view

0.8.2
-----

* Add GASConfig.default_auto_field
* Remove default_app_config
* Add admin.py file

0.8.1
-----

* Bugfix

0.8
---

* form_actions block on delete confirmation template
* Cancel url for GAS views

0.7.3
-----

* 'show_deleted_objects' boolean attribute in GASDeleteView

0.7.2
-----

* Add GET support to AjaxCommandMixin
* Enhanced json encoder, available in AjaxCommandsMixin
* Add Shakarina to collaborators, thanks!

0.7.1
-----

* Fix login view
* Fix initial roles in user form

0.7
---

* Enhance sidebar menu
* Use all css files on login template
* Make user admin section optional
* Show role description in user edit form

0.6
---

* Close button for messages
* Add locale files to package
* Add basque translations

0.5.1
-----

* Fix typo

0.5
---

* Update spanish translations
* multipart/form-data by default
* New templatetag for pagination

0.4
---

* Helper function to use SplitDateTimeField for datetimes
* Update spanish translation

0.3
---

* Allow extending GAS media files
* Allow actions in every view
* Enhance support for inline formsets
* Add missing templates
* Add help_text to gas views

0.2
---

* Allow overriding base_form template controls
* Style login
* Fix migration
* Add spanish translation
* Add form.media to base_form.html
* Fix license in setup.cfg

0.1
---

Initial relase.
