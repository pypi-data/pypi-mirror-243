Changelog
=========

2.0.0
-----
 - upgraded to Pyramid 2.0

1.3.1
-----
 - use internal tee to avoid multiple accesses to values getter (so that values adapters should be able to return
   iterators without any problem)
 - added support for Python 3.10 and 3.11

1.3.0
-----
 - added table and row update events, with matching subscribers predicates; these events are
   enabled by default but can be disabled by setting custom table attributes
 - handle dynamic CSS classes by supporting callables

1.2.1
-----
 - updated doctests

1.2.0
-----
 - removed support for Python < 3.7

1.1.3
-----
 - updated Gitlab-CI configuration

1.1.2
-----
 - updated Gitlab-CI configuration

1.1.1
-----
 - updated Gitlab-CI configuration
 - removed Travis-CI configuration

1.1.0
-----
 - added methods to render cells and rows contents in JSON format
 - updated "adapter_config" decorator arguments names

1.0.2
-----
 - updated doctests using ZCA hook

1.0.1
-----
 - use current request registry instead of global registry to query adapters

1.0.0
-----
 - initial release
