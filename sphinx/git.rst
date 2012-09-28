Git integration
===============

Introduction
------------

Moa integrates with `Git <http://git-scm.com/>`_ repositories to
easily add templates from any git repository. This currently only
works when having the moaGit plugin enabled and with having your moa
workflow under git version control. Upon installing a git based
template, moa merges the template repository with the workflow's
repository using the git subtree merge strategy. In short, the
template repository is added as a remote to the workflow's repository
and subsequently merged with the workflow. This strategy has a number
of nice properties:

- The template is properly integrated in the local workflow and can be
  copied around and changed (as one normally would do within a git
  repository).
- The template code does not change unless requested. Even when
  duplicating your repository - the template remains unchanged.
- If required, it is possible to update to the latest version of the
  remote template repository (using a regular `moa refresh`)

As a note - the git submodule approach was another candidate for
implenting this, but copying submodules around is much more
cumbersome.

Installation
------------

To set up moa to work with git template you meed to define a template
provider in the configuration (for example in
`~/.config/moa/config`). For example::

    template:
      providers:
        mfg:
          enabled: false
          class: gitmodule
          base: 'https://github.com/mfiers/moa_template_'


This defines a provider (called mfg) that pulls templates from
github. After doing this you can run::

    moa new mfg:bowtie

which would expect and merge a repository in the following location:

    https://github.com/mfiers/moa_template_bowtie

Moa requires to have template name (bowtie in the example above) and
the configured `base` resolve to a valid git repository url. This
provides a user friendly syntax and the ability to use any git
repository required.


