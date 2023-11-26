Changelog
=========

2.0.0
-----
 - migrated to Pyramid 2.0

1.2.0
-----
 - added support for default value when using I18n query_attribute method
   or i18n TALES extension
 - added support for Python 3.10 and 3.11

1.1.0
-----
 - removed support for Python < 3.7
 - updated doctests

1.0.7
-----
 - removed Travis-CI configuration

1.0.6
-----
 - updated "adapter_config" decorator arguments names

1.0.5
-----
 - updated management of default value in I18n schema fields
 - added "default" argument in II18n "query_attribute" method
 - updated doctests

1.0.4
-----
 - updated Travis-CI integration

1.0.3
-----
 - updated doctests

1.0.2
-----
 - use request's registry instead of global registry when looking for settings

1.0.1
-----
 - force server language of language negotiator in constructor to avoid recursion error when
   getting localizer

1.0.0
-----
 - initial release
