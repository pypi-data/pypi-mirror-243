Changelog
=========

2.0.1
-----
 - updated Buildout configuration

2.0.0
-----
 - upgrade to Pyramid 2.0

1.7.1
-----
 - packaging issue

1.7.0
-----
 - added support for undefined content providers
 - added support for boolean provider arguments
 - added support for Python 3.10 and 3.11

1.6.3
-----
 - updated Gitlab-CI configuration file

1.6.2
-----
 - added method to base content provider to load required Fanstatic resources

1.6.1
-----
 - don't load content provider resources when rendered content is empty

1.6.0
-----
 - added RawContentProvider class, to provide a component rendering raw HTML code but with the
   content provider API

1.5.0
-----
 - added "template_name" argument to content provider "render" method, to be able to
   specify name of a custom registered template on rendering

1.4.0
-----
 - removed support for Python < 3.7

1.3.5
-----
 - removed Travis-CI configuration

1.3.4
-----
 - doctest update to handle viewlets uniform sorting

1.3.3
-----
 - packaging version mismatch!

1.3.2
-----
 - refactored viewlet registration code

1.3.1
-----
 - packaging update

1.3.0
-----
 - updated viewletmanager_config to be able to declare a viewlet manager as a viewlet in a
   single step
 - updated "provider" TALES extension to be able to provide arguments to extension
 - small updates in registry access

1.2.1
-----
 - updated TALES *provider* expression to also support a mapping of provider factories into
   request annotations

1.2.0
-----
 - updated TALES *provider* expression to be able to define a custom content provider during
   traversal using request a "provider:{provider-name}:factory" annotation, instead of using a
   classical adapter lookup

1.1.0
-----
 - updated doctests
 - removed ZCML directives

1.0.2
-----
 - updated Travis-CI configuration

1.0.1
-----
 - updated doctests

1.0.0
-----
 - initial release
