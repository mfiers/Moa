Git integration
===============

Introduction
------------

Moa integrates with `Git <http://git-scm.com/>`_ repositories to
easily add templates from any git repository. This requires that you
have the moaGit plugin enabled and that your Moa workflow is under Git
version control. Upon installing a Git based template, moa merges the
template repository with the workflow's repository using the `git
subtree <https://github.com/apenwarr/git-subtree>`_. This approach has
a a number of nice properties:

- The template is integrated in the local workflow and can be copied
  around and changed (as one normally would do within a git
  repository).
- The template code does not change unless requested. Even when
  duplicating your repository - the template remains unchanged.
- If required, it is possible to update to the latest version of the
  remote template repository (using a regular `moa refresh`)
- It possible to upload the template changes upstream.

Note - the git submodule approach was another candidate for implenting
this, but submodules are difficult to be copied once they are checked
out. Additionally, the `git subtree
<https://github.com/apenwarr/git-subtree>`_ approach has as an
advantage above the `git subtree merge strategy
<https://www.kernel.org/pub/software/scm/git/docs/howto/using-merge-subtree.html>`_
that it is easier to upload changes upstream. A downside is that an
extra prerequisite is added.

Installation
------------

Install `git subtree`
=====================

See: https://github.com/apenwarr/git-subtree for installation instructions

Define a template provider
==========================

To set up moa to work with git template you need to define a template
provider, for example::

	moa set -s template.providers.gtp.class=gitmodule
	moa set -s template.providers.gtp.base='https://github.com/mfiers/moa_template_'
    moa set -s template.providers.gtp.enabled=true

This defines a provider (called gtp) that pulls templates from github
(but any other git server can be used). Note that it is probably
advisable to set `*.enabled=true` as last - to prevent an incomplete
import.

After doing this you can run::

    moa new gtp:bowtie

which would expect and merge a repository in the following location:

    https://github.com/mfiers/moa_template_bowtie

Moa requires to have template name (bowtie in the example above) and
the configured `base` resolve to a valid git repository url. This
provides a user friendly syntax and the ability to use any git
repository required.


