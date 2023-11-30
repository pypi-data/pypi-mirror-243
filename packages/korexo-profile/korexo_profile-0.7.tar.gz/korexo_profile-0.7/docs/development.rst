Development 
===========

An issue tracker is located at `GitLab
<https://gitlab.com/dew-waterscience/korexo_profile>`_.


The documentation is accessible on `GitLab
<https://dew-waterscience.gitlab.io/korexo_profile>`_ when you are signed in.

Contact Kent Inverarity for access to the GitLab site.

To build and publish a release
------------------------------

If necessary, create a new version with a git tag per setuptools-scm:

.. code-block::

  $ git log --oneline
  0ad38e0 (HEAD -> master) update everything
  13a8644 (tag: v0.2) update
  ab86ff2 (tag: v0.1) Initial commit
  $ git tag v0.3

Then the usual way to build a wheel:

.. code-block::
  
  $ python setup.py bdist_wheel

And to publish, the usual:

.. code-block::

  $ twine upload dist\korexo_profile-0.3-py3-none-any.whl
